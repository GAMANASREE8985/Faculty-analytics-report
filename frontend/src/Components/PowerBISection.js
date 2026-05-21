import React from "react";

function PowerBISection() {

  // =========================
  // GET EMPLOYEE ID
  // =========================

  const employeeId =
    localStorage.getItem("emp_id");

  // =========================
  // POWER BI URL
  // =========================

  const powerBIURL =
    "https://app.powerbi.com/reportEmbed?reportId=31bcf4d8-5acb-432d-aef1-951fd41b51be&autoAuth=true&ctid=808cc83e-a546-47e7-a03f-73a1ebba24f3";

  // =========================
  // FILTERED URL
  // =========================

  const filteredURL =
    `${powerBIURL}&filter=employees/emp_id eq ${employeeId}`;

  // =========================
  // UI
  // =========================

  return (

    <div
      style={{
        padding: "30px",
        background: "#f3f4f6",
        minHeight: "100vh"
      }}
    >

      {/* HEADER */}

      <h1
        style={{
          fontSize: "34px",
          fontWeight: "700",
          marginBottom: "15px",
          color: "#111827"
        }}
      >

        Power BI Dashboard

      </h1>

      <p
        style={{
          fontSize: "16px",
          color: "#6b7280",
          marginBottom: "30px"
        }}
      >

        View complete HR and Faculty Analytics dashboards.

      </p>

      {/* CARD */}

      <div
        style={{
          background: "#ffffff",
          padding: "30px",
          borderRadius: "20px",
          boxShadow:
            "0 4px 14px rgba(0,0,0,0.08)"
        }}
      >

        {/* TITLE */}

        <h2
          style={{
            marginBottom: "20px",
            color: "#111827"
          }}
        >

          Employee Analytics Dashboard

        </h2>

        {/* EMPLOYEE INFO */}

        <p
          style={{
            marginBottom: "20px",
            color: "#374151",
            fontWeight: "600"
          }}
        >

          Logged in Employee ID:
          {" "}
          {employeeId}

        </p>

        {/* POWER BI IFRAME */}

        <iframe

          title="PowerBI"

          width="100%"

          height="750"

          src={filteredURL}

          frameBorder="0"

          allowFullScreen={true}

          style={{
            borderRadius: "12px",
            border: "1px solid #d1d5db"
          }}

        />

      </div>

    </div>

  );

}

export default PowerBISection;