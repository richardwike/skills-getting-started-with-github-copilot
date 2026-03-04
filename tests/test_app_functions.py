import pytest
from fastapi import HTTPException

from src.app import activities, signup_for_activity, unregister_for_activity


def test_signup_for_activity_adds_participant():
    activity_name = "Chess Club"
    new_email = "functiontest@mergington.edu"

    response = signup_for_activity(activity_name, new_email)

    assert response["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in activities[activity_name]["participants"]


def test_signup_for_activity_raises_for_duplicate():
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    with pytest.raises(HTTPException) as exc_info:
        signup_for_activity(activity_name, existing_email)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Student already signed up for this activity"


def test_signup_for_activity_raises_for_unknown_activity():
    with pytest.raises(HTTPException) as exc_info:
        signup_for_activity("Unknown Club", "person@mergington.edu")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Activity not found"


def test_unregister_for_activity_removes_participant():
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    response = unregister_for_activity(activity_name, existing_email)

    assert response["message"] == f"Unregistered {existing_email} from {activity_name}"
    assert existing_email not in activities[activity_name]["participants"]


def test_unregister_for_activity_raises_for_missing_participant():
    with pytest.raises(HTTPException) as exc_info:
        unregister_for_activity("Chess Club", "notfound@mergington.edu")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Student is not signed up for this activity"


def test_unregister_for_activity_raises_for_unknown_activity():
    with pytest.raises(HTTPException) as exc_info:
        unregister_for_activity("Unknown Club", "person@mergington.edu")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Activity not found"
