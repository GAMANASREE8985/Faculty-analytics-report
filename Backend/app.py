# =========================================================
# Backend/app.py
# =========================================================

from flask import Flask, jsonify
from flask import request

from flask_cors import CORS

import sqlite3
import pandas as pd

from agent import run_agent


# =========================================================
# FLASK SETUP
# =========================================================

app = Flask(__name__)

CORS(app)


# =========================================================
# DATABASE
# =========================================================

DATABASE = "schedule.db"


# =========================================================
# LOGIN API
# =========================================================

@app.route("/login/<emp_id>/<password>")

def login(emp_id, password):

    # =====================================================
    # HR LOGIN
    # =====================================================

    if emp_id == "hr" and password == "hr123":

        return jsonify({

            "status": "success",

            "role": "hr",

            "employee": {

                "emp_id": 999,

                "name": "HR Admin",

                "type": "HR"

            }

        })

    # =====================================================
    # NORMAL EMPLOYEE LOGIN
    # =====================================================

    conn = sqlite3.connect(DATABASE)

    employee_df = pd.read_sql_query(

        f"""

        SELECT *

        FROM employees

        WHERE emp_id = {emp_id}

        """,

        conn

    )

    conn.close()

    # =====================================================
    # EMPLOYEE NOT FOUND
    # =====================================================

    if employee_df.empty:

        return jsonify({

            "status": "error",

            "message": "Employee Not Found"

        })

    # =====================================================
    # FIRST ROW
    # =====================================================

    employee = employee_df.iloc[0]

    # =====================================================
    # PASSWORD CHECK
    # =====================================================

    if str(employee["doj"]) != password:

        return jsonify({

            "status": "error",

            "message": "Invalid Password"

        })

    # =====================================================
    # DEFAULT ROLE
    # =====================================================

    role = "employee"

    employee_type = "Employee"

    # =====================================================
    # CHECK type COLUMN
    # =====================================================

    if "type" in employee.index:

        employee_type = str(employee["type"])

        if employee_type == "HR":

            role = "hr"

    # =====================================================
    # SUCCESS RESPONSE
    # =====================================================

    return jsonify({

        "status": "success",

        "role": role,

        "employee": {

            "emp_id": int(employee["emp_id"]),

            "name": str(employee["name"]),

            "type": employee_type

        }

    })


# =========================================================
# HR DASHBOARD API
# =========================================================

@app.route("/hr-dashboard")

def hr_dashboard():

    conn = sqlite3.connect(DATABASE)

    employees_df = pd.read_sql_query(

        "SELECT * FROM employees",

        conn

    )

    schedules_df = pd.read_sql_query(

        "SELECT * FROM schedules",

        conn

    )

    artifacts_df = pd.read_sql_query(

        "SELECT * FROM artifacts",

        conn

    )

    conn.close()

    data = {

        "total_employees":

            int(len(employees_df)),

        "total_sessions":

            int(len(schedules_df)),

        "total_artifacts":

            int(len(artifacts_df)),

        "employees":

            employees_df.to_dict(
                orient="records"
            ),

        "sessions":

            schedules_df.to_dict(
                orient="records"
            ),

        "artifacts":

            artifacts_df.to_dict(
                orient="records"
            )

    }

    return jsonify(data)


# =========================================================
# EMPLOYEE DASHBOARD API
# =========================================================

@app.route("/employee-dashboard/<emp_id>")

def employee_dashboard(emp_id):

    conn = sqlite3.connect(DATABASE)

    # =====================================================
    # EMPLOYEE DETAILS
    # =====================================================

    employee_df = pd.read_sql_query(

        f"""

        SELECT *

        FROM employees

        WHERE emp_id = {emp_id}

        """,

        conn

    )

    # =====================================================
    # EMPLOYEE ROLES
    # =====================================================

    try:

        roles_df = pd.read_sql_query(

            f"""

            SELECT *

            FROM emp_position

            WHERE faculty_id = {emp_id}

            """,

            conn

        )

    except:

        roles_df = pd.DataFrame()

    # =====================================================
    # ALL SESSIONS
    # =====================================================

    schedules_df = pd.read_sql_query(

        """

        SELECT *

        FROM schedules

        """,

        conn

    )

    # =====================================================
    # REMOVE COLUMN SPACES
    # =====================================================

    schedules_df.columns = (

        schedules_df.columns

        .str.strip()

    )

    # =====================================================
    # EMPLOYEE ARTIFACTS
    # =====================================================

    try:

        artifacts_df = pd.read_sql_query(

            f"""

            SELECT *

            FROM artifacts

            WHERE faculty_id = {emp_id}

            """,

            conn

        )

    except:

        artifacts_df = pd.DataFrame()

    conn.close()

    # =====================================================
    # RESPONSE
    # =====================================================

    data = {

        "employee":

            employee_df.to_dict(
                orient="records"
            ),

        "roles":

            roles_df.to_dict(
                orient="records"
            ),

        "sessions":

            schedules_df.to_dict(
                orient="records"
            ),

        "artifacts":

            artifacts_df.to_dict(
                orient="records"
            )

    }

    return jsonify(data)


# =========================================================
# EMPLOYEE ARTIFACT API
# =========================================================

@app.route("/artifacts/<emp_id>")

def employee_artifacts(emp_id):

    conn = sqlite3.connect(DATABASE)

    artifact_df = pd.read_sql_query(

        f"""

        SELECT *

        FROM artifacts

        WHERE faculty_id = {emp_id}

        """,

        conn

    )

    conn.close()

    return jsonify(

        artifact_df.to_dict(
            orient="records"
        )

    )


# =========================================================
# CHATBOT API
# =========================================================

@app.route(

    "/chatbot",

    methods=["POST"]

)

def chatbot():

    data = request.json

    user_message = data["message"]

    try:

        response = run_agent(

            user_message

        )

        return jsonify({

            "reply": str(response)

        })

    except Exception as e:

        return jsonify({

            "reply":

                f"Error: {str(e)}"

        })
@app.route("/faculty-ids")

def get_faculty_ids():

    conn = sqlite3.connect(
        "schedule.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

        SELECT DISTINCT faculty_id
        FROM emp_position
        ORDER BY faculty_id

    """)

    rows = cursor.fetchall()

    conn.close()

    faculty_ids = [
        row[0]
        for row in rows
    ]

    return jsonify(faculty_ids)
# =========================================================
# FACULTY DETAILS API
# =========================================================

@app.route("/faculty-details/<faculty_id>")

def faculty_details(faculty_id):

    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()

    cursor.execute("""

        SELECT DISTINCT position

        FROM emp_position

        WHERE faculty_id = ?

    """, (faculty_id,))

    rows = cursor.fetchall()

    conn.close()

    positions = [

        row[0].strip()

        for row in rows

    ]

    return jsonify({

        "faculty_id": faculty_id,

        "positions": positions

    })
# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)