"""Service layer for the Car Maintenance System."""
from datetime import datetime, timedelta
from typing import List, Optional
from models import Vehicle, MaintenanceRecord
from persistence import MaintenanceDB


class VehicleRegistry:
    """Handles vehicle registration operations."""
    
    def __init__(self, db: MaintenanceDB):
        self.db = db
    
    def register_vehicle(self, vehicle_id: str, make: str, model: str, year: int, vin: str) -> tuple:
        """Register a new vehicle."""
        # Check if VIN already exists
        existing_vehicles = self.db.get_all_vehicles()
        for v in existing_vehicles:
            if v.vin == vin:
                return False, "VIN already registered"
        
        vehicle = Vehicle(vehicle_id, make, model, year, vin)
        success = self.db.create_vehicle_record(vehicle)
        
        if success:
            return True, "Vehicle registered successfully"
        return False, "Vehicle ID already exists"


class MaintenanceService:
    """Handles maintenance record operations."""
    
    def __init__(self, db: MaintenanceDB):
        self.db = db
    
    def log_maintenance_event(self, vehicle_id: str, record_id: str, date: str,
                              service_type: str, description: str, cost: float, 
                              mileage: Optional[int] = None) -> tuple:
        """Log a new maintenance event."""
        # Check if vehicle exists
        vehicle = self.db.get_vehicle(vehicle_id)
        if not vehicle:
            return False, "Vehicle not registered"
        
        record = MaintenanceRecord(record_id, vehicle_id, date, service_type, 
                                   description, cost, mileage)
        success = self.db.insert_maintenance_record(record)
        
        if success:
            return True, "Maintenance event logged successfully"
        return False, "Failed to log maintenance event"
    
    def edit_maintenance_record(self, record_id: str, **updates) -> tuple:
        """Edit an existing maintenance record."""
        # Get existing record
        all_records = []
        for vehicle in self.db.get_all_vehicles():
            all_records.extend(self.db.query_records(vehicle.vehicle_id))
        
        record = None
        for r in all_records:
            if r.record_id == record_id:
                record = r
                break
        
        if not record:
            return False, "Record not found"
        
        # Update fields
        for key, value in updates.items():
            if hasattr(record, key):
                setattr(record, key, value)
        
        success = self.db.update_maintenance_record(record)
        if success:
            return True, "Record updated successfully"
        return False, "Failed to update record"
    
    def delete_maintenance_record(self, record_id: str) -> tuple:
        """Delete a maintenance record."""
        success = self.db.delete_maintenance_record(record_id)
        if success:
            return True, "Record deleted successfully"
        return False, "Record not found"
    
    def view_maintenance_history(self, vehicle_id: str) -> tuple:
        """View all maintenance history for a vehicle."""
        vehicle = self.db.get_vehicle(vehicle_id)
        if not vehicle:
            return False, "Vehicle not found"
        
        records = self.db.query_records(vehicle_id)
        return True, records


class RecommendationEngine:
    """Provides service recommendations based on maintenance history."""
    
    def __init__(self, db: MaintenanceDB):
        self.db = db
    
    def get_service_recommendation(self, vehicle_id: str) -> tuple:
        """Get service recommendation for a vehicle."""
        vehicle = self.db.get_vehicle(vehicle_id)
        if not vehicle:
            return False, "Vehicle not found"
        
        records = self.db.query_records(vehicle_id)
        
        if not records:
            return True, "Recommend initial inspection and oil change"
        
        # Get most recent maintenance
        recent_record = records[0]
        recent_date = datetime.strptime(recent_record.date, "%Y-%m-%d")
        days_since = (datetime.now() - recent_date).days
        
        recommendations = []
        
        if days_since > 180:
            recommendations.append("Major service overdue (6+ months since last service)")
        elif days_since > 90:
            recommendations.append("Schedule maintenance check-up soon")
        
        # Check mileage-based recommendations
        if recent_record.mileage:
            if recent_record.mileage > 5000:
                recommendations.append("Oil change recommended (based on mileage)")
        
        if not recommendations:
            recommendations.append("Vehicle maintenance is up to date")
        
        return True, recommendations
