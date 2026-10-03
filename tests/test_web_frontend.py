"""Unit tests for LiftMate web frontend and API endpoints."""
import json
from io import BytesIO

from api.index import app


def _request(method: str, path: str, body: bytes = b"", query: str = "") -> tuple[int, dict, bytes]:
    status_code = None
    headers_dict = {}

    def start_response(status, headers):
        nonlocal status_code, headers_dict
        status_code = int(status.split()[0])
        headers_dict = dict(headers)

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": query,
        "wsgi.input": BytesIO(body),
        "CONTENT_LENGTH": str(len(body)),
        "CONTENT_TYPE": "application/json" if body else "",
    }
    resp = app(environ, start_response)
    return status_code, headers_dict, b"".join(resp)


def test_frontend_static_html():
    status, headers, body = _request("GET", "/")
    assert status == 200
    assert "text/html" in headers.get("Content-Type", "")
    assert b"LiftMate" in body
    assert b"TRAINING OS" in body


def test_frontend_static_css():
    status, headers, body = _request("GET", "/style.css")
    assert status == 200
    assert "text/css" in headers.get("Content-Type", "")
    assert b"--strava-orange" in body


def test_frontend_static_js():
    status, headers, body = _request("GET", "/app.js")
    assert status == 200
    assert "javascript" in headers.get("Content-Type", "")
    assert b"fetchDashboard" in body


def test_frontend_dashboard():
    status, headers, body = _request("GET", "/api/dashboard")
    assert status == 200
    data = json.loads(body.decode())
    assert "profile" in data
    assert "weekly_stats" in data
    assert "recent_activities" in data
    assert "prs" in data
    assert len(data["recent_activities"]) > 0


def test_frontend_activities_filtering():
    status, headers, body = _request("GET", "/api/activities", query="sport=Run")
    assert status == 200
    data = json.loads(body.decode())
    assert all(a["sport_type"] == "Run" for a in data["activities"])


def test_frontend_chat():
    payload = json.dumps({"message": "what is my bench PR?"}).encode()
    status, headers, body = _request("POST", "/api/chat", body=payload)
    assert status == 200
    data = json.loads(body.decode())
    assert "reply" in data
    assert "Bench Press" in data["reply"]


def test_frontend_simulate_workout():
    workout = "Bench Press\nSet 1: 100kg x 6\nSet 2: 90kg x 8"
    payload = json.dumps({"text": workout}).encode()
    status, headers, body = _request("POST", "/api/simulate-workout", body=payload)
    assert status == 200
    data = json.loads(body.decode())
    assert data["status"] == "success"
    assert data["total_volume_kg"] == 1320.0
    assert len(data["exercises"]) == 1
    assert "briefing" in data


def test_frontend_chart_preset():
    status, headers, body = _request("GET", "/api/chart/s01")
    assert status == 200
    assert headers.get("Content-Type") == "image/png"
    assert len(body) > 1000


def test_frontend_profile_update():
    payload = json.dumps({"max_hr": 195, "training_goal": "Marathon + 400kg Total"}).encode()
    status, headers, body = _request("POST", "/api/profile", body=payload)
    assert status == 200
    data = json.loads(body.decode())
    assert data["status"] == "success"
    assert data["profile"]["max_hr"] == 195
    assert data["profile"]["training_goal"] == "Marathon + 400kg Total"
