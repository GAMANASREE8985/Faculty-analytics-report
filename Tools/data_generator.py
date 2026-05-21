import pandas as pd
import random
from faker import Faker

fake = Faker()

total_employees = 5000
total_batches = 500
total_sessions = 50000
total_schedules = 20000

cities = ["Bangalore", "Chennai", "Hyderabad", "Pune", "Delhi"]
states = ["KA", "TN", "TS", "MH", "DL"]

faculty_types = [
    "Educator",
    "Co-Educator",
    "Invigilator"
]

positions = [
    "Faculty",
    "Coordinator",
    "Batch Owner"
]

tracks = [
    "Java Full Stack",
    "Python Full Stack",
    "Data Engineering",
    "Cloud Computing",
    "DevOps",
    "AI & ML"
]

artifact_names = [
    ("Certifications", 5),
    ("Question Paper", 3),
    ("Capstone", 5),
    ("Course", 10),
    ("Evaluation Tool", 3)
]

# employee data

employees = []

for i in range(1001, 1001 + total_employees):

    name = fake.first_name()

    if random.random() < 0.05:
        name = ""

    city = random.choice(cities)
    state = random.choice(states)

    if random.random() < 0.1:
        state = random.choice(states)

    doj = fake.date_between(
        start_date='-10y',
        end_date='today'
    )

    if random.random() < 0.03:
        doj = ""

    employees.append({

        "emp_id": i,
        "name": name,
        "mail": f"{name.lower()}.{i}.trn" if name else "",
        "city": city,
        "state": state,
        "doj": doj

    })

employee_df = pd.DataFrame(employees)

employee_df.to_csv("Employee.csv", index=False)

print("employee file created")


# employee positions

emp_positions = []

for i in range(1001, 1001 + total_employees):

    total_roles = random.randint(1, 3)

    selected_roles = random.sample(
        positions,
        total_roles
    )

    for role in selected_roles:

        emp_positions.append({

            "faculty_id": i,
            "position": role

        })

emp_position_df = pd.DataFrame(emp_positions)

emp_position_df.to_csv(
    "Emp_Position.csv",
    index=False
)

print("position file created")


# batch data

batches = []

for i in range(4001, 4001 + total_batches):

    batches.append({

        "batch_id": i,
        "batch_owner": random.randint(1001, 1000 + total_employees),
        "batch_name": f"Batch_{i}",
        "track_name": random.choice(tracks),
        "stu_strength": random.randint(25, 60)

    })

batch_df = pd.DataFrame(batches)

batch_df.to_csv("Batch.csv", index=False)

print("batch file created")

"""

# schedule data

schedule_data = []

roles = [
    "Educator",
    "Co-Educator",
    "Invigilator"
]

for i in range(2001, 2001 + total_schedules):

    alloc = round(random.choice([
        0.25,
        0.5,
        0.75,
        1
    ]), 2)

    if random.random() < 0.05:
        alloc = ""

    schedule_data.append({

        "coord_id": i,
        "faculty_id": random.randint(1001, 1000 + total_employees),
        "batch_id": random.randint(4001, 4000 + total_batches),
        "session_date": fake.date_between(
            start_date='-1y',
            end_date='today'
        ),
        "session_allocated": alloc,
        "role": random.choice(roles)

    })

schedule_df = pd.DataFrame(schedule_data)

schedule_df.to_csv("Schedule.csv", index=False)

print("schedule file created")


# session data

session_data = []

statuses = [
    "Completed",
    "Partial",
    "Pending"
]

for i in range(5001, 5001 + total_sessions):

    alloc = round(random.choice([
        0.25,
        0.5,
        0.75,
        1
    ]), 2)

    taken = round(random.choice([
        0,
        0.25,
        0.5,
        0.75,
        1
    ]), 2)

    left = round(max(alloc - taken, 0), 2)

    if random.random() < 0.05:
        alloc = ""

    if random.random() < 0.05:
        taken = ""

    if random.random() < 0.05:
        left = ""

    status = random.choice(statuses)

    if random.random() < 0.03:
        status = ""

    session_data.append({

        "session_id": i,
        "faculty_id": random.randint(1001, 1000 + total_employees),
        "batch_id": random.randint(4001, 4000 + total_batches),
        "session_date": fake.date_between(
            start_date='-1y',
            end_date='today'
        ),
        "session_allocated": alloc,
        "session_taken": taken,
        "session_left": left,
        "session_status": status

    })

session_df = pd.DataFrame(session_data)

session_df.to_csv("Session.csv", index=False)

print("session file created")
"""

# artifacts

artifact_data = []

artifact_id = 201

for art in artifact_names:

    artifact_data.append({

        "artifact_id": artifact_id,
        "artifact_name": art[0],
        "session_equivalence": art[1]

    })

    artifact_id += 1

artifact_df = pd.DataFrame(artifact_data)

artifact_df.to_csv("Artifacts.csv", index=False)

print("artifact file created")


# completed artifacts

artifact_completed = []

for i in range(15000):

    artifact_completed.append({

        "faculty_id": random.randint(1001, 1000 + total_employees),
        "artifact_id": random.randint(201, 205),
        "count": random.randint(1, 5)

    })

artifact_completed_df = pd.DataFrame(
    artifact_completed
)

artifact_completed_df.to_csv(
    "Artifacts_Completed.csv",
    index=False
)

print("completed artifact file created")


# reviews

reviews = []

for i in range(1001, 1001 + total_employees):

    reviews.append({

        "faculty_id": i,
        "reviews": random.randint(1, 5)

    })

reviews_df = pd.DataFrame(reviews)

reviews_df.to_csv("Reviews.csv", index=False)

print("reviews file created")


# salary

salary_data = []

salary_id = 1

for i in range(1001, 1001 + total_employees):

    salary_data.append({

        "salary_id": salary_id,
        "faculty_id": i,
        "salary": random.randint(30000, 120000)

    })

    salary_id += 1

salary_df = pd.DataFrame(salary_data)

salary_df.to_csv("Salary.csv", index=False)

print("salary file created")


# self development

sd_data = []

for i in range(1001, 1001 + total_employees):

    sd_data.append({

        "faculty_id": i,
        "internal_certification": random.randint(0, 5),
        "external_certification": random.randint(0, 5)

    })

sd_df = pd.DataFrame(sd_data)

sd_df.to_csv(
    "Self_Development.csv",
    index=False
)

print("self development file created")


# batch performance

bp_data = []

for i in range(4001, 4001 + total_batches):

    total = random.randint(25, 60)

    passed = random.randint(15, total)

    failed = total - passed

    bp_data.append({

        "batch_id": i,
        "stu_passed": passed,
        "stu_failed": failed,
        "total_stu": total

    })

bp_df = pd.DataFrame(bp_data)

bp_df.to_csv(
    "Batch_Performance.csv",
    index=False
)

print("batch performance file created")

print("\nall files generated")