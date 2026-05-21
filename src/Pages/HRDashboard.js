import React, {
  useEffect,
  useState
} from "react";

import axios from "axios";

import HRSidebar
from "../Components/HRSidebar";

import HRTopbar
from "../Components/HRTopbar";

import HRPowerBI
from "./HRPowerBI";

import "./HRDashboard.css";

function HRDashboard() {

  // =========================
  // STATES
  // =========================

  const [
    dashboardData,
    setDashboardData
  ] = useState(null);

  const [
    showPowerBI,
    setShowPowerBI
  ] = useState(false);

  const [
    showOverallAnalytics,
    setShowOverallAnalytics
  ] = useState(false);

  // =========================
  // FETCH DATA
  // =========================

  useEffect(() => {

    axios

      .get(
        "https://faculty-backed.onrender.com/hr-dashboard"
      )

      .then((response) => {

        setDashboardData(
          response.data
        );

      })

      .catch((error) => {

        console.log(error);

      });

  }, []);

  // =========================
  // LOADING
  // =========================

  if (!dashboardData) {

    return <h1>Loading...</h1>;

  }

  // =========================
  // SESSION COUNTS
  // =========================

  const completedSessions =

    dashboardData.sessions.filter(

      (s) =>
        s.session_status === "Completed"

    ).length;

  const inProgressSessions =

    dashboardData.sessions.filter(

      (s) =>
        s.session_status === "Partial"

    ).length;

  const pendingSessions =

    dashboardData.sessions.filter(

      (s) =>
        s.session_status === "Cancelled"

    ).length;

  // =========================
  // POWER BI PAGE
  // =========================

  if (showPowerBI) {

    return (

      <HRPowerBI
        setShowPowerBI={
          setShowPowerBI
        }
      />

    );

  }

  // =========================
  // OVERALL ANALYTICS PAGE
  // =========================

  if (showOverallAnalytics) {

    return (

      <div className="dashboard-container">

        {/* SIDEBAR */}

        <HRSidebar
          setShowPowerBI={
            setShowPowerBI
          }

          setShowOverallAnalytics={
            setShowOverallAnalytics
          }
        />

        {/* MAIN */}

        <div className="main-content">

          <HRTopbar />

          <div
            style={{
              padding: "20px"
            }}
          >

            <h1
              style={{
                marginBottom: "20px",
                color: "#111827"
              }}
            >

              Overall HR Analytics

            </h1>

            <iframe

              title="Overall Analytics"

              width="100%"

              height="750"

              src="https://app.powerbi.com/view?r=eyJrIjoiZDVkZTY3MWMtYzYxNS00ZjNjLTgwYTItZTg0ZjFiYjFlMzYxIiwidCI6IjgwOGNjODNlLWE1NDYtNDdlNy1hMDNmLTczYTFlYmJhMjRmMyIsImMiOjEwfQ%3D%3D"

              frameBorder="0"

              allowFullScreen={true}

              style={{
                borderRadius: "12px",
                border: "1px solid #d1d5db"
              }}

            />

          </div>

        </div>

      </div>

    );

  }

  // =========================
  // MAIN HR DASHBOARD
  // =========================

  return (

    <div className="dashboard-container">

      {/* SIDEBAR */}

      <HRSidebar

        setShowPowerBI={
          setShowPowerBI
        }

        setShowOverallAnalytics={
          setShowOverallAnalytics
        }

      />

      {/* MAIN */}

      <div className="main-content">

        <HRTopbar />

        {/* CARDS */}

        <div className="cards">

          <div className="card">

            <h4>
              Total Employees
            </h4>

            <h2>

              {
                dashboardData
                  .total_employees
              }

            </h2>

          </div>

          <div className="card">

            <h4>
              Total Sessions
            </h4>

            <h2>

              {
                dashboardData
                  .total_sessions
              }

            </h2>

          </div>

          <div className="card">

            <h4>
              Completed
            </h4>

            <h2>

              {completedSessions}

            </h2>

          </div>

        </div>

        {/* STATUS */}

        <div className="chart-card">

          <h3>
            Session Status
          </h3>

          <div className="status-box green">

            Complete :
            {" "}
            {completedSessions}

          </div>

          <div className="status-box blue">

            Partial:
            {" "}
            {inProgressSessions}

          </div>

          <div className="status-box red">

            Cancelled :
            {" "}
            {pendingSessions}

          </div>

        </div>

      </div>

    </div>

  );

}

export default HRDashboard;