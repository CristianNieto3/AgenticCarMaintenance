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
        # Simple recommendation logic: if no records, recommend a major service; otherwise, suggest regular check-up
        if not records:
            return "Recommend major service for vehicle {}".format(vehicleId)
        else:
            return "Suggest performing regular check-up for vehicle {}".format(vehicleId)

# Demo
if __name__ == '__main__':
    maintenance_service = MaintenanceService()
    recommendation = maintenance_service.request_recommendation("123", {"condition": "good"})
    print(recommendation)
