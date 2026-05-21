"""
agent.py
--------
Local AI scheduling agent powered by Meta Llama 3.1 via the Ollama library.

This file wires together:
  • Five tool schemas  (one scheduling tool + four CRUD tools)
  • A robust `while True` agent heartbeat loop that:
      1. Sends the conversation history + tool schemas to Llama 3.1.
      2. Detects tool-call requests in the model's response.
      3. Dispatches to the correct Python function.
      4. Appends the tool result back to the message history.
      5. Loops until the model gives a plain conversational reply (no tool call).
  • Error handling so a crashed tool returns an error string to the LLM
    instead of crashing the whole script.

Usage
-----
    python agent.py

The agent then prompts you for input.  Type your scheduling request in plain
English.  Examples:
    "Schedule all batches for 2025-08-01"
    "Show me sessions for faculty 1001"
    "Update schedule_id 5 — change the date to 2025-08-10"
    "Delete schedule_id 12"
"""

import ollama

# Import every tool function we want the agent to be able to call.
from scheduling_tool       import session_allocation
from session_manipulation_tool import (
    get_sessions,
    insert_session,
    update_session,
    delete_session,
)


# ===========================================================================
# TOOL SCHEMAS
# These JSON structures describe each Python function to the LLM in the
# format Ollama / the Llama tool-calling spec expects.  The LLM reads them
# and decides which function (if any) to invoke based on the user's request.
# ===========================================================================

# ---------------------------------------------------------------------------
# Tool 1: session_allocation  — generates a full schedule for a given date
# ---------------------------------------------------------------------------
schedule_tool_schema = {
    "type": "function",
    "function": {
        "name": "session_allocation",
        "description": (
            "Generates and saves a complete faculty-to-batch schedule for a "
            "given date.  Use whenever the user asks to schedule, allocate, "
            "or assign faculty sessions for a day."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "session_date": {
                    "type": "string",
                    "description": "The date to schedule in YYYY-MM-DD format.",
                }
            },
            "required": ["session_date"],
        },
    },
}

# ---------------------------------------------------------------------------
# Tool 2: get_sessions  — READ sessions (queries the Session table)
# ---------------------------------------------------------------------------
get_sessions_tool_schema = {
    "type": "function",
    "function": {
        "name": "get_sessions",
        "description": (
            "Retrieves session records from the database.  Use when the user "
            "asks to view, look up, find, or check sessions — optionally "
            "filtered by faculty_id, date, or both."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "faculty_id": {
                    "type": "string",
                    "description": (
                        "The faculty member's ID to filter by.  "
                        "Omit to retrieve sessions for all faculty."
                    ),
                },
                "date": {
                    "type": "string",
                    "description": (
                        "An ISO date string YYYY-MM-DD to filter by.  "
                        "Omit to retrieve sessions across all dates."
                    ),
                },
            },
            # Neither field is strictly required — caller may supply both, one, or neither.
            "required": [],
        },
    },
}

# ---------------------------------------------------------------------------
# Tool 3: insert_session  — CREATE a new schedule row
# ---------------------------------------------------------------------------
insert_session_tool_schema = {
    "type": "function",
    "function": {
        "name": "insert_session",
        "description": (
            "Inserts a new session assignment into the Schedule table.  "
            "Use when the user wants to manually add or book a single "
            "faculty–batch session for a specific date."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "faculty_id": {
                    "type": "string",
                    "description": "The ID of the faculty member to assign.",
                },
                "batch_id": {
                    "type": "string",
                    "description": "The ID of the student batch.",
                },
                "session_alloc": {
                    "type": "number",
                    "description": (
                        "Fraction of a full session (0.25, 0.5, 0.75, or 1.0)."
                    ),
                },
                "session_role": {
                    "type": "string",
                    "description": "Role of the faculty: 'Educator' or 'Co-Educator'.",
                },
                "session_date": {
                    "type": "string",
                    "description": "Date of the session in YYYY-MM-DD format.",
                },
            },
            "required": [
                "faculty_id",
                "batch_id",
                "session_alloc",
                "session_role",
                "session_date",
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# Tool 4: update_session  — UPDATE an existing schedule row
# ---------------------------------------------------------------------------

update_session_tool_schema = {

    "type": "function",

    "function": {

        "name": "update_session",

        "description": (

            "Updates one or more fields on an existing schedule row identified "
            "by its session_id. Use when the user wants to update "
            "session taken, session left, status, allocation, faculty "
            "or date."

        ),

        "parameters": {

            "type": "object",

            "properties": {

                # =========================================================
                # SESSION ID
                # =========================================================

                "session_id": {

                    "type": "integer",

                    "description": (

                        "Primary key of session row."

                    ),

                },

                # =========================================================
                # FACULTY UPDATE
                # =========================================================

                "new_faculty_id": {

                    "type": "string",

                    "description": (

                        "New faculty ID."

                    ),

                },

                # =========================================================
                # DATE UPDATE
                # =========================================================

                "new_date": {

                    "type": "string",

                    "description": (

                        "New session date in YYYY-MM-DD format."

                    ),

                },

                # =========================================================
                # ALLOCATION UPDATE
                # =========================================================

                "new_alloc": {

                    "type": "number",

                    "description": (

                        "New allocated session value."

                    ),

                },

                # =========================================================
                # SESSION TAKEN
                # =========================================================

                "new_taken": {

                    "type": "number",

                    "description": (

                        "Amount of session completed/taken."

                    ),

                },

                # =========================================================
                # SESSION LEFT
                # =========================================================

                "new_left": {

                    "type": "number",

                    "description": (

                        "Remaining session left."

                    ),

                },

                # =========================================================
                # STATUS UPDATE
                # =========================================================

                "new_status": {

                    "type": "string",

                    "description": (

                        "Session status like "
                        "'Not Taken', "
                        "'Partial', "
                        "'Completed'."

                    ),

                },

            },

            # =============================================================
            # REQUIRED FIELD
            # =============================================================

            "required": [

                "session_id"

            ],

        },

    },

}
# ---------------------------------------------------------------------------
# Tool 5: delete_session  — DELETE a schedule row
# ---------------------------------------------------------------------------
delete_session_tool_schema = {
    "type": "function",
    "function": {
        "name": "delete_session",
        "description": (
            "Permanently deletes a schedule row by its schedule_id.  "
            "Use only when the user explicitly asks to remove or cancel a "
            "session record."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "integer",
                    "description": "The schedule_id to delete.",
                },
            },
            "required": ["session_id"],
        },
    },
}

# Collect all schemas into one list for easy passing to ollama.chat().
ALL_TOOLS = [
    schedule_tool_schema,
    get_sessions_tool_schema,
    insert_session_tool_schema,
    update_session_tool_schema,
    delete_session_tool_schema,
]

# ---------------------------------------------------------------------------
# Dispatch map  — maps function-name strings to actual Python callables.
# The agent loop uses this to avoid a long if/elif chain.
# ---------------------------------------------------------------------------
TOOL_DISPATCH = {
    "session_allocation": session_allocation,
    "get_sessions":       get_sessions,
    "insert_session":     insert_session,
    "update_session":     update_session,
    "delete_session":     delete_session,
}


# ===========================================================================
# AGENT LOOP
# ===========================================================================

def run_agent(user_prompt: str) -> None:
    """
    Runs a single user request through the Llama 3.1 agent until the model
    produces a final conversational answer (no more tool calls).

    The agent heartbeat:
    ─────────────────────────────────────────────────────────────────────────
    1. Build an initial messages list with the system prompt + user message.
    2. Call ollama.chat() with the messages + ALL_TOOLS.
    3. Append the model's reply to messages (keeps the full conversation
       context so the LLM can "remember" what it just did).
    4a. If the reply contains tool_calls:
          • Extract the function name and arguments from the call.
          • Look up the matching Python function in TOOL_DISPATCH.
          • Execute it, catching any exception so the agent never crashes.
          • Append a {'role': 'tool', 'content': <result_string>} message
            so the LLM can read the tool's output on the next iteration.
          • Continue the while loop (go back to step 2).
    4b. If no tool_calls:
          • The model has finished reasoning and produced its final reply.
          • Print it and break the loop.
    ─────────────────────────────────────────────────────────────────────────

    Parameters
    ----------
    user_prompt : str — The raw user request in plain English.
    """

    print(f"\nUser: {user_prompt}")
    print("Agent is thinking...\n")

    # ------------------------------------------------------------------
    # Build the initial message history.
    # The system prompt instructs the model to ALWAYS use tools for
    # scheduling tasks and never fabricate data.
    # ------------------------------------------------------------------
    messages = [
        {
            "role": "system",
            "content": (
                "You are a scheduling assistant with access to a faculty "
                "session scheduling system.  You MUST use the provided tools "
                "to answer any scheduling, viewing, inserting, updating, or "
                "deleting requests.  Never fabricate schedule data; always "
                "call a tool to read from or write to the database.  "
                "After receiving a tool result, summarise it clearly for the user."
            ),
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    # ------------------------------------------------------------------
    # Agent heartbeat — keeps running until the LLM gives a plain reply.
    # ------------------------------------------------------------------
    while True:
        # --- Step 2: ask the model ---
        response = ollama.chat(
            model="llama3.1",
            messages=messages,
            tools=ALL_TOOLS,
            options={"temperature": 0},   # deterministic output
        )

        ai_message = response["message"]

        # --- Step 3: add the model's reply to history ---
        # This is essential: without this the LLM forgets what it just said.
        messages.append(ai_message)

        # --- Step 4a: handle tool calls ---
        if ai_message.get("tool_calls"):
            for tool_call in ai_message["tool_calls"]:
                fn_name = tool_call["function"]["name"]
                fn_args = tool_call["function"].get("arguments", {})

                print(f"[Tool call] {fn_name}({fn_args})")

                # Look up the Python function; gracefully handle an unknown name.
                fn = TOOL_DISPATCH.get(fn_name)
                if fn is None:
                    tool_output = (
                        f"Error: The tool '{fn_name}' is not registered.  "
                        "Please try a different approach."
                    )
                else:
                    try:
                        # Unpack the dict of arguments as keyword arguments.
                        # e.g. fn_args = {"session_date": "2025-08-01"}
                        # becomes session_allocation(session_date="2025-08-01")
                        result = fn(**fn_args)
                        tool_output = str(result)
                    except TypeError as e:
                        # Wrong argument names / missing required args.
                        tool_output = f"Tool argument error for '{fn_name}': {e}"
                    except Exception as e:
                        # Any other runtime error from the tool itself.
                        tool_output = f"Tool execution error for '{fn_name}': {e}"

                print(f"[Tool result] {tool_output[:200]}{'...' if len(tool_output) > 200 else ''}\n")

                # Feed the result back into the conversation so the LLM can
                # read it on the next iteration.
                messages.append({
                    "role": "tool",
                    "content": tool_output,
                })

            # After processing all tool calls, loop back to let the model
            # read the tool output and decide what to do next.
            continue

        # --- Step 4b: no tool call → final conversational reply ---
        #print(f"Agent: {ai_message['content']}")
        #break   # exit the heartbeat loop
        return ai_message["content"]


# ===========================================================================
# Entry point
# ===========================================================================

if __name__ == "__main__":
    print("=== Faculty Scheduling Agent ===")
    print("Type your request below (e.g. 'Schedule all batches for 2025-08-15').")
    print("Press Ctrl+C to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input:
                run_agent(user_input)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
