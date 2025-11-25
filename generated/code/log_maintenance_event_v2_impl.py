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
            return "No maintenance records found."
        records = self.maintenance_records[vehicleId]
        if not records:
            return "No maintenance records found."
        last_record = records[-1]
        last_service_date = last_record['date']
        from datetime import datetime
        try:
            current_date = datetime.strptime(current_date, '%Y-%m-%d')
            last_service_date = datetime.strptime(last_service_date, '%Y-%m-%d')
            delta = current_date - last_service_date
            return f"Days since last service: {delta.days}"
        except ValueError:
            return "Invalid date format."

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
        else:
            return "No maintenance records found."

class RecommendationEngine:
    def __init__(self):
        self.recommendations = {}
    
    def generate_recommendation(self, vehicleId, last_service_date):
        from datetime import datetime, timedelta
        try:
            last_service_date = datetime.strptime(last_service_date, '%Y-%m-%d')
            next_service_date = last_service_date + timedelta(days=365)
            if datetime.now() > next_service_date:
                return f"Vehicle {vehicleId} requires service."
            else:
                return f"Vehicle {vehicleId} does not require immediate service."
        except ValueError:
            return "Invalid date format."

# Example usage
if __name__ == '__main__':
    registry = VehicleRegistry()
    db = MaintenanceDB()
    engine = RecommendationEngine()
    
    # Log maintenance event
    registry.log_maintenance_event('123', {'date': '2022-01-01'})
    registry.log_maintenance_event('123', {'date': '2022-12-31'})
    
    # Insert maintenance record into database
    db.insert_record({'vehicleId': '123', 'date': '2022-12-31'})
    
    # Get days since last service
    current_date = datetime.now().strftime('%Y-%m-%d')
    days_since_last_service = registry.get_days_since_last_service('123', current_date)
    print(days_since_last_service)  # Output: Days since last service: 0
    
    # Generate recommendation
    last_service_date = db.get_last_service_date('123')
    recommendation = engine.generate_recommendation('123', last_service_date)
    print(recommendation)  # Output: Vehicle 123 requires service.
