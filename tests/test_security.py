"""Tests for security headers and CORS configuration."""
from unittest import TestCase

from service import app


class SecurityTest(TestCase):
    """Verify HTTP security headers and cross-origin requests."""

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_security_headers(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("X-Frame-Options"), "SAMEORIGIN"
        )
        self.assertEqual(
            response.headers.get("X-Content-Type-Options"), "nosniff"
        )
        self.assertIn(
            "default-src 'self'",
            response.headers.get("Content-Security-Policy", "")
        )

    def test_cors_header(self):
        response = self.client.get(
            "/",
            headers={"Origin": "http://localhost:3000"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Access-Control-Allow-Origin"),
            "http://localhost:3000"
        )
