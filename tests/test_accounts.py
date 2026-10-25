"""Automated tests for the Account REST API."""
from unittest import TestCase

from service import app
from service.routes import reset_counters


class AccountTest(TestCase):
    """Test account CRUD operations."""

    def setUp(self):
        app.testing = True
        reset_counters()
        self.client = app.test_client()
        self.account = {
            "name": "John Doe",
            "email": "john@doe.com",
            "address": "123 Main St.",
            "phone_number": "555-1212",
        }

    def test_create_account(self):
        response = self.client.post("/accounts", json=self.account)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "John Doe")
        self.assertIn("/accounts/1", response.headers["Location"])

    def test_create_account_missing_fields(self):
        response = self.client.post("/accounts", json={"name": "John Doe"})
        self.assertEqual(response.status_code, 400)

    def test_list_accounts(self):
        self.client.post("/accounts", json=self.account)
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_read_account(self):
        self.client.post("/accounts", json=self.account)
        response = self.client.get("/accounts/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["email"], "john@doe.com")

    def test_read_missing_account(self):
        response = self.client.get("/accounts/999")
        self.assertEqual(response.status_code, 404)

    def test_update_account(self):
        self.client.post("/accounts", json=self.account)
        response = self.client.put(
            "/accounts/1", json={"name": "Jane Doe"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Jane Doe")

    def test_delete_account(self):
        self.client.post("/accounts", json=self.account)
        response = self.client.delete("/accounts/1")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            self.client.get("/accounts/1").status_code, 404
        )

    def test_delete_missing_account(self):
        response = self.client.delete("/accounts/999")
        self.assertEqual(response.status_code, 404)
