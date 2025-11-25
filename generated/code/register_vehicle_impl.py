import json
from datetime import datetime, timedelta

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
    
    def days_since_last_service(self, last_service_date):
        if not last_service_date:
            return float('inf')
        
        today = datetime.now()
        delta = today - last_service_date
        return delta.days

class MaintenanceDB:
    def __init__(self):
        try:
            with open('maintenance_db.json', 'r') as f:
                self.database = json.load(f)
        except FileNotFoundError:
            self.database = {}
    
    def create_vehicle_record(self, vehicle_id):
        if vehicle_id not in self.database:
            self.database[vehicle_id] = {"last_service_date": None}
        
        with open('maintenance_db.json', 'w') as f:
            json.dump(self.database, f)
    
    def get_next_service_due(self, vehicle_id):
        if vehicle_id not in self.database:
            return {"status": "error", "message": "Vehicle not found"}
        
        last_service_date = datetime.strptime(self.database[vehicle_id]["last_service_date"], "%Y-%m-%d")
        days_since = MaintenanceService().days_since_last_service(last_service_date)
        
        if days_since == float('inf'):
            return {"status": "success", "next_service_due": "Never"}
        
        recommended_interval = 365  # Assuming a yearly service interval
        next_service_days = recommended_interval - days_since
        
        if next_service_days <= 0:
            return {"status": "success", "next_service_due": "Overdue"}
        
        return {"status": "success", "next_service_due": next_service_days}

class RecommendationEngine:
    def __init__(self):
        pass
    
    def generate_recommendations(self, vehicle_id):
        result = MaintenanceDB().get_next_service_due(vehicle_id)
        
        if result["status"] == "error":
            return result
        
        next_service_due = result["next_service_due"]
        recommendations = {
            "vehicle_id": vehicle_id,
            "recommendations": []
        }
        
        if next_service_due == "Overdue" or next_service_due > 365:
            recommendations["recommendations"].append("Immediate service required")
        
        return {"status": "success", "recommendations": recommendations}

if __name__ == '__main__':
    registry = VehicleRegistry()
    
    payload = {
        "vehicle_id": "12345",
        "make": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "last_service_date": "2020-01-01"
    }
    
    print(registry.register_vehicle(payload))
    print(registry.create_vehicle_record("12345"))
    
    recommendation = RecommendationEngine().generate_recommendations("12345")
    if "status" in recommendation:
        print(recommendation)
    else:
        print("Recommendations:", recommendation["recommendations"])
