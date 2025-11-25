import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Assuming the rest of the code is provided and works as expected
class TestVehicleRegistry(unittest.TestCase):
    def setUp(self):
        self.vehicle_registry = VehicleRegistry()
        self.maintenance_db = MaintenanceDB()
        self.maintenance_service = MaintenanceService()

    @patch('builtins.print')
    def test_request_maintenance_history(self, mock_print):
        # Test when vehicleId is not in maintenance_history
        vehicleId = "123"
        expected_output = []
        self.assertEqual(self.vehicle_registry.request_maintenance_history(vehicleId), expected_output)
        
        # Add a record to the maintenance history for the vehicleId
        self.maintenance_db.maintenance_history[vehicleId] = [{'date': '2023-01-01', 'description': 'Oil change'}]
        self.vehicle_registry.maintenance_history[vehicleId] = [{'date': '2023-01-01', 'description': 'Oil change'}]
        
        # Test when vehicleId is in maintenance_history
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.maintenance_service.query_records(vehicleId, self.maintenance_db)
            output = fake_output.getvalue().strip()
            expected_output = json.dumps([{'date': '2023-01-01', 'description': 'Oil change'}])
            self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
