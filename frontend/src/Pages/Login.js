import React, { useState } from "react";

import { useNavigate } from "react-router-dom";

import "./Login.css";

function Login() {

  const navigate = useNavigate();

  const [empId, setEmpId] = useState("");

  const [password, setPassword] = useState("");

  // LOGIN FUNCTION

  const handleLogin = async () => {

    try {

      const response = await fetch(
        `https://faculty-backed.onrender.com/login/${empId}/${password}`
      );

      const data = await response.json();

      if (data.status === "success") {

        localStorage.setItem(
          "emp_id",
          data.employee.emp_id
        );

        localStorage.setItem(
          "role",
          data.role
        );

        if (data.role === "hr") {

          navigate("/hr");

        } else {

          navigate("/employee");

        }

      } else {

        alert(data.message);

      }

    } catch (error) {

      console.log(error);

      alert("Backend Connection Error");

    }

  };

  return (

    <div className="login-container">

      {/* NAVBAR */}

      <div className="navbar">

        <h2>Faculty Analytics Portal</h2>

        <div className="nav-links">

          <span>Home</span>
          <span>Dashboard</span>
          <span>Analytics</span>
          <span>Reports</span>

        </div>

      </div>

      {/* MAIN SECTION */}

      <div className="main-section">

        {/* LEFT CONTENT */}

        <div className="left-content">

          <h1>
            Faculty Analytics Dashboard
          </h1>

          <p>
            HR Analytics • Session Management •
            Power BI • Employee Performance •
            Batch Tracking
          </p>

          <div className="feature-grid">

            <div className="feature-card">
              📊 Real-Time Analytics
            </div>

            <div className="feature-card">
              👨‍🏫 Employee Role Management
            </div>

            <div className="feature-card">
              📚 Session Allocation Tracking
            </div>

            <div className="feature-card">
              ⚡ Power BI Integration
            </div>

          </div>

        </div>

        {/* LOGIN CARD */}

        <div className="login-box">

          <h1>Login</h1>

          <p>Access your dashboard</p>

          <input
            type="text"
            placeholder="Employee ID"
            value={empId}
            onChange={(e) =>
              setEmpId(e.target.value)
            }
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
          />

          <button onClick={handleLogin}>
            Login
          </button>

          <div className="demo-box">

            <h4>Demo Credentials</h4>

            <p>HR → 101 / 2024-01-01</p>

            <p>
              Employee → 103 / 2024-03-01
            </p>

          </div>

        </div>

      </div>

    </div>

  );
}

export default Login;