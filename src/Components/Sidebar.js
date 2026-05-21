import React from "react";

function Sidebar({ setActiveSection }) {

  return (

    <div className="employee-sidebar">

      <h2>Faculty Portal</h2>

      <ul>

        {/* Dashboard */}
        <li
          onClick={() =>
            setActiveSection("dashboard")
          }
        >
          📊 Dashboard
        </li>

        {/* Scheduler Bot */}
        <li
          onClick={() =>
            setActiveSection("schedulerbot")
          }
        >
          🤖 Scheduler Bot
        </li>

        {/* Power BI */}
        <li
          onClick={() =>
            setActiveSection("powerbi")
          }
        >
          📈 Power BI
        </li>

      </ul>

    </div>
  );
}

export default Sidebar;