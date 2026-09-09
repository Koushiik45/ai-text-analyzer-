"""
Tests for the analyze endpoint.

Real engineers write tests BEFORE shipping. This file tests:
- Happy path (valid input → correct response)
- Edge cases (empty input, very long input)
- Response shape (all fields present, correct types)

Run with: pytest tests/ -v
"""

from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)


class TestHealthCheck:
    """Health endpoint should always return ok."""

    def test_health_returns_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data


class TestAnalyzeEndpoint:
    """Core analysis endpoint tests."""

    def test_analyze_valid_text(self):
        response = client.post(
            "/analyze",
            json={"text": "The product launch exceeded our targets significantly."},
        )
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "word_count" in data
        assert "sentiment" in data
        assert "processed_at" in data
        assert isinstance(data["word_count"], int)
        assert data["word_count"] > 0

    def test_analyze_positive_sentiment(self):
        response = client.post(
            "/analyze",
            json={"text": "This is a great and excellent product with amazing results."},
        )
        data = response.json()
        assert data["sentiment"] == "positive"

    def test_analyze_negative_sentiment(self):
        response = client.post(
            "/analyze",
            json={"text": "This is a terrible and awful product that failed badly."},
        )
        data = response.json()
        assert data["sentiment"] == "negative"

    def test_analyze_neutral_sentiment(self):
        response = client.post(
            "/analyze",
            json={"text": "The meeting is scheduled for Tuesday at 3pm."},
        )
        data = response.json()
        assert data["sentiment"] == "neutral"

    def test_analyze_empty_text_rejected(self):
        """Empty strings should be rejected by Pydantic validation."""
        response = client.post("/analyze", json={"text": ""})
        assert response.status_code == 422  # Validation error

    def test_analyze_missing_text_rejected(self):
        """Missing required field should be rejected."""
        response = client.post("/analyze", json={})
        assert response.status_code == 422

    def test_analyze_long_text_truncates_summary(self):
        """Summary should truncate long text to ~30 words."""
        long_text = " ".join(["word"] * 100)
        response = client.post("/analyze", json={"text": long_text})
        data = response.json()
        assert data["summary"].endswith("...")
        assert data["word_count"] == 100

    def test_response_has_timestamp(self):
        response = client.post(
            "/analyze",
            json={"text": "Check the timestamp."},
        )
        data = response.json()
        assert "T" in data["processed_at"]  # ISO format check
class TestVersionEndpoint:
    def test_version_returns_ok(self):
        response = client.get("/version")
        assert response.status_code == 200
        data = response.json()
        assert data["version"] == "0.1.0"
        assert data["title"] == "AI Text Analyzer"