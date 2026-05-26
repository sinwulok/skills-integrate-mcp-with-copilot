"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities",
)

BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "mergington.sqlite3"

INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"],
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"],
    },
}


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS activities (
                name TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                schedule TEXT NOT NULL,
                max_participants INTEGER NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS participants (
                activity_name TEXT NOT NULL,
                email TEXT NOT NULL,
                PRIMARY KEY (activity_name, email),
                FOREIGN KEY (activity_name) REFERENCES activities(name) ON DELETE CASCADE
            )
            """
        )

        existing_activities = connection.execute(
            "SELECT COUNT(*) AS count FROM activities"
        ).fetchone()["count"]

        if existing_activities == 0:
            for activity_name, activity in INITIAL_ACTIVITIES.items():
                connection.execute(
                    """
                    INSERT INTO activities (name, description, schedule, max_participants)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        activity_name,
                        activity["description"],
                        activity["schedule"],
                        activity["max_participants"],
                    ),
                )

                for email in activity["participants"]:
                    connection.execute(
                        """
                        INSERT INTO participants (activity_name, email)
                        VALUES (?, ?)
                        """,
                        (activity_name, email),
                    )


def get_activity(activity_name):
    with get_connection() as connection:
        activity = connection.execute(
            """
            SELECT name, description, schedule, max_participants
            FROM activities
            WHERE name = ?
            """,
            (activity_name,),
        ).fetchone()

        if activity is None:
            return None

        participants = connection.execute(
            """
            SELECT email
            FROM participants
            WHERE activity_name = ?
            ORDER BY email
            """,
            (activity_name,),
        ).fetchall()

    return {
        "description": activity["description"],
        "schedule": activity["schedule"],
        "max_participants": activity["max_participants"],
        "participants": [participant["email"] for participant in participants],
    }


def get_all_activities():
    with get_connection() as connection:
        activity_rows = connection.execute(
            """
            SELECT name, description, schedule, max_participants
            FROM activities
            ORDER BY name
            """
        ).fetchall()

        activities = {}
        for activity in activity_rows:
            participants = connection.execute(
                """
                SELECT email
                FROM participants
                WHERE activity_name = ?
                ORDER BY email
                """,
                (activity["name"],),
            ).fetchall()

            activities[activity["name"]] = {
                "description": activity["description"],
                "schedule": activity["schedule"],
                "max_participants": activity["max_participants"],
                "participants": [participant["email"] for participant in participants],
            }

    return activities


# Mount the static files directory
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def read_activities():
    return get_all_activities()


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    activity = get_activity(activity_name)

    # Validate activity exists
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(
            status_code=400,
            detail="Activity is already full",
        )

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO participants (activity_name, email)
            VALUES (?, ?)
            """,
            (activity_name, email),
        )

    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    activity = get_activity(activity_name)

    # Validate activity exists
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM participants
            WHERE activity_name = ? AND email = ?
            """,
            (activity_name, email),
        )

    return {"message": f"Unregistered {email} from {activity_name}"}


initialize_database()
