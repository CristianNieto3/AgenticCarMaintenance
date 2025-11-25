<<<<<<< HEAD
work in progress :)
=======
# Agentic Car Maintenance Tracking System

An AI-powered system that automatically generates software artifacts (UML diagrams, specifications, and executable code) from a high-level system summary using multi-agent collaboration patterns.

## Overview

This project demonstrates **4 required agentic AI patterns** to automatically transform a system description into a working application:

1. **Tool-based agents** - Date calculation functions (`calculate_service_due_date`, `days_since_last_service`)
2. **Coding agents** - Generates and executes Python code with syntax validation
3. **Multi-agent collaboration** - Architect → Coder → Tester pipeline
4. **Observer/Reflection** - Code reviewer provides feedback, coder refines implementation

## Project Structure

```
HW3/
├── agents/                          # Agent implementations
│   ├── uc_diagram_agent.py         # Use case diagram generator
│   ├── uc_specs_agent.py           # Use case specifications generator
│   ├── seq_diagram_agent.py        # Sequence diagram generator (5 diagrams)
│   ├── class_diagram_agent.py      # Class diagram generator
│   └── code_gen_agent.py           # Code generation orchestrator (4 patterns)
├── config/
│   └── llm_config.py               # LLM configuration (Ollama/local model)
├── generated/                       # All generated artifacts
│   ├── diagrams/
│   │   ├── use_case_diagram.puml
│   │   ├── class_diagram.puml
│   │   └── sequence/               # 5 sequence diagrams
│   ├── specs/
│   │   └── use_case_specs.md
│   └── code/                        # Executable application
│       ├── models.py
│       ├── persistence.py
│       ├── services.py
│       ├── cli_app.py              # Interactive CLI
│       ├── test_app.py             # Automated tests
│       └── README.md
├── summary/
│   └── system_summary.txt          # Input: high-level system description
├── main.py                          # Main orchestration pipeline
├── requirements.txt
└── README.md                        # This file
```

## Requirements

### Software
- Python 3.10+
- [Ollama](https://ollama.ai/) with `deepseek-coder-v2:16b` model installed

### Python Dependencies
```bash
pip install -r requirements.txt
```

Dependencies:
- `autogen-agentchat` - Multi-agent framework
- `autogen-core` - Core AutoGen functionality
- `autogen-ext[ollama]` - Ollama integration
- `python-dotenv` - Environment variable management

## Setup

1. **Install Ollama and pull the model:**
   ```bash
   ollama pull deepseek-coder-v2:16b
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/CristianNieto3/AgenticCarMaintenance.git
   cd AgenticCarMaintenance
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Ollama is running:**
   ```bash
   ollama list  # Should show deepseek-coder-v2:16b
   ```

## Usage

### Generate All Artifacts (Full Pipeline)

Run the complete pipeline to generate diagrams, specs, and executable code:

```bash
python main.py
```

This will:
1. Generate use case diagram from `summary/system_summary.txt`
2. Generate use case specifications
3. Generate 5 sequence diagrams (one per use case)
4. Generate class diagram
5. Generate executable Python code using 4 agentic patterns

All outputs are saved to `generated/`

### Run the Generated Application

```bash
cd generated/code
python cli_app.py
```

**Menu options:**
1. Register Vehicle
2. Log Maintenance Event
3. Edit/Delete Maintenance Record
4. View Maintenance History
5. Get Service Recommendation
6. Exit

### Run Automated Tests

```bash
cd generated/code
python test_app.py
```

Expected output: `ALL TESTS PASSED ✓` (14 tests)

## Agentic Patterns Implementation

### 1. Tool-based Agents
**Location:** `agents/code_gen_agent.py` (lines 19-28)

Two date calculation tools:
- `calculate_service_due_date(last_service, months)` - Calculates next service date
- `days_since_last_service(last_service)` - Calculates days since last maintenance

These tools are invoked and their results are included in agent prompts to demonstrate tool usage.

### 2. Coding Agents
**Location:** `agents/code_gen_agent.py` (lines 62-88)

- `write_code()` - Generates Python files and validates syntax using `py_compile`
- `execute_code()` - Executes generated code and captures stdout/stderr/returncode

Demonstrates code generation → validation → execution pipeline.

### 3. Multi-agent Collaboration
**Location:** `agents/code_gen_agent.py` (lines 129-165)

Three-agent pipeline for each use case:
1. **Architect Agent** - Reads sequence diagram, produces class structure outline
2. **Coder Agent** - Implements the outline as executable Python code
3. **Tester Agent** - Generates test cases for the implementation

Agents pass outputs sequentially, each building on the previous agent's work.

### 4. Observer/Reflection
**Location:** `agents/code_gen_agent.py` (lines 167-233)

- **Reviewer Agent** - Analyzes generated code and execution results, provides feedback
- **Reflection Loop** - If code is not approved, Coder agent refines implementation based on feedback

Demonstrates evaluate → feedback → refine pattern (one iteration).

## Generated Artifacts

### UML Diagrams (PlantUML format)
- **Use Case Diagram:** Shows 5 use cases and User actor
- **Class Diagram:** Shows Vehicle, MaintenanceRecord, services, and relationships
- **Sequence Diagrams (5):**
  - Register Vehicle
  - Log Maintenance Event
  - Edit/Delete Maintenance Record
  - View Maintenance History
  - Get Service Recommendation

### Specifications
- **Use Case Specifications:** Detailed specs with preconditions, postconditions, main flows, and alternate flows

### Executable Code
- **models.py:** Vehicle and MaintenanceRecord data classes
- **persistence.py:** JSON-based database layer
- **services.py:** Business logic (VehicleRegistry, MaintenanceService, RecommendationEngine)
- **cli_app.py:** Interactive command-line interface
- **test_app.py:** 14 automated tests covering all use cases

## Example Workflow

1. **Run the pipeline:**
   ```bash
   python main.py
   ```

2. **Test the generated code:**
   ```bash
   cd generated/code
   python test_app.py
   # Expected: ALL TESTS PASSED ✓
   ```

3. **Use the application:**
   ```bash
   python cli_app.py
   # Register a vehicle: V001, Toyota Camry 2020, VIN: 1HGCM82633A123456
   # Log maintenance: Oil Change on 2024-06-15, $45.99
   # View history for V001
   # Get recommendation for V001
   ```

4. **Data persistence:**
   - Data is saved to `maintenance_db.json`
   - Survives application restarts

## Assignment Requirements Compliance

This project fulfills all requirements:

✅ **Tool-based agents** - Date calculation functions  
✅ **Coding agents** - Generates and executes Python code  
✅ **Multi-agent collaboration** - Architect → Coder → Tester pipeline  
✅ **Observer/reflection** - Reviewer provides feedback, Coder refines  
✅ **Runnable application** - CLI with all 5 use cases integrated  
✅ **Automated tests** - 14 tests covering all functionality  
✅ **Complete documentation** - READMEs, code comments, diagrams  

## Troubleshooting

**Issue:** `Unable to import 'autogen.agentchat'`  
**Solution:** Install dependencies: `pip install -r requirements.txt`

**Issue:** Agent returns empty responses  
**Solution:** Verify Ollama is running and model is loaded: `ollama list`

**Issue:** `max_tokens` too small  
**Solution:** Already set to 4096 in `config/llm_config.py`

**Issue:** Tests fail  
**Solution:** Check that `generated/code/` contains all 5 files (models, persistence, services, cli_app, test_app)

## Author

Cristian Nieto  
GitHub: [@CristianNieto3](https://github.com/CristianNieto3)

## License

Educational project for coursework.
>>>>>>> e7e23b8 (Completed agentic car maintenance system with 4 agentic SWE patterns)
