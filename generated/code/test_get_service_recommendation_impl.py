import unittest
from unittest.mock import patch
from io import StringIO
import sys

class VehicleRegistry:
    def __init__(self):
        self.maintenance_records = {}
    
    def fetch_recent_maintenance(self, vehicleId):
        return self.maintenance_records.get(vehicleId, [])

class MaintenanceService:
    def __init__(self):
        self.db = VehicleRegistry()
    
    def request_recommendation(self, vehicleId, context):
        records = self.db.fetch_recent_maintenance(vehicleId)
        recommendation_engine = RecommendationEngine()
        return recommendation_engine.generate_recommendation(records, context)

class RecommendationEngine:
    def __init__(self):
        self.db = VehicleRegistry()
    
    def fetch_recent_maintenance(self, vehicleId):
        return self.db.fetch_recent_maintenance(vehicleId)
    
    def generate_recommendation(self, records, context):
        if not records:
            return "Recommend major service"
        else:
            return "Suggest regular check-up"

class TestMaintenanceService(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_request_recommendation_no_records(self, mock_stdout):
        ms = MaintenanceService()
        recommendation = ms.request_recommendation("123", {})
        self.assertEqual(recommendation, "Recommend major service")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_request_recommendation_with_records(self, mock_stdout):
        ms = MaintenanceService()
        ms.db.maintenance_records["123"] = ["oil change", "tire rotation"]
        recommendation = ms.request_recommendation("123", {})
        self.assertEqual(recommendation, "Suggest regular check-up")

if __name__ == "__main__":
    unittest.main()
