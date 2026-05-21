import React from "react";

function DashboardSection({
  employeeData
}) {

  const emp =
    employeeData.employee?.[0] || {};

  const totalSessions =
    employeeData.sessions?.length || 0;

  const completedSessions =
    employeeData.sessions?.filter(
      (s) =>
        s.session_status ===
        "Completed"
    ).length || 0;

  const pendingSessions =
    employeeData.sessions?.filter(
      (s) =>
        s.session_status ===
        "Not Taken"
    ).length || 0;

  const partialSessions =
    employeeData.sessions?.filter(
      (s) =>
        s.session_status ===
        "Partial"
    ).length || 0;

  const artifactCount =
    employeeData.artifacts?.length || 0;

  const analyticsCards = [

    {
      title: "Total Sessions",
      value: totalSessions,
      icon: "📚"
    },

    {
      title: "Completed",
      value: completedSessions,
      icon: "✅"
    },

    {
      title: "Pending",
      value: pendingSessions,
      icon: "⏳"
    },

    {
      title: "Partial",
      value: partialSessions,
      icon: "🟡"
    },

    {
      title: "Artifacts",
      value: artifactCount,
      icon: "📊"
    }

  ];

  return (

    <div className="dashboard-wrapper">

      {/* ANALYTICS */}

      <div className="analytics-cards">

        {
          analyticsCards.map(
            (card, index) => (

              <div
                className="analytics-card"
                key={index}
              >

                <div className="card-icon">
                  {card.icon}
                </div>

                <h3>{card.title}</h3>

                <h1>{card.value}</h1>

              </div>

            )
          )
        }

      </div>

      {/* PROFILE */}

      <div className="profile-card">

        <div className="profile-left">

          <div className="profile-avatar">

            {emp.name?.charAt(0)}

          </div>

          <div>

            <h2>{emp.name}</h2>

            <p>Faculty Member</p>

          </div>

        </div>

      </div>

    </div>
  );
}

export default DashboardSection;