import React from "react";

function RolesSection({ roles }) {

  return (

    <div
      style={{
        background: "#ffffff",
        padding: "25px",
        borderRadius: "20px",
        boxShadow:
          "0 4px 14px rgba(0,0,0,0.08)",
        marginTop: "30px"
      }}
    >

      {/* HEADER */}

      <h2
        style={{
          fontSize: "28px",
          fontWeight: "700",
          marginBottom: "25px",
          color: "#111827"
        }}
      >
        Employee Roles
      </h2>

      {/* ROLE GRID */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "20px"
        }}
      >

        {
          roles.map((role, index) => (

            <div

              key={index}

              style={{
                background:
                  "linear-gradient(135deg, #2563eb, #1d4ed8)",

                color: "#fff",

                padding: "20px",

                borderRadius: "16px",

                boxShadow:
                  "0 4px 12px rgba(0,0,0,0.12)",

                transition: "0.3s"
              }}
            >

              <h3
                style={{
                  fontSize: "20px",
                  marginBottom: "10px"
                }}
              >
                {role.position}
              </h3>

              <p
                style={{
                  fontSize: "14px",
                  opacity: 0.9
                }}
              >
                Faculty ID :
                {role.faculty_id}
              </p>

            </div>

          ))
        }

      </div>

    </div>
  );
}

export default RolesSection;