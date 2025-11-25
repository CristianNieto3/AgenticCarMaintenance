import json
from typing import Dict, List

class VehicleRegistry:
    def __init__(self):
        self.maintenance_history: Dict[str, List[Dict]] = {}
    
    def request_maintenance_history(self, vehicleId: str) -> List[Dict]:
        return self.maintenance_history.get(vehicleId, [])

class MaintenanceService:
    def __init__(self):
        pass
    
    def query_records(self, vehicleId: str, maintenanceDB: 'MaintenanceDB') -> List[Dict]:
        return maintenanceDB.return_records(vehicleId)

class MaintenanceDB:
    def __init__(self):
        self.maintenance_history: Dict[str, List[Dict]] = {}
    
    def return_records(self, vehicleId: str) -> List[Dict]:
        return self.maintenance_history.get(vehicleId, [])

class RecommendationEngine:
    def __init__(self):
        pass

# In-memory storage for demonstration purposes
if __name__ == '__main__':
    # Initialize the system components
    vehicle_registry = VehicleRegistry()
    maintenance_db = MaintenanceDB()
    maintenance_service = MaintenanceService()
    
    # Mock data
    mock_records = [
        {"vehicleId": "123", "date": "2023-01-01", "description": "Oil Change"},
        {"vehicleId": "123", "date": "2023-02-01", "description": "Tire Rotation"}
    ]
    
    # Set up maintenance history in the database
    for record in mock_records:
        if record["vehicleId"] not in maintenance_db.maintenance_history:
            maintenance_db.maintenance_history[record["vehicleId"]] = []
        maintenance_db.maintenance_history[record["vehicleId"]].append(record)
    
    # Set up vehicle registry with the same data
    for record in mock_records:
        if record["vehicleId"] not in vehicle_registry.maintenance_history:
            vehicle_registry.maintenance_history[record["vehicleId"]] = []
        vehicle_registry.maintenance_history[record["vehicleId"]].append(record)
    
    # User requests maintenance history for a vehicle
    user_request = "123"
    maintenance_records = maintenance_service.query_records(user_request, maintenance_db)
    
    print("Maintenance History for Vehicle", user_request, ":")
    for record in maintenance_records:
        print(record)
