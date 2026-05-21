import React from "react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";

function AnalyticsSection({ employeeData }) {

  // ============================================
  // ALL SESSIONS DATA
  // ============================================

  const sessions =
    employeeData.sessions || [];

  // ============================================
  // SESSION HOURS DATA
  // ============================================

  const totalAllocated =
    sessions.reduce(
      (a, b) =>
        a +
        Number(
          b.session_alloc || 0
        ),
      0
    );

  const totalTaken =
    sessions.reduce(
      (a, b) =>
        a +
        Number(
          b.session_taken || 0
        ),
      0
    );

  const totalLeft =
    sessions.reduce(
      (a, b) =>
        a +
        Number(
          b.session_left || 0
        ),
      0
    );

  // ============================================
  // BAR CHART DATA
  // ============================================

  const sessionChart = [

    {
      name: "Allocated",
      value: totalAllocated
    },

    {
      name: "Taken",
      value: totalTaken
    },

    {
      name: "Left",
      value: totalLeft
    }

  ];

  // ============================================
  // STATUS DATA
  // ============================================

  const completedCount =
    sessions.filter(
      (s) =>
        s.session_status ===
        "Completed"
    ).length;

  const pendingCount =
    sessions.filter(
      (s) =>
        s.session_status ===
        "Pending"
    ).length;

  const partialCount =
    sessions.filter(
      (s) =>
        s.session_status ===
        "Partial"
    ).length;

  // ============================================
  // PIE CHART DATA
  // ============================================

  const statusChart = [

    {
      name: "Completed",
      value: completedCount
    },

    {
      name: "Pending",
      value: pendingCount
    },

    {
      name: "Partial",
      value: partialCount
    }

  ];

  // ============================================
  // COLORS
  // ============================================

  const COLORS = [
    "#2563eb",
    "#14b8a6",
    "#f59e0b"
  ];

  // ============================================
  // UI
  // ============================================

  return (

    <div
      style={{
        padding: "25px",
        background: "#f3f4f6",
        minHeight: "100vh"
      }}
    >

      {/* HEADER */}

      <div
        style={{
          marginBottom: "30px"
        }}
      >

        <h1
          style={{
            fontSize: "34px",
            fontWeight: "700",
            color: "#111827",
            marginBottom: "10px"
          }}
        >
          Faculty Analytics Dashboard
        </h1>

        <p
          style={{
            fontSize: "16px",
            color: "#6b7280"
          }}
        >
          Monitor faculty session performance and analytics.
        </p>

      </div>

      {/* SUMMARY CARDS */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(250px, 1fr))",
          gap: "25px",
          marginBottom: "35px"
        }}
      >

        {/* ALLOCATED */}

        <div
          style={{
            background: "#2563eb",
            color: "#fff",
            padding: "30px",
            borderRadius: "18px",
            boxShadow:
              "0 4px 14px rgba(0,0,0,0.08)"
          }}
        >

          <h3
            style={{
              marginBottom: "15px",
              fontSize: "20px"
            }}
          >
            Allocated Hours
          </h3>

          <h1
            style={{
              fontSize: "42px",
              fontWeight: "700"
            }}
          >
            {totalAllocated.toFixed(2)}
          </h1>

        </div>

        {/* TAKEN */}

        <div
          style={{
            background: "#14b8a6",
            color: "#fff",
            padding: "30px",
            borderRadius: "18px",
            boxShadow:
              "0 4px 14px rgba(0,0,0,0.08)"
          }}
        >

          <h3
            style={{
              marginBottom: "15px",
              fontSize: "20px"
            }}
          >
            Taken Hours
          </h3>

          <h1
            style={{
              fontSize: "42px",
              fontWeight: "700"
            }}
          >
            {totalTaken.toFixed(2)}
          </h1>

        </div>

        {/* LEFT */}

        <div
          style={{
            background: "#f59e0b",
            color: "#fff",
            padding: "30px",
            borderRadius: "18px",
            boxShadow:
              "0 4px 14px rgba(0,0,0,0.08)"
          }}
        >

          <h3
            style={{
              marginBottom: "15px",
              fontSize: "20px"
            }}
          >
            Remaining Hours
          </h3>

          <h1
            style={{
              fontSize: "42px",
              fontWeight: "700"
            }}
          >
            {totalLeft.toFixed(2)}
          </h1>

        </div>

      </div>

      {/* CHART SECTION */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(550px, 1fr))",
          gap: "30px"
        }}
      >

        {/* BAR CHART */}

        <div
          style={{
            background: "#fff",
            borderRadius: "20px",
            padding: "25px",
            boxShadow:
              "0 4px 14px rgba(0,0,0,0.08)"
          }}
        >

          <h2
            style={{
              fontSize: "26px",
              marginBottom: "20px",
              color: "#111827"
            }}
          >
            Session Hours Analytics
          </h2>

          <ResponsiveContainer
            width="100%"
            height={350}
          >

            <BarChart
              data={sessionChart}
            >

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey="name"
              />

              <YAxis />

              <Tooltip />

              <Bar
                dataKey="value"
                fill="#2563eb"
                radius={[
                  10,
                  10,
                  0,
                  0
                ]}
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

        {/* PIE CHART */}

        <div
          style={{
            background: "#fff",
            borderRadius: "20px",
            padding: "25px",
            boxShadow:
              "0 4px 14px rgba(0,0,0,0.08)"
          }}
        >

          <h2
            style={{
              fontSize: "26px",
              marginBottom: "20px",
              color: "#111827"
            }}
          >
            Session Status Analytics
          </h2>

          <ResponsiveContainer
            width="100%"
            height={350}
          >

            <PieChart>

              <Pie
                data={statusChart}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="45%"
                outerRadius={120}
                label
              >

                {
                  statusChart.map(
                    (
                      entry,
                      index
                    ) => (

                      <Cell
                        key={`cell-${index}`}
                        fill={
                          COLORS[index]
                        }
                      />

                    )
                  )
                }

              </Pie>

              <Tooltip />

              <Legend />

            </PieChart>

          </ResponsiveContainer>

        </div>

      </div>

    </div>
  );
}

export default AnalyticsSection;