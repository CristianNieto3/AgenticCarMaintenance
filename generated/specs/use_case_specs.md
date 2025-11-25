 ## Register Vehicle
- **Use Case Name:** Register Vehicle
- **Brief Description:** Allows the user to register a new vehicle by entering details such as make, model, year, and VIN.
- **Primary Actor:** User
- **Preconditions:** None
- **Postconditions:** The vehicle is added to the user's vehicle registry with all necessary details recorded.
- **Main Success Scenario:**
  1. User selects "Register Vehicle" from the main menu.
  2. System prompts for vehicle make, model, year, and VIN.
  3. User enters the required information.
  4. System confirms the registration of the vehicle with a success message.
- **Alternate / Exception Flows:**
  - If the entered VIN is already registered or invalid, the system displays an error message and prompts for correct details.

## Log Maintenance Event
- **Use Case Name:** Log Maintenance Event
- **Brief Description:** Enables the user to log a maintenance event for their vehicle, including services performed and parts replaced.
- **Primary Actor:** User
- **Preconditions:** The vehicle must be registered in the system.
- **Postconditions:** A new record of the maintenance event is added to the vehicle's maintenance history.
- **Main Success Scenario:**
  1. User selects "Log Maintenance Event" from the main menu.
  2. System prompts for details about the maintenance event, such as date, service performed, and parts replaced.
  3. User enters the required information.
  4. System confirms the addition of the maintenance record with a success message.
- **Alternate / Exception Flows:**
  - If the entered data is incomplete or incorrect, the system displays an error message and prompts for correct details.

## Edit/Delete Maintenance Record
- **Use Case Name:** Edit/Delete Maintenance Record
- **Brief Description:** Allows the user to edit or delete existing maintenance records for their vehicles.
- **Primary Actor:** User
- **Preconditions:** The vehicle must be registered in the system, and there must be at least one maintenance record available.
- **Postconditions:** The selected maintenance record is either updated or deleted from the vehicle's maintenance history.
- **Main Success Scenario:**
  1. User selects "Edit/Delete Maintenance Record" from the main menu.
  2. System lists all maintenance records associated with the user’s vehicles.
  3. User selects a record to edit or delete.
  4. If editing, system prompts for updated information and confirms changes.
  5. If deleting, system confirms the deletion of the selected record.
- **Alternate / Exception Flows:**
  - If no maintenance records are found, the system displays a message indicating there are no records to edit or delete.

## View Maintenance History
- **Use Case Name:** View Maintenance History
- **Brief Description:** Allows the user to view the detailed history of all maintenance events for their vehicles.
- **Primary Actor:** User
- **Preconditions:** The vehicle must be registered in the system, and there must be at least one maintenance record available.
- **Postconditions:** The user is presented with a detailed report of all maintenance records associated with their vehicles.
- **Main Success Scenario:**
  1. User selects "View Maintenance History" from the main menu.
  2. System lists all registered vehicles and their respective maintenance history.
  3. User can view details for each vehicle's maintenance events.
- **Alternate / Exception Flows:**
  - If no vehicles are registered, the system displays a message indicating there are no vehicles to display records for.

## Get Service Recommendation
- **Use Case Name:** Get Service Recommendation
- **Brief Description:** Provides recommendations for future services based on the vehicle's maintenance history and mileage.
- **Primary Actor:** User
- **Preconditions:** The vehicle must be registered in the system, and there must be at least one maintenance record available.
- **Postconditions:** The user receives personalized service recommendations tailored to their vehicle’s condition and usage.
- **Main Success Scenario:**
  1. User selects "Get Service Recommendation" from the main menu.
  2. System analyzes the vehicle's maintenance history and mileage.
  3. Based on analysis, system recommends upcoming services or parts replacement.
  4. User is informed of recommended actions with details provided.
- **Alternate / Exception Flows:**
  - If no data is available for analysis, the system may display a generic recommendation based on typical vehicle maintenance schedules.