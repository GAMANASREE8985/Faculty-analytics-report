import React from "react";

function Topbar({
  emp,
  handleLogout
}) {

  return (

    <div className="employee-topbar">

      <h1>
        Employee Dashboard
      </h1>

      <div className="topbar-right">

        <button className="profile-btn">

          {emp.name}

        </button>

        <button
          className="logout-btn"
          onClick={handleLogout}
        >

          Logout

        </button>

      </div>

    </div>

  );
}

export default Topbar;