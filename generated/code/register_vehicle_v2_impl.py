import json
from datetime import datetime, timedelta

class VehicleRegistry:
    def __init__(self):
        self.registry = {}
    
    def register_vehicle(self, payload):
        vehicle_id = payload['vehicle_id']
        if vehicle_id in self.registry:
            return {'status': 'error', 'message': 'Vehicle already registered'}
        else:
            self.registry[vehicle_id] = {}
            return {'status': 'success', 'message': 'Vehicle registered successfully'}
    
    def create_vehicle_record(self, vehicle_id):
        if vehicle_id in self.registry:
            MaintenanceDB().create_vehicle_record(vehicle_id)
            return {'status': 'success', 'message': 'Vehicle record created successfully'}
        else:
            return {'status': 'error', 'message': 'Vehicle not found'}

class MaintenanceService:
    def __init__(self):
        pass
    
    def days_since_last_service(self, last_service_date):
        today = datetime.now()
        delta = today - last_service_date
        return delta.days

class MaintenanceDB:
    def __init__(self):
        self.db = {}
    
    def create_vehicle_record(self, vehicle_id):
        if vehicle_id not in self.db:
            self.db[vehicle_id] = {'last_service_date': datetime.now()}
            return True
        else:
            return False
    
    def get_next_service_due(self, vehicle_id):
        if vehicle_id in self.db:
            last_service_date = self.db[vehicle_id]['last_service_date']
            days_since_last_service = MaintenanceService().days_since_last_service(last_service_date)
            recommended_service_interval = 365  # Assuming a yearly service interval
            days_until_next_service = recommended_service_interval - days_since_last_service
            return {'status': 'success', 'days_until_next_service': days_until_next_service}
        else:
            return {'status': 'error', 'message': 'Vehicle not found'}

class RecommendationEngine:
    def __init__(self):
        pass
    
    def generate_recommendations(self, vehicle_id):
        if MaintenanceDB().get_next_service_due(vehicle_id)['status'] == 'success':
            return {'status': 'success', 'message': 'Vehicle is due for service'}
        else:
            return {'status': 'error', 'message': 'Vehicle not found or no record of last service'}

if __name__ == '__main__':
    registry = VehicleRegistry()
    payload = {'vehicle_id': '12345'}
    print(registry.register_vehicle(payload))
    print(registry.create_vehicle_record('12345'))
    recommendation = RecommendationEngine().generate_recommendations('12345')
    print(recommendation)
