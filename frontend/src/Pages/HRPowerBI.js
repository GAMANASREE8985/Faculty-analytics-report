import React, { useEffect, useState } from "react";

import HRSidebar from "../Components/HRSidebar";

import "./HRDashboard.css";

function HRPowerBI({ setShowPowerBI }) {

  // =========================
  // STATES
  // =========================

  const [facultyIds, setFacultyIds] = useState([]);

  const [facultyId, setFacultyId] = useState("");

  const [positions, setPositions] = useState([]);

  const [activeDashboard, setActiveDashboard] =
    useState("faculty");

  // =========================
  // FETCH FACULTY IDS
  // =========================

  useEffect(() => {

    fetch("https://faculty-backed.onrender.com/faculty-ids")

      .then((res) => res.json())

      .then((data) => {

        setFacultyIds(data);

      })

      .catch((err) => {

        console.log(err);

      });

  }, []);

  // =========================
  // FETCH FACULTY DETAILS
  // =========================

  const handleFacultyChange = (value) => {

    setFacultyId(value);

    if (!value) {

      setPositions([]);

      return;

    }

    fetch(
      `https://faculty-backed.onrender.com/faculty-details/${value}`
    )

      .then((res) => res.json())

      .then((data) => {

        setPositions(data.positions || []);

      })

      .catch((err) => {

        console.log(err);

      });

  };

  // =========================
  // POWER BI LINKS
  // =========================

  // FACULTY DASHBOARD

  const facultyDashboardURL =
    "https://app.powerbi.com/reportEmbed?reportId=972cafa4-1885-4022-9c19-cacfc373c5a4&autoAuth=true&ctid=808cc83e-a546-47e7-a03f-73a1ebba24f3";

  // BATCH OWNER DASHBOARD

  const batchDashboardURL =
    "https://app.powerbi.com/reportEmbed?reportId=5b745f7e-8497-4495-b1ec-89d2a44226ee&autoAuth=true&ctid=808cc83e-a546-47e7-a03f-73a1ebba24f3";

  // =========================
  // DYNAMIC FILTER URL
  // =========================

  const filteredPowerBIUrl =

    activeDashboard === "faculty"

      ? `${facultyDashboardURL}&filter=schedules/faculty_id eq ${facultyId}`

      : `${batchDashboardURL}&filter=batches/batch_owner eq ${facultyId}`;

  // =========================
  // UI
  // =========================

  return (

    <div className="dashboard-container">

      {/* SIDEBAR */}

      <HRSidebar
        setShowPowerBI={setShowPowerBI}
      />

      {/* MAIN CONTENT */}

      <div className="main-content">

        {/* TOP BAR */}

        <div className="top-bar">

          <h1>
            HR Power BI Analytics Dashboard
          </h1>

        </div>

        {/* POWER BI CARD */}

        <div className="powerbi-wrapper">

          <div
            className="powerbi-card"
            style={{
              width: "100%",
              padding: "25px",
              background: "#ffffff",
              borderRadius: "15px",
              boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
            }}
          >

            {/* TITLE */}

            <h2
              style={{
                textAlign: "center",
                marginBottom: "20px",
                color: "#1f2937"
              }}
            >
              Faculty & Batch Analytics Dashboard
            </h2>

            {/* DROPDOWN */}

            <div
              style={{
                display: "flex",
                justifyContent: "center",
                marginBottom: "20px"
              }}
            >

              <select
                value={facultyId}
                onChange={(e) =>
                  handleFacultyChange(
                    e.target.value
                  )
                }
                style={{
                  padding: "12px",
                  width: "260px",
                  borderRadius: "8px",
                  border: "1px solid #d1d5db",
                  fontSize: "15px",
                  outline: "none"
                }}
              >

                <option value="">
                  Select Faculty ID
                </option>

                {

                  facultyIds.map((id) => (

                    <option
                      key={id}
                      value={id}
                    >

                      {id}

                    </option>

                  ))

                }

              </select>

            </div>

            {/* POSITION DISPLAY */}

            {

              facultyId && (

                <div
                  style={{
                    textAlign: "center",
                    marginBottom: "20px",
                    fontSize: "16px",
                    fontWeight: "600",
                    color: "#374151"
                  }}
                >

                  Positions:
                  {" "}

                  {

                    positions.length > 0

                      ? positions.join(", ")

                      : "No Position Found"

                  }

                </div>

              )

            }

            {/* DASHBOARD BUTTONS */}

            <div
              style={{
                display: "flex",
                justifyContent: "center",
                gap: "20px",
                marginBottom: "25px",
                flexWrap: "wrap"
              }}
            >

              {/* FACULTY BUTTON */}

              {

                positions.includes("Faculty") && (

                  <button

                    onClick={() =>
                      setActiveDashboard("faculty")
                    }

                    style={{
                      padding: "12px 20px",
                      background: "#2563eb",
                      color: "#ffffff",
                      border: "none",
                      borderRadius: "8px",
                      fontWeight: "600",
                      cursor: "pointer"
                    }}
                  >

                    Faculty Dashboard

                  </button>

                )

              }

              {/* BATCH OWNER BUTTON */}

              {

                positions.includes("Batch Owner") && (

                  <button

                    onClick={() =>
                      setActiveDashboard("batch")
                    }

                    style={{
                      padding: "12px 20px",
                      background: "#059669",
                      color: "#ffffff",
                      border: "none",
                      borderRadius: "8px",
                      fontWeight: "600",
                      cursor: "pointer"
                    }}
                  >

                    Batch Owner Dashboard

                  </button>

                )

              }

            </div>

            {/* POWER BI IFRAME */}

            {

              facultyId && (

                <iframe
                  title="PowerBI"
                  width="100%"
                  height="750"

                  src={filteredPowerBIUrl}

                  frameBorder="0"

                  allowFullScreen={true}

                  style={{
                    borderRadius: "12px",
                    border: "1px solid #d1d5db"
                  }}
                />

              )

            }

          </div>

        </div>

      </div>

    </div>

  );

}

export default HRPowerBI;