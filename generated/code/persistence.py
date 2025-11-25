"""Persistence layer for the Car Maintenance System."""
import json
from pathlib import Path
from typing import Dict, List, Optional
from models import Vehicle, MaintenanceRecord


class MaintenanceDB:
    """Handles data persistence using JSON file storage."""
    
    def __init__(self, db_path: str = "maintenance_db.json"):
        self.db_path = Path(db_path)
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from JSON file."""
        if self.db_path.exists():
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"vehicles": {}, "maintenance_records": {}}
    
    def _save_data(self):
        """Save data to JSON file."""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)
    
    def create_vehicle_record(self, vehicle: Vehicle) -> bool:
        """Create a new vehicle record."""
        if vehicle.vehicle_id in self.data["vehicles"]:
            return False
        self.data["vehicles"][vehicle.vehicle_id] = vehicle.to_dict()
        self._save_data()
        return True
    
    def get_vehicle(self, vehicle_id: str) -> Optional[Vehicle]:
        """Retrieve a vehicle by ID."""
        vehicle_data = self.data["vehicles"].get(vehicle_id)
        if vehicle_data:
            return Vehicle.from_dict(vehicle_data)
        return None
    
    def insert_maintenance_record(self, record: MaintenanceRecord) -> bool:
        """Insert a new maintenance record."""
        self.data["maintenance_records"][record.record_id] = record.to_dict()
        self._save_data()
        return True
    
    def update_maintenance_record(self, record: MaintenanceRecord) -> bool:
        """Update an existing maintenance record."""
        if record.record_id not in self.data["maintenance_records"]:
            return False
        self.data["maintenance_records"][record.record_id] = record.to_dict()
        self._save_data()
        return True
    
    def delete_maintenance_record(self, record_id: str) -> bool:
        """Delete a maintenance record."""
        if record_id in self.data["maintenance_records"]:
            del self.data["maintenance_records"][record_id]
            self._save_data()
            return True
        return False
    
    def query_records(self, vehicle_id: str) -> List[MaintenanceRecord]:
        """Query all maintenance records for a vehicle."""
        records = []
        for record_data in self.data["maintenance_records"].values():
            if record_data["vehicle_id"] == vehicle_id:
                records.append(MaintenanceRecord.from_dict(record_data))
        return sorted(records, key=lambda r: r.date, reverse=True)
    
    def get_all_vehicles(self) -> List[Vehicle]:
        """Get all registered vehicles."""
        return [Vehicle.from_dict(v) for v in self.data["vehicles"].values()]
