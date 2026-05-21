"""
scheduling_tool.py
------------------

AI Faculty Scheduling Tool

FEATURES
--------
1. Historical data generation
   (2022-01-01 → 2026-05-21)

2. Skips Saturday and Sunday

3. Random weekday holiday skips

4. Random weekday schedule generation

5. Random batch allocation

6. Random faculty allocation

7. AI chatbot compatible

8. Power BI visualization friendly

9. Current schedules remain:
    session_taken  = 0
    session_left   = allocated value
    session_status = "Not Taken"

10. Historical schedules contain:
    Completed
    Partial
    Pending
    Cancelled
"""

import sqlite3
import random
import datetime


# =========================================================
# DATABASE PATH
# =========================================================

DB_PATH = "schedule.db"


# =========================================================
# LOAD FACULTY DATA
# =========================================================

def _load_faculty_positions():

    today = datetime.datetime.now()

    positions = []

    try:

        conn = sqlite3.connect(DB_PATH)

        conn.row_factory = sqlite3.Row

        rows = conn.execute("""

        SELECT emp_id, doj
        FROM employees

        """).fetchall()

        conn.close()

    except sqlite3.Error as e:

        raise RuntimeError(
            f"Could not load faculty data: {e}"
        )

    # =====================================================
    # EXPERIENCE BASED ROLE ASSIGNMENT
    # =====================================================

    for row in rows:

        doj = datetime.datetime.strptime(
            row["doj"],
            "%Y-%m-%d"
        )

        exp_years = round(
            (today - doj).days / 365.25,
            2
        )

        # =================================================
        # ROLE ASSIGNMENT
        # =================================================

        if exp_years < (5 / 12):

            role = "Invigilator"

        elif exp_years <= 5:

            role = "Co-Educator"

        else:

            role = "Educator"

        positions.append(

            (
                str(row["emp_id"]),
                role
            )

        )

    return positions


# =========================================================
# LOAD BATCH IDS
# =========================================================

def _load_batch_ids():

    try:

        conn = sqlite3.connect(DB_PATH)

        rows = conn.execute("""

        SELECT batch_id
        FROM batches

        """).fetchall()

        conn.close()

    except sqlite3.Error as e:

        raise RuntimeError(
            f"Could not load batch data: {e}"
        )

    return [str(row[0]) for row in rows]


# =========================================================
# FACULTY ALLOCATION
# =========================================================

def faculty_allocation(

    faculty_data,
    session_type

):

    if session_type == 0:

        return None

    random.shuffle(faculty_data)

    for fid in faculty_data:

        if fid[1] >= session_type:

            fid[1] -= session_type

            return fid

    raise ValueError(
        "Error: Out of available faculty members!"
    )


# =========================================================
# MAIN SESSION ALLOCATION
# =========================================================

def session_allocation(session_date):

    # =====================================================
    # LOAD DATA
    # =====================================================

    emp_position = _load_faculty_positions()

    batch_ids = _load_batch_ids()

    # =====================================================
    # RANDOMIZE BATCHES
    # =====================================================

    random.shuffle(batch_ids)

    # =====================================================
    # RANDOM DAILY BATCH COUNT
    # =====================================================

    batch_limit = random.randint(

        40,
        80

    )

    batch_ids = batch_ids[:batch_limit]

    # =====================================================
    # FACULTY CAPACITY
    # =====================================================

    faculty_capacity = [

        [
            fid[0],      # faculty id
            1.0,         # remaining capacity
            fid[1]       # role
        ]

        for fid in emp_position

    ]

    # =====================================================
    # SESSION TYPES
    # =====================================================

    session_type_options = [

        0.25,
        0.5,
        0.75,
        1.0

    ]

    # =====================================================
    # STORE SCHEDULE ROWS
    # =====================================================

    schedule_rows = []

    # =====================================================
    # GET MAX SESSION ID
    # =====================================================

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT MAX(session_id)
    FROM schedules

    """)

    max_id = cursor.fetchone()[0]

    conn.close()

    if max_id is None:

        schedule_id = 1

    else:

        schedule_id = max_id + 1

    # =====================================================
    # LOOP THROUGH RANDOM BATCHES
    # =====================================================

    for batch_id in batch_ids:

        try:

            # =============================================
            # RANDOM SESSION TYPE
            # =============================================

            first_slice = random.choice(
                session_type_options
            )

            # =============================================
            # RANDOM FACULTY
            # =============================================

            chosen_faculty = faculty_allocation(

                faculty_capacity,
                first_slice

            )

            # =============================================
            # DATE CHECK
            # =============================================

            today = datetime.date.today()

            schedule_day = datetime.datetime.strptime(
                session_date,
                "%Y-%m-%d"
            ).date()

            # =============================================
            # HISTORICAL DATA
            # =============================================

            if schedule_day < today:

                session_status = random.choice([

                    "Completed",
                    "Completed",
                    "Completed",

                    "Partial",
                    "Partial",

                    "Pending",

                    "Cancelled"

                ])

                # =========================================
                # COMPLETED
                # =========================================

                if session_status == "Completed":

                    session_taken = first_slice

                    session_left = 0

                # =========================================
                # PARTIAL
                # =========================================

                elif session_status == "Partial":

                    session_taken = round(

                        first_slice * random.uniform(
                            0.3,
                            0.8
                        ),

                        2

                    )

                    session_left = round(

                        first_slice - session_taken,

                        2

                    )

                # =========================================
                # PENDING / CANCELLED
                # =========================================

                else:

                    session_taken = 0

                    session_left = first_slice

            # =============================================
            # TODAY / FUTURE DATA
            # =============================================

            else:

                session_taken = 0

                session_left = first_slice

                session_status = "Not Taken"

            # =============================================
            # STORE ROW
            # =============================================

            schedule_rows.append([

                schedule_id,

                chosen_faculty[0],

                batch_id,

                first_slice,

                session_taken,

                session_left,

                chosen_faculty[2],

                session_date,

                session_status

            ])

            schedule_id += 1

        except ValueError:

            continue

    # =====================================================
    # DELETE EXISTING DATE DATA
    # =====================================================

    delete_query = """

    DELETE FROM schedules
    WHERE session_date = ?

    """

    # =====================================================
    # INSERT QUERY
    # =====================================================

    insert_query = """

    INSERT INTO schedules (

        session_id,
        faculty_id,
        batch_id,

        session_alloc,

        session_taken,
        session_left,

        session_role,

        session_date,

        session_status

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

    """

    # =====================================================
    # SAVE TO DATABASE
    # =====================================================

    try:

        with sqlite3.connect(DB_PATH) as conn:

            conn.execute(

                delete_query,
                (session_date,)

            )

            conn.executemany(

                insert_query,
                schedule_rows

            )

            conn.commit()

    except sqlite3.Error as e:

        return (
            f"Database error while saving schedule: {e}"
        )

    print(

        f"\nSchedule generated for "
        f"{session_date}"

    )

    return schedule_rows


# =========================================================
# HISTORICAL DATA GENERATION
# =========================================================

if __name__ == "__main__":

    print(

        "\nGenerating Historical Data "
        "from 2022 to 2026-05-21..."

    )

    # =====================================================
    # CHECK EXISTING DATA
    # =====================================================

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT COUNT(*)
    FROM schedules

    """)

    total_records = cursor.fetchone()[0]

    conn.close()

    # =====================================================
    # SKIP IF DATA EXISTS
    # =====================================================

    if total_records > 0:

        print(

            "\nHistorical data already exists."

        )

        print(

            "Skipping generation..."

        )

    else:

        # =================================================
        # START & END DATE
        # =================================================

        start_date = datetime.date(
            2022,
            1,
            1
        )

        end_date = datetime.date(
            2026,
            5,
            21
        )

        current_date = start_date

        total_generated = 0

        # =================================================
        # LOOP THROUGH DATES
        # =================================================

        while current_date <= end_date:

            # =============================================
            # SKIP SATURDAY & SUNDAY
            # =============================================

            if current_date.weekday() in [5, 6]:

                current_date += datetime.timedelta(days=1)

                continue

            # =============================================
            # RANDOM HOLIDAY SKIPS
            # =============================================

            holiday_skip = random.random()

            # 25% weekdays skipped
            if holiday_skip < 0.25:

                current_date += datetime.timedelta(days=1)

                continue

            print(

                f"\nGenerating schedules for "
                f"{current_date}"

            )

            # =============================================
            # GENERATE DAILY SCHEDULES
            # =============================================

            result = session_allocation(
                str(current_date)
            )

            if isinstance(result, list):

                total_generated += len(result)

                print(

                    f"{len(result)} schedules created"

                )

            current_date += datetime.timedelta(days=1)

        print(

            f"\nTOTAL HISTORICAL SCHEDULES: "
            f"{total_generated}"

        )

        print(

            "\nHistorical data generation complete!"

        )