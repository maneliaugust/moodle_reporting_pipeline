
import os
import requests
from dotenv import load_dotenv

load_dotenv()

MOODLE_URL = os.getenv("MOODLE_URL")
MOODLE_TOKEN = os.getenv("MOODLE_TOKEN")


def call_moodle_api(function_name, extra_params=None):
    """
    Connect to Moodle REST API and execute a function.
    """

    endpoint = f"{MOODLE_URL}/webservice/rest/server.php"

    params = {
        "wstoken": MOODLE_TOKEN,
        "wsfunction": function_name,
        "moodlewsrestformat": "json"
    }

    if extra_params:
        params.update(extra_params)

    response = requests.get(
        endpoint,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict) and data.get("exception"):
        raise RuntimeError(
            f"Moodle API error: {data.get('message')}"
        )

    return data


def get_courses():
    """
    Retrieve courses from Moodle.
    """

    result = call_moodle_api(
        "core_course_get_courses_by_field"
    )

    return result.get("courses", [])


def get_enrolled_users(course_id):
    """
    Retrieve users enrolled in a specific Moodle course.
    """

    users = call_moodle_api(
        "core_enrol_get_enrolled_users",
        {"courseid": course_id}
    )

    return users


def get_site_info():
    """
    Verify the authenticated Moodle API user.
    """

    return call_moodle_api(
        "core_webservice_get_site_info"
    )
