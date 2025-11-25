"""Command-line interface for the Car Maintenance System."""
import sys
from datetime import datetime
from persistence import MaintenanceDB
from services import VehicleRegistry, MaintenanceService, RecommendationEngine


def print_menu():
    """Display the main menu."""
    print("\n" + "="*60)
    print("Car Maintenance Tracking System")
    print("="*60)
    print("1. Register Vehicle")
    print("2. Log Maintenance Event")
    print("3. Edit/Delete Maintenance Record")
    print("4. View Maintenance History")
    print("5. Get Service Recommendation")
    print("6. Exit")
    print("="*60)


def register_vehicle(registry: VehicleRegistry):
    """Handle vehicle registration."""
    print("\n--- Register Vehicle ---")
    vehicle_id = input("Enter Vehicle ID: ").strip()
    make = input("Enter Make: ").strip()
    model = input("Enter Model: ").strip()
    year = input("Enter Year: ").strip()
    vin = input("Enter VIN (17 characters): ").strip()
    
    try:
        year = int(year)
        success, message = registry.register_vehicle(vehicle_id, make, model, year, vin)
        print(f"\n{message}")
    except ValueError:
        print("\nError: Year must be a number")


def log_maintenance(service: MaintenanceService):
    """Handle logging maintenance event."""
    print("\n--- Log Maintenance Event ---")
    vehicle_id = input("Enter Vehicle ID: ").strip()
    record_id = input("Enter Record ID: ").strip()
    date = input("Enter Date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    service_type = input("Enter Service Type (Oil Change, Tire Rotation, etc.): ").strip()
    description = input("Enter Description: ").strip()
    cost = input("Enter Cost: ").strip()
    mileage = input("Enter Mileage (optional, press Enter to skip): ").strip()
    
    try:
        cost = float(cost)
        mileage = int(mileage) if mileage else None
        success, message = service.log_maintenance_event(
            vehicle_id, record_id, date, service_type, description, cost, mileage
        )
        print(f"\n{message}")
    except ValueError:
        print("\nError: Invalid cost or mileage value")


def edit_delete_record(service: MaintenanceService):
    """Handle editing or deleting maintenance records."""
    print("\n--- Edit/Delete Maintenance Record ---")
    print("1. Edit Record")
    print("2. Delete Record")
    choice = input("Choose option: ").strip()
    
    if choice == "1":
        record_id = input("Enter Record ID to edit: ").strip()
        print("Enter new values (press Enter to keep current value):")
        
        updates = {}
        new_date = input("New Date (YYYY-MM-DD): ").strip()
        if new_date:
            updates["date"] = new_date
        
        new_service = input("New Service Type: ").strip()
        if new_service:
            updates["service_type"] = new_service
        
        new_desc = input("New Description: ").strip()
        if new_desc:
            updates["description"] = new_desc
        
        new_cost = input("New Cost: ").strip()
        if new_cost:
            try:
                updates["cost"] = float(new_cost)
            except ValueError:
                print("Invalid cost value")
                return
        
        new_mileage = input("New Mileage: ").strip()
        if new_mileage:
            try:
                updates["mileage"] = int(new_mileage)
            except ValueError:
                print("Invalid mileage value")
                return
        
        if updates:
            success, message = service.edit_maintenance_record(record_id, **updates)
            print(f"\n{message}")
        else:
            print("\nNo changes made")
    
    elif choice == "2":
        record_id = input("Enter Record ID to delete: ").strip()
        confirm = input(f"Are you sure you want to delete record {record_id}? (yes/no): ").strip().lower()
        if confirm == "yes":
            success, message = service.delete_maintenance_record(record_id)
            print(f"\n{message}")
        else:
            print("\nDeletion cancelled")
    else:
        print("\nInvalid option")


def view_history(service: MaintenanceService):
    """Handle viewing maintenance history."""
    print("\n--- View Maintenance History ---")
    vehicle_id = input("Enter Vehicle ID: ").strip()
    
    success, result = service.view_maintenance_history(vehicle_id)
    
    if not success:
        print(f"\n{result}")
        return
    
    records = result
    if not records:
        print("\nNo maintenance records found for this vehicle")
        return
    
    print(f"\nMaintenance History for Vehicle {vehicle_id}:")
    print("-" * 80)
    for record in records:
        print(f"Record ID: {record.record_id}")
        print(f"Date: {record.date}")
        print(f"Service Type: {record.service_type}")
        print(f"Description: {record.description}")
        print(f"Cost: ${record.cost:.2f}")
        if record.mileage:
            print(f"Mileage: {record.mileage}")
        print("-" * 80)


def get_recommendation(engine: RecommendationEngine):
    """Handle getting service recommendations."""
    print("\n--- Get Service Recommendation ---")
    vehicle_id = input("Enter Vehicle ID: ").strip()
    
    success, result = engine.get_service_recommendation(vehicle_id)
    
    if not success:
        print(f"\n{result}")
        return
    
    recommendations = result
    print("\nService Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")


def main():
    """Main application loop."""
    # Initialize database and services
    db = MaintenanceDB("maintenance_db.json")
    registry = VehicleRegistry(db)
    service = MaintenanceService(db)
    engine = RecommendationEngine(db)
    
    print("\nWelcome to the Car Maintenance Tracking System!")
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            register_vehicle(registry)
        elif choice == "2":
            log_maintenance(service)
        elif choice == "3":
            edit_delete_record(service)
        elif choice == "4":
            view_history(service)
        elif choice == "5":
            get_recommendation(engine)
        elif choice == "6":
            print("\nThank you for using the Car Maintenance Tracking System!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
