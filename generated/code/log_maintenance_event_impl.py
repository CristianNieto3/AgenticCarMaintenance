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
        from datetime import datetime
        current_date = datetime.strptime(current_date, '%Y-%m-%d')
        last_service_date = datetime.strptime(last_service_date, '%Y-%m-%d')
        delta = current_date - last_service_date
        return delta.days

class MaintenanceService:
    def __init__(self, registry: VehicleRegistry):
        self.registry = registry
    
    def log_maintenance_event(self, vehicleId, details):
        self.registry.log_maintenance_event(vehicleId, details)
    
    def insert_maintenance_record(self, record):
        self.registry.insert_maintenance_record(record)

class MaintenanceDB:
    def __init__(self):
        self.records = {}
    
    def insert_record(self, record):
        self.records[record['vehicleId']] = record
    
    def get_last_service_date(self, vehicleId):
        if vehicleId in self.records:
            return self.records[vehicleId]['date']
        return None

class RecommendationEngine:
    def __init__(self):
        self.recommendations = {}
    
    def generate_recommendation(self, vehicleId, last_service_date):
        if last_service_date is None:
            return "Immediate service required"
        from datetime import datetime, timedelta
        current_date = datetime.now()
        recommended_days = 365  # Assuming a yearly recommendation
        next_service_date = last_service_date + timedelta(days=recommended_days)
        if current_date > next_service_date:
            return "Service overdue"
        else:
            return f"Next service recommended in {int((next_service_date - current_date).days)} days"

# Example usage
if __name__ == '__main__':
    registry = VehicleRegistry()
    service = MaintenanceService(registry)
    db = MaintenanceDB()
    engine = RecommendationEngine()
    
    # Log maintenance event
    service.log_maintenance_event('123', {'date': '2022-01-01', 'description': 'Oil change'})
    
    # Insert maintenance record
    db.insert_record({'vehicleId': '123', 'date': '2022-01-01', 'description': 'Oil change'})
    
    # Get days since last service
    days_since_last_service = registry.get_days_since_last_service('123', '2023-04-01')
    print(f"Days since last service: {days_since_last_service}")
    
    # Generate recommendation
    last_service_date = db.get_last_service_date('123')
    recommendation = engine.generate_recommendation('123', datetime.strptime(last_service_date, '%Y-%m-%d'))
    print(recommendation)
