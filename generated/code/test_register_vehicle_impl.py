import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
import json

# Assuming the rest of the classes and methods are defined elsewhere in your codebase
class VehicleRegistry:
    def __init__(self):
        self.registry = {}
    
    def register_vehicle(self, payload):
        vehicle_id = payload['vehicle_id']
        if vehicle_id in self.registry:
            return {"status": "error", "message": "Vehicle already registered"}
        
        self.registry[vehicle_id] = {
            "last_service_date": None,
            "payload": payload
        }
        return {"status": "success", "message": "Vehicle registered successfully"}
    
    def create_vehicle_record(self, vehicle_id):
        if vehicle_id not in self.registry:
            return {"status": "error", "message": "Vehicle not found"}
        
        payload = self.registry[vehicle_id]['payload']
        MaintenanceDB().create_vehicle_record(vehicle_id)
        return {"status": "success", "message": "Vehicle record created successfully"}

class MaintenanceService:
    def __init__(self):
        pass
    
# Mocking the MaintenanceDB class and its create_vehicle_record method
class MaintenanceDB:
    @staticmethod
    def create_vehicle_record(vehicle_id):
        # Simulate creating a record in the database
        print(f"Vehicle record created for {vehicle_id}")

# Test cases for VehicleRegistry class
class TestVehicleRegistry(unittest.TestCase):
    
    def setUp(self):
        self.registry = VehicleRegistry()
    
    @patch('builtins.print')  # Mocking the print function to capture output
    def test_register_vehicle_success(self, mock_print):
        payload = {'vehicle_id': '123', 'brand': 'Toyota'}
        result = self.registry.register_vehicle(payload)
        self.assertEqual(result, {"status": "success", "message": "Vehicle registered successfully"})
        self.assertIn('123', self.registry.registry)
    
    @patch('builtins.print')  # Mocking the print function to capture output
    def test_register_vehicle_failure(self, mock_print):
        payload = {'vehicle_id': '123', 'brand': 'Toyota'}
        self.registry.register_vehicle(payload)
        result = self.registry.register_vehicle(payload)
        self.assertEqual(result, {"status": "error", "message": "Vehicle already registered"})
    
    @patch('builtins.print')  # Mocking the print function to capture output
    def test_create_vehicle_record_success(self, mock_print):
        payload = {'vehicle_id': '123', 'brand': 'Toyota'}
        self.registry.register_vehicle(payload)
        result = self.registry.create_vehicle_record('123')
        self.assertEqual(result, {"status": "success", "message": "Vehicle record created successfully"})
        mock_print.assert_called_with("Vehicle record created for 123")
    
    @patch('builtins.print')  # Mocking the print function to capture output
    def test_create_vehicle_record_failure(self, mock_print):
        result = self.registry.create_vehicle_record('123')
        self.assertEqual(result, {"status": "error", "message": "Vehicle not found"})

if __name__ == '__main__':
    unittest.main()
