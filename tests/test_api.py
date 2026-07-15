"""
tests/test_api.py
-----------------
End-to-end integration tests for CodeMentor AI.

Covers all Phase 1-5 features:
  Phase 1: Backend health
  Phase 2: Authentication (signup, login, token)
  Phase 3: Code execution (multiple languages, stdin)
  Phase 4: AI explanation (streaming SSE)
  Phase 5: Dashboard stats, submission history, chat history

Run with:
    pytest tests/test_api.py -v
"""

import json
import time
import pytest  # pyrefly: ignore [missing-import]
import requests

BASE_URL = "http://127.0.0.1:8000"
TEST_EMAIL = f"pytest_{int(time.time())}@test.com"
TEST_PASSWORD = "TestPass123!"

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def auth_token():
    """Create a test user and return their JWT token."""
    requests.post(f"{BASE_URL}/api/auth/signup", json={
        "name": "Test User",
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "gender": "Other",
    })
    r = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
    })
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]


@pytest.fixture(scope="module")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


# ---------------------------------------------------------------------------
# Phase 1: Health
# ---------------------------------------------------------------------------
class TestHealth:
    def test_health_returns_ok(self):
        r = requests.get(f"{BASE_URL}/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# Phase 2: Authentication
# ---------------------------------------------------------------------------
class TestAuth:
    def test_signup_creates_user(self):
        unique_email = f"signup_test_{int(time.time())}@test.com"
        r = requests.post(f"{BASE_URL}/api/auth/signup", json={
            "name": "New User",
            "email": unique_email,
            "password": "StrongPass1!",
            "gender": "Other",
        })
        assert r.status_code == 201
        assert r.json()["email"] == unique_email

    def test_signup_duplicate_email_returns_400(self):
        # Create a user first
        duplicate_email = f"dup_{int(time.time())}@test.com"
        requests.post(f"{BASE_URL}/api/auth/signup", json={
            "name": "First",
            "email": duplicate_email,
            "password": "any",
            "gender": "Other",
        })
        # Try to create it again
        r = requests.post(f"{BASE_URL}/api/auth/signup", json={
            "name": "Duplicate",
            "email": duplicate_email,
            "password": "any",
            "gender": "Other",
        })
        assert r.status_code == 400

    def test_login_returns_token(self, auth_token):
        assert isinstance(auth_token, str)
        assert len(auth_token) > 20

    def test_login_wrong_password_returns_401(self):
        r = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": "wrongpassword",
        })
        assert r.status_code == 401


# ---------------------------------------------------------------------------
# Phase 3: Code Execution
# ---------------------------------------------------------------------------
class TestCodeExecution:
    def _run(self, language, code, stdin=""):
        r = requests.post(f"{BASE_URL}/api/code/execute", json={
            "language": language,
            "code": code,
            "stdin": stdin,
        })
        assert r.status_code == 200, f"Status {r.status_code}: {r.text}"
        return r.json()

    def test_python_hello_world(self):
        data = self._run("python", "print('hello world')")
        assert data["success"] is True
        assert "hello world" in data["output"]

    def test_python_stdin(self):
        data = self._run("python", "x = input()\nprint('got', x)", stdin="myinput\n")
        assert data["success"] is True
        assert "got myinput" in data["output"]

    def test_cpp_compilation(self):
        code = '#include<iostream>\nusing namespace std;\nint main(){cout<<"cpp_ok";return 0;}'
        data = self._run("cpp", code)
        assert data["success"] is True
        assert "cpp_ok" in data["output"]

    def test_javascript(self):
        data = self._run("javascript", "console.log('js_ok')")
        assert data["success"] is True
        assert "js_ok" in data["output"]

    def test_java(self):
        code = 'class Main{public static void main(String[] a){System.out.println("java_ok");}}'
        data = self._run("java", code)
        assert data["success"] is True
        assert "java_ok" in data["output"]

    def test_go(self):
        code = 'package main\nimport "fmt"\nfunc main(){fmt.Println("go_ok")}'
        data = self._run("go", code)
        assert data["success"] is True
        assert "go_ok" in data["output"]

    def test_ruby(self):
        data = self._run("ruby", 'puts "ruby_ok"')
        assert data["success"] is True
        assert "ruby_ok" in data["output"]

    def test_unsupported_language_graceful_error(self):
        """Swift is listed for AI explanation but not Wandbox — must return a graceful error."""
        data = self._run("swift", "print('hi')")
        assert data["success"] is False
        assert "temporarily unavailable" in data["error"]


# ---------------------------------------------------------------------------
# Phase 4: AI Explanation
# ---------------------------------------------------------------------------
class TestAIExplanation:
    def test_explain_streams_and_returns_submission_id(self, auth_headers):
        r = requests.post(
            f"{BASE_URL}/api/chat/explain",
            json={"language": "python", "code": "def add(a, b): return a + b", "github_url": None},
            headers=auth_headers,
            stream=True,
            timeout=30,
        )
        assert r.status_code == 200

        got_submission_id = False
        got_chunk = False

        for line in r.iter_lines():
            if line:
                raw = line.decode()
                if "data: " in raw:
                    try:
                        data = json.loads(raw.replace("data: ", ""))
                        if data.get("submission_id"):
                            got_submission_id = True
                        if data.get("chunk"):
                            got_chunk = True
                    except Exception:
                        pass
            if got_submission_id and got_chunk:
                break

        assert got_submission_id, "No submission_id received in stream"
        assert got_chunk, "No AI text chunks received in stream"


# ---------------------------------------------------------------------------
# Phase 5: Dashboard & History
# ---------------------------------------------------------------------------
class TestDashboardAndHistory:
    def test_stats_endpoint_returns_correct_keys(self, auth_headers):
        r = requests.get(f"{BASE_URL}/api/dashboard/stats", headers=auth_headers)
        assert r.status_code == 200
        data = r.json()
        assert "total_submissions" in data
        assert "total_explanations" in data
        assert "languages_practiced" in data

    def test_submissions_list_not_empty_after_explain(self, auth_headers):
        r = requests.get(f"{BASE_URL}/api/submissions", headers=auth_headers)
        assert r.status_code == 200
        submissions = r.json()
        assert len(submissions) >= 1

    def test_chat_history_for_submission(self, auth_headers):
        # Get the most recent submission
        subs = requests.get(f"{BASE_URL}/api/submissions", headers=auth_headers).json()
        assert subs, "No submissions found"

        sub_id = subs[0]["id"]
        r = requests.get(f"{BASE_URL}/api/chat/{sub_id}", headers=auth_headers)
        assert r.status_code == 200
        history = r.json()
        assert len(history) >= 1
        assert "ai_response" in history[0]
        assert "user_message" in history[0]
