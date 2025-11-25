"""Data models for the Car Maintenance System."""
from datetime import datetime
from typing import Optional


class Vehicle:
    """Represents a vehicle in the system."""
    
    def __init__(self, vehicle_id: str, make: str, model: str, year: int, vin: str):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.vin = vin
    
    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "vin": self.vin
        }
    
    @staticmethod
    def from_dict(data):
        return Vehicle(
            data["vehicle_id"],
            data["make"],
            data["model"],
            data["year"],
            data["vin"]
        )


class MaintenanceRecord:
    """Represents a maintenance record for a vehicle."""
    
    def __init__(self, record_id: str, vehicle_id: str, date: str, 
                 service_type: str, description: str, cost: float, mileage: Optional[int] = None):
        self.record_id = record_id
        self.vehicle_id = vehicle_id
        self.date = date
        self.service_type = service_type
        self.description = description
        self.cost = cost
        self.mileage = mileage
    
    def to_dict(self):
        return {
            "record_id": self.record_id,
            "vehicle_id": self.vehicle_id,
            "date": self.date,
            "service_type": self.service_type,
            "description": self.description,
            "cost": self.cost,
            "mileage": self.mileage
        }
    
    @staticmethod
    def from_dict(data):
        return MaintenanceRecord(
            data["record_id"],
            data["vehicle_id"],
            data["date"],
            data["service_type"],
            data["description"],
            data["cost"],
            data.get("mileage")
        )
