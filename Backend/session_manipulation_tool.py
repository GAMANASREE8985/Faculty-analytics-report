"""
session_manipulation_tool.py
----------------------------

CRUD operations for AI scheduling bot.

AI Agent Uses:
---------------
1. get_sessions()
2. insert_session()
3. update_session()
4. delete_session()

Works with:
------------
- Ollama tool calling
- Flask backend
- SQLite database
"""

import sqlite3


# =========================================================
# DATABASE PATH
# =========================================================

DB_PATH = "schedule.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def _get_connection():

    """
    Creates SQLite connection.
    """

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# GET SESSIONS
# =========================================================

def get_sessions(
    faculty_id=None,
    date=None
):

    """
    Fetch sessions from database.

    Optional Filters:
    -----------------
    faculty_id
    date
    """

    conditions = []

    params = []

    # =====================================================
    # FILTER BY FACULTY ID
    # =====================================================

    if faculty_id is not None:

        conditions.append(
            "faculty_id = ?"
        )

        params.append(
            str(faculty_id)
        )

    # =====================================================
    # FILTER BY DATE
    # =====================================================

    if date is not None:

        conditions.append(
            "session_date = ?"
        )

        params.append(date)

    # =====================================================
    # CREATE WHERE CLAUSE
    # =====================================================

    where_clause = (

        "WHERE " + " AND ".join(conditions)

    ) if conditions else ""

    # =====================================================
    # QUERY
    # =====================================================

    query = f"""

    SELECT *
    FROM schedules

    {where_clause}

    """

    try:

        with _get_connection() as conn:

            cursor = conn.execute(

                query,
                params

            )

            rows = cursor.fetchall()

        # =================================================
        # EMPTY RESULT
        # =================================================

        if not rows:

            return []

        # =================================================
        # CONVERT ROWS TO DICTIONARY
        # =================================================

        return [

            dict(row)

            for row in rows

        ]

    except sqlite3.Error as e:

        return f"Database error in get_sessions: {e}"


# =========================================================
# INSERT SESSION
# =========================================================

def insert_session(

    faculty_id,
    batch_id,
    session_alloc,
    session_role,
    session_date

):

    """
    Insert new session.
    """

    query = """

    INSERT INTO schedules (

        faculty_id,
        batch_id,
        session_alloc,
        session_role,
        session_date,
        status

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """

    params = (

        str(faculty_id),

        str(batch_id),

        float(session_alloc),

        session_role,

        session_date,

        "Scheduled"

    )

    try:

        with _get_connection() as conn:

            cursor = conn.execute(

                query,
                params

            )

            conn.commit()

            new_id = cursor.lastrowid

        return (

            f"Success: "

            f"Inserted session_id={new_id}"

        )

    except sqlite3.Error as e:

        return f"Database error in insert_session: {e}"


# =========================================================
# UPDATE SESSION
# =========================================================
# =========================================================
# UPDATE SESSION
# =========================================================

def update_session(

    session_id,

    new_faculty_id=None,

    new_date=None,

    new_alloc=None,

    new_taken=None,

    new_left=None,

    new_status=None

):

    """
    Update existing session.
    """

    set_parts = []

    params = []

    # =====================================================
    # UPDATE FACULTY ID
    # =====================================================

    if new_faculty_id not in [None, "None"]:

        set_parts.append(
            "faculty_id = ?"
        )

        params.append(
            str(new_faculty_id)
        )

    # =====================================================
    # UPDATE DATE
    # =====================================================

    if new_date not in [None, "None"]:

        set_parts.append(
            "session_date = ?"
        )

        params.append(new_date)

    # =====================================================
    # UPDATE SESSION ALLOCATED
    # =====================================================

    if new_alloc not in [None, "None"]:

        set_parts.append(
            "session_alloc = ?"
        )

        params.append(
            float(new_alloc)
        )

    # =====================================================
    # UPDATE SESSION TAKEN
    # =====================================================

    if new_taken not in [None, "None"]:

        set_parts.append(
            "session_taken = ?"
        )

        params.append(
            float(new_taken)
        )

    # =====================================================
    # UPDATE SESSION LEFT
    # =====================================================

    if new_left not in [None, "None"]:

        set_parts.append(
            "session_left = ?"
        )

        params.append(
            float(new_left)
        )

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    if new_status not in [None, "None"]:

        set_parts.append(
            "session_status = ?"
        )

        params.append(new_status)

    # =====================================================
    # NO FIELDS
    # =====================================================

    if not set_parts:

        return "No fields to update."

    params.append(session_id)

    # =====================================================
    # UPDATE QUERY
    # =====================================================

    query = f"""

    UPDATE schedules

    SET {", ".join(set_parts)}

    WHERE session_id = ?

    """

    try:

        with _get_connection() as conn:

            cursor = conn.execute(

                query,
                params

            )

            conn.commit()

            if cursor.rowcount == 0:

                return (

                    f"No row found "

                    f"with session_id={session_id}"

                )

        return (

            f"Success: "

            f"Updated session_id={session_id}"

        )

    except sqlite3.Error as e:

        return f"Database error in update_session: {e}"

# =========================================================
# DELETE SESSION
# =========================================================

def delete_session(session_id):

    """
    Delete session from database.
    """

    query = """

    DELETE FROM schedules

    WHERE session_id = ?

    """

    try:

        with _get_connection() as conn:

            cursor = conn.execute(

                query,
                (session_id,)

            )

            conn.commit()

            if cursor.rowcount == 0:

                return (

                    f"No row found "

                    f"with session_id={session_id}"

                )

        return (

            f"Success: "

            f"Deleted session_id={session_id}"

        )

    except sqlite3.Error as e:

        return f"Database error in delete_session: {e}"


# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    print(

        get_sessions(
            faculty_id=1001
        )

    )