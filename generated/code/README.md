# Car Maintenance Tracking System

A simple command-line application for tracking vehicle maintenance records, demonstrating 4 agentic AI patterns.

## Features

- Register vehicles with make, model, year, and VIN
- Log maintenance events with date, service type, cost, and mileage
- Edit or delete existing maintenance records
- View complete maintenance history for any vehicle
- Get service recommendations based on maintenance history

## Installation

No external dependencies required - uses Python standard library only.

## Usage

Run the application:

```bash
cd generated/code
python cli_app.py
```

### Menu Options

1. **Register Vehicle** - Add a new vehicle to the system
2. **Log Maintenance Event** - Record a maintenance service
3. **Edit/Delete Maintenance Record** - Modify or remove records
4. **View Maintenance History** - Display all records for a vehicle
5. **Get Service Recommendation** - Get maintenance suggestions
6. **Exit** - Close the application

## Data Storage

Data is persisted in `maintenance_db.json` in the same directory as the application.

## Example Workflow

1. Register a vehicle (e.g., Vehicle ID: V001, Make: Toyota, Model: Camry, Year: 2020, VIN: 1HGCM82633A004352)
2. Log maintenance event (e.g., Oil Change on 2024-06-01, cost $50)
3. View maintenance history for V001
4. Get service recommendation for V001

## Agentic Patterns Demonstrated

This application was generated using 4 agentic AI patterns:

1. **Tool-based agents** - Date calculation functions
2. **Coding agents** - Generates and executes Python code
3. **Multi-agent collaboration** - Architect → Coder → Tester pipeline
4. **Observer/Reflection** - Code reviewer provides feedback, coder refines

## Files

- `models.py` - Data models (Vehicle, MaintenanceRecord)
- `persistence.py` - Database layer (JSON file storage)
- `services.py` - Business logic (VehicleRegistry, MaintenanceService, RecommendationEngine)
- `cli_app.py` - Command-line interface
