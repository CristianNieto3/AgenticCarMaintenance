import unittest
from datetime import datetime

class VehicleRegistry:
    def __init__(self):
        self.maintenance_records = {}
    
    def log_maintenance_event(self, vehicleId, details):
        if vehicleId not in self.maintenance_records:
            self.maintenance_records[vehicleId] = []
        self.maintenance_records[vehicleId].append(details)
    
    def insert_maintenance_record(self, record):
        self.maintenance_records[record['vehicleId']] = [record]
    
    def get_days_since_last_service(self, vehicleId, current_date):
        if vehicleId not in self.maintenance_records:
            return None
        records = self.maintenance_records[vehicleId]
        if not records:
            return None
        last_record = records[-1]
        last_service_date = last_record['date']
        current_date = datetime.strptime(current_date, '%Y-%m-%d')
        last_service_date = datetime.strptime(last_service_date, '%Y-%m-%d')
        delta = current_date - last_service_date
        return delta.days

class TestVehicleRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = VehicleRegistry()
    
    def test_log_maintenance_event(self):
        self.registry.log_maintenance_event('123', {'date': '2023-04-01'})
        self.assertEqual(len(self.registry.maintenance_records), 1)
        self.assertIn('123', self.registry.maintenance_records)
        self.assertEqual(len(self.registry.maintenance_records['123']), 1)
    
    def test_insert_maintenance_record(self):
        record = {'vehicleId': '123', 'date': '2023-04-01'}
        self.registry.insert_maintenance_record(record)
        self.assertEqual(len(self.registry.maintenance_records), 1)
        self.assertIn('123', self.registry.maintenance_records)
        self.assertEqual(len(self.registry.maintenance_records['123']), 1)
    
    def test_get_days_since_last_service_nonexistent_vehicle(self):
        result = self.registry.get_days_since_last_service('456', '2023-04-01')
        self.assertIsNone(result)
    
    def test_get_days_since_last_service_no_records(self):
        self.registry.log_maintenance_event('123', {'date': '2023-04-01'})
        result = self.registry.get_days_since_last_service('123', '2023-04-01')
        self.assertIsNone(result)
    
    def test_get_days_since_last_service_valid(self):
        self.registry.log_maintenance_event('123', {'date': '2023-03-31'})
        result = self.registry.get_days_since_last_service('123', '2023-04-01')
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
