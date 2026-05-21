import React, { useEffect, useState } from "react";

import axios from "axios";

import Sidebar from "../Components/Sidebar";
import Topbar from "../Components/Topbar";
import PowerBISection from "../Components/PowerBISection";
import DashboardSection from "../Components/DashboardSection";

import SchedulerBot from "../Components/SchedulerBot";

import "../styles/EmployeeDashboard.css";

function EmployeeDashboard() {

  const [employeeData, setEmployeeData] =
    useState(null);

  const [activeSection, setActiveSection] =
    useState("dashboard");

  // ============================================
  // API CALL
  // ============================================

  useEffect(() => {

    const empId =
      localStorage.getItem("emp_id");

    axios
      .get(
        `https://faculty-backed.onrender.com/employee-dashboard/${empId}`
      )
      .then((response) => {

        setEmployeeData(
          response.data
        );

      })
      .catch((error) => {

        console.log(error);

      });

  }, []);

  // ============================================
  // LOADING
  // ============================================

  if (!employeeData) {

    return <h1>Loading...</h1>;

  }

  // ============================================
  // SAFE EMPLOYEE
  // ============================================

  const emp =
    employeeData.employee?.[0] || {};

  // ============================================
  // LOGOUT FUNCTION
  // ============================================

  const handleLogout = () => {

    localStorage.removeItem("emp_id");

    localStorage.removeItem("role");

    window.location.href = "/";

  };

  // ============================================
  // UI
  // ============================================

  return (

    <div className="employee-dashboard">

      {/* SIDEBAR */}

      <Sidebar
        setActiveSection={
          setActiveSection
        }
      />

      {/* MAIN SECTION */}

      <div className="employee-main">

        {/* TOPBAR */}

        <Topbar
          emp={emp}
          handleLogout={
            handleLogout
          }
        />

        {/* DASHBOARD */}

        {
          activeSection ===
          "dashboard" && (

            <DashboardSection
              employeeData={
                employeeData
              }
              roles={
    employeeData.roles
  }

            />

          )
        }

        {/* ANALYTICS */}

       
        

        
      {
  activeSection ===
  "schedulerbot" && (

    <SchedulerBot />

  )
}

{
  activeSection ===
  "powerbi" && (

    <PowerBISection />

  )
}

      </div>

    </div>

  );
}

export default EmployeeDashboard;