"""Automated tests for the Car Maintenance System."""
from models import Vehicle, MaintenanceRecord
from persistence import MaintenanceDB
from services import VehicleRegistry, MaintenanceService, RecommendationEngine
import os

def run_tests():
    """Run all automated tests for the system."""
    # Clean slate
    test_db = "test_maintenance_db.json"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = MaintenanceDB(test_db)
    vehicle_registry = VehicleRegistry(db)
    maintenance_service = MaintenanceService(db)
    recommendation_engine = RecommendationEngine(db)
    
    print("\n" + "="*60)
    print("Running Automated Tests for Car Maintenance System")
    print("="*60 + "\n")
    
    # Test 1: Register Vehicle
    print("TEST 1: Register Vehicle")
    success, msg = vehicle_registry.register_vehicle("V001", "Toyota", "Camry", 2020, "1HGCM82633A123456")
    assert success, f"Failed: {msg}"
    print(f"✓ {msg}")
    
    # Verify vehicle exists
    vehicle = db.get_vehicle("V001")
    assert vehicle is not None, "Vehicle should exist in database"
    assert vehicle.make == "Toyota", "Make should be Toyota"
    print(f"✓ Vehicle verified in database: {vehicle.year} {vehicle.make} {vehicle.model}\n")
    
    # Test 2: Duplicate VIN should fail
    print("TEST 2: Duplicate VIN Validation")
    success, msg = vehicle_registry.register_vehicle("V002", "Honda", "Civic", 2021, "1HGCM82633A123456")
    assert not success, "Should reject duplicate VIN"
    assert "already registered" in msg.lower(), "Error message should mention VIN already registered"
    print(f"✓ Correctly rejected: {msg}\n")
    
    # Test 3: Register second vehicle with unique VIN
    print("TEST 3: Register Second Vehicle")
    success, msg = vehicle_registry.register_vehicle("V002", "Honda", "Civic", 2021, "2T1BURHE5JC123456")
    assert success, f"Failed: {msg}"
    print(f"✓ {msg}\n")
    
    # Test 4: Log Maintenance Event
    print("TEST 4: Log Maintenance Event")
    success, msg = maintenance_service.log_maintenance_event(
        "V001", "R001", "2024-06-15", "Oil Change", "Regular 5W-30 oil change", 45.99, 50000
    )
    assert success, f"Failed: {msg}"
    print(f"✓ {msg}")
    
    # Verify record exists
    records = db.query_records("V001")
    assert len(records) == 1, "Should have 1 record"
    assert records[0].service_type == "Oil Change", "Service type should match"
    print(f"✓ Record verified: {records[0].service_type} on {records[0].date}\n")
    
    # Test 5: Log maintenance for non-existent vehicle
    print("TEST 5: Log Maintenance for Non-Existent Vehicle")
    success, msg = maintenance_service.log_maintenance_event(
        "V999", "R999", "2024-06-15", "Oil Change", "Test", 50.00
    )
    assert not success, "Should fail for non-existent vehicle"
    assert "not registered" in msg.lower(), "Error should mention vehicle not registered"
    print(f"✓ Correctly rejected: {msg}\n")
    
    # Test 6: View Maintenance History
    print("TEST 6: View Maintenance History")
    success, records = maintenance_service.view_maintenance_history("V001")
    assert success, "Should succeed"
    assert len(records) == 1, f"Should return 1 record, got {len(records)}"
    print(f"✓ Found {len(records)} record(s)")
    print(f"  - {records[0].date}: {records[0].service_type} (${records[0].cost:.2f})\n")
    
    # Test 7: Add multiple maintenance records
    print("TEST 7: Add Multiple Maintenance Records")
    success, msg = maintenance_service.log_maintenance_event(
        "V001", "R002", "2024-09-20", "Tire Rotation", "Rotated all 4 tires", 25.00, 55000
    )
    assert success, f"Failed: {msg}"
    
    success, msg = maintenance_service.log_maintenance_event(
        "V001", "R003", "2024-11-10", "Brake Inspection", "Checked brake pads", 75.00, 58000
    )
    assert success, f"Failed: {msg}"
    print(f"✓ Added 2 more records")
    
    success, records = maintenance_service.view_maintenance_history("V001")
    assert len(records) == 3, f"Should have 3 records, got {len(records)}"
    print(f"✓ Total records for V001: {len(records)}\n")
    
    # Test 8: Edit Maintenance Record
    print("TEST 8: Edit Maintenance Record")
    success, msg = maintenance_service.edit_maintenance_record("R001", cost=49.99, description="Premium synthetic oil change")
    assert success, f"Failed: {msg}"
    print(f"✓ {msg}")
    
    # Verify edit
    records = db.query_records("V001")
    edited_record = [r for r in records if r.record_id == "R001"][0]
    assert edited_record.cost == 49.99, "Cost should be updated"
    assert "synthetic" in edited_record.description.lower(), "Description should be updated"
    print(f"✓ Verified update: ${edited_record.cost:.2f}, {edited_record.description}\n")
    
    # Test 9: Edit non-existent record
    print("TEST 9: Edit Non-Existent Record")
    success, msg = maintenance_service.edit_maintenance_record("R999", cost=100.00)
    assert not success, "Should fail for non-existent record"
    assert "not found" in msg.lower(), "Error should mention record not found"
    print(f"✓ Correctly rejected: {msg}\n")
    
    # Test 10: Get Service Recommendation
    print("TEST 10: Get Service Recommendation")
    success, recommendations = recommendation_engine.get_service_recommendation("V001")
    assert success, "Failed to get recommendations"
    assert isinstance(recommendations, list), "Should return a list"
    assert len(recommendations) > 0, "Should have at least one recommendation"
    print(f"✓ Recommendations for V001:")
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    print()
    
    # Test 11: Recommendation for vehicle with no history
    print("TEST 11: Recommendation for Vehicle with No History")
    success, recommendations = recommendation_engine.get_service_recommendation("V002")
    assert success, "Should succeed"
    assert "initial" in str(recommendations).lower() or "inspection" in str(recommendations).lower(), "Should recommend initial service"
    print(f"✓ Recommendation: {recommendations}\n")
    
    # Test 12: Delete Maintenance Record
    print("TEST 12: Delete Maintenance Record")
    success, msg = maintenance_service.delete_maintenance_record("R002")
    assert success, f"Failed: {msg}"
    print(f"✓ {msg}")
    
    # Verify deletion
    success, records = maintenance_service.view_maintenance_history("V001")
    assert len(records) == 2, f"Should have 2 records after deletion, got {len(records)}"
    assert not any(r.record_id == "R002" for r in records), "R002 should be deleted"
    print(f"✓ Verified deletion: {len(records)} records remain\n")
    
    # Test 13: Delete non-existent record
    print("TEST 13: Delete Non-Existent Record")
    success, msg = maintenance_service.delete_maintenance_record("R999")
    assert not success, "Should fail for non-existent record"
    assert "not found" in msg.lower(), "Error should mention record not found"
    print(f"✓ Correctly rejected: {msg}\n")
    
    # Test 14: View history for non-existent vehicle
    print("TEST 14: View History for Non-Existent Vehicle")
    success, result = maintenance_service.view_maintenance_history("V999")
    assert not success, "Should fail for non-existent vehicle"
    assert "not found" in result.lower(), "Error should mention vehicle not found"
    print(f"✓ Correctly rejected: {result}\n")
    
    # Clean up test database
    if os.path.exists(test_db):
        os.remove(test_db)
    
    print("="*60)
    print("ALL TESTS PASSED ✓")
    print(f"Total Tests: 14")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        run_tests()
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}\n")
        raise
