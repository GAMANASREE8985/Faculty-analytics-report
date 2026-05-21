import React from "react";

function HRSidebar({
  setShowPowerBI,
  setShowOverallAnalytics
}) {

  return (

    <div className="sidebar">

      <h2>
        HR Panel
      </h2>

      <ul>

        {/* HR DASHBOARD */}

        <li

          onClick={() => {

            if (setShowPowerBI) {

              setShowPowerBI(false);

            }

            if (setShowOverallAnalytics) {

              setShowOverallAnalytics(false);

            }

          }}

        >

          🏠 HR Dashboard

        </li>

        {/* OVERALL ANALYTICS */}

        <li

          onClick={() => {

            if (setShowOverallAnalytics) {

              setShowOverallAnalytics(true);

            }

            if (setShowPowerBI) {

              setShowPowerBI(false);

            }

          }}

          className="powerbi-btn"

        >

          📈 Overall Analytics

        </li>

        {/* POWER BI */}

        <li

          onClick={() => {

            if (setShowPowerBI) {

              setShowPowerBI(true);

            }

            if (setShowOverallAnalytics) {

              setShowOverallAnalytics(false);

            }

          }}

          className="powerbi-btn"

        >

          📊 Power BI Dashboard

        </li>

        {/* LOGOUT */}

       <li

  className="logout-btn"

  onClick={() => {

    // CLEAR STORAGE

    localStorage.clear();

    sessionStorage.clear();

    // REDIRECT LOGIN PAGE

    window.location.href = "/";

  }}

>

  🚪 Logout

</li>
      </ul>

    </div>

  );

}

export default HRSidebar;