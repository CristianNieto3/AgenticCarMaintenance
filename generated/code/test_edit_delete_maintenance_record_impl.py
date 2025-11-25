import unittest
from unittest import mock

class TestVehicleRegistry(unittest.TestCase):
    def setUp(self):
        self.vehicle_registry = VehicleRegistry()
    
    @mock.patch('builtins.print')
    def test_edit_maintenance_record(self, mock_print):
        self.vehicle_registry.edit_delete_maintenance_record(123, 'edit')
        mock_print.assert_called_with("Editing maintenance record with ID 123")
    
    @mock.patch('builtins.print')
    def test_delete_maintenance_record(self, mock_print):
        self.vehicle_registry.edit_delete_maintenance_record(456, 'delete')
        mock_print.assert_called_with("Deleting maintenance record with ID 456")
    
    def test_invalid_action(self):
        with self.assertRaises(ValueError) as context:
            self.vehicle_registry.edit_delete_maintenance_record(789, 'invalid')
        self.assertEqual("Invalid action. Use 'edit' or 'delete'.", str(context.exception))

class TestMaintenanceService(unittest.TestCase):
    @mock.patch('builtins.print')
    def test_update_maintenance_record(self, mock_print):
        db_connection = mock.Mock()
        maintenance_service = MaintenanceService(db_connection)
        maintenance_service.update_delete_record(123, 'update')
        mock_print.assert_called_with("Updating maintenance record with ID 123")
    
    @mock.patch('builtins.print')
    def test_delete_maintenance_record(self, mock_print):
        db_connection = mock.Mock()
        maintenance_service = MaintenanceService(db_connection)
        maintenance_service.update_delete_record(456, 'delete')
        mock_print.assert_called_with("Deleting maintenance record with ID 456")
    
    def test_invalid_action(self):
        db_connection = mock.Mock()
        maintenance_service = MaintenanceService(db_connection)
        with self.assertRaises(ValueError) as context:
            maintenance_service.update_delete_record(789, 'invalid')
        self.assertEqual("Invalid action. Use 'edit' or 'delete'.", str(context.exception))

if __name__ == '__main__':
    unittest.main()
