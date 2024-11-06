import unittest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

class TestAPI(unittest.TestCase):

    def test_fetch_all_data(self):
        response = client.get("/data/all")
        self.assertEqual(response.status_code, 200, "Response status should be 200")
        self.assertIsInstance(response.json(), list, "Response should be a list of records")

    def test_fetch_filtered_data_valid(self):
        response = client.get("/data/filter?start_date=2023-10-01&end_date=2023-10-31&status=complete")
        self.assertEqual(response.status_code, 200, "Response status should be 200 for valid query")
        self.assertIsInstance(response.json(), list, "Response should be a list of records")

    def test_fetch_filtered_data_invalid_date(self):
        response = client.get("/data/filter?start_date=invalid-date")
        self.assertEqual(response.status_code, 400, "Response status should be 400 for invalid date format")
        self.assertIn("Invalid start_date format", response.json()["detail"], "Error message should indicate invalid date format")

if __name__ == "__main__":
    unittest.main()
