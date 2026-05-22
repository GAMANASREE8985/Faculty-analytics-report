import React, { useState } from "react";

function SchedulerBot() {

  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");

  // =====================================
  // SEND MESSAGE
  // =====================================

  const sendMessage = async () => {

    if (!message.trim()) return;

    try {

      const response = await fetch(
        "https://faculty-backed.onrender.com/chatbot",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            message: message
          })
        }
      );

      const data = await response.json();

      setReply(data.reply);

    } catch (error) {

      setReply(
        "Server connection failed"
      );

    }

  };

  // =====================================
  // UI
  // =====================================

  return (

    <div
      style={{
        width: "92%",
        margin: "30px auto",
        background: "#ffffff",
        borderRadius: "20px",
        overflow: "hidden",
        boxShadow:
          "0 4px 20px rgba(0,0,0,0.08)"
      }}
    >

      {/* HEADER */}

      <div
        style={{
          background:
            "linear-gradient(to right, #1d4ed8, #2563eb)",

          color: "white",

          padding: "25px 35px",

          display: "flex",

          justifyContent:
            "space-between",

          alignItems: "center"
        }}
      >

        <h2
          style={{
            margin: 0,
            fontSize: "38px",
            fontWeight: "700"
          }}
        >
          🤖 Smart Coordinator Assistant
        </h2>

        <p
          style={{
            margin: 0,
            fontSize: "16px"
          }}
        >
          AI Powered Scheduling &
          Faculty Support System
        </p>

      </div>

      {/* INPUT SECTION */}

      <div
        style={{
          display: "flex",
          gap: "20px",
          padding: "30px"
        }}
      >

        <input
          type="text"

          value={message}

          onChange={(e) =>
            setMessage(
              e.target.value
            )
          }

          placeholder="
Ask AI assistant..."

          style={{
            flex: 1,

            height: "60px",

            padding: "0 20px",

            border:
              "1px solid #cbd5e1",

            borderRadius: "14px",

            fontSize: "18px",

            outline: "none",

            background: "#f8fafc"
          }}
        />

        <button
          onClick={sendMessage}

          style={{
            height: "60px",

            padding: "0 35px",

            border: "none",

            borderRadius: "14px",

            background: "#2563eb",

            color: "white",

            fontSize: "18px",

            fontWeight: "600",

            cursor: "pointer"
          }}
        >
          Send
        </button>

      </div>

      {/* RESPONSE */}

      {
        reply && (

          <div
            style={{
              margin:
                "0 30px 30px",

              padding: "25px",

              borderRadius: "16px",

              background: "#f1f5f9"
            }}
          >

            <h3
              style={{
                marginBottom: "10px",
                color: "#0f172a"
              }}
            >
              AI Response
            </h3>

            <p
              style={{
                color: "#334155",
                fontSize: "17px",
                lineHeight: "1.7"
              }}
            >
              {reply}
            </p>

          </div>

        )
      }

    </div>

  );
}

export default SchedulerBot;
