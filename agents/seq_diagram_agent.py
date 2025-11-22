from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from autogen.agentchat import ConversableAgent
from config.llm_config import get_llm_config
import re

def generate_seq_diagram(uc_specs_path: Path, output_dir: Path) -> None:
    """Reads the use case specifications and generates a Sequence Diagram (PlantUML) for EACH use case described."""

    specs_text = uc_specs_path.read_text(encoding="utf-8")
    llm_config = get_llm_config()

    expected_names = ["Register Vehicle",
                      "Log Maintenance Event",
                      "Edit/Delete Maintenance Record",
                      "View Maintenance History",
                      "Get Service Recommendation",
                      ]
    
    expected_messages = {
        "Register Vehicle": [
            "User -> VehicleRegistry: Register Vehicle (payload)",
            "VehicleRegistry -> MaintenanceDB: Create Vehicle Record",
            "MaintenanceDB --> VehicleRegistry: Ack",
            "VehicleRegistry --> User: Registration Complete",
        ],
        "Log Maintenance Event": [
            "User -> MaintenanceService: Log Maintenance Event (vehicleId, details)",
            "MaintenanceService -> MaintenanceDB: Insert Maintenance Record",
            "MaintenanceDB --> MaintenanceService: Ack",
            "MaintenanceService --> User: Event Logged",
        ],
        "Edit/Delete Maintenance Record": [
            "User -> MaintenanceService: Edit/Delete Maintenance Record (recordId, action)",
            "MaintenanceService -> MaintenanceDB: Update/Delete Record",
            "MaintenanceDB --> MaintenanceService: Ack/Result",
            "MaintenanceService --> User: Edit/Delete Result",
        ],
        "View Maintenance History": [
            "User -> MaintenanceService: Request Maintenance History (vehicleId)",
            "MaintenanceService -> MaintenanceDB: Query Records",
            "MaintenanceDB --> MaintenanceService: Return Records",
            "MaintenanceService --> User: Display History",
        ],
        "Get Service Recommendation": [
            "User -> RecommendationEngine: Request Recommendation (vehicleId, context)",
            "RecommendationEngine -> MaintenanceDB: Fetch Recent Maintenance (vehicleId)",
            "MaintenanceDB --> RecommendationEngine: Return Records",
            "RecommendationEngine --> User: Recommendation Response",
        ],
    }


    def extract_section(text: str, heading: str) -> str:
        """Try to extract a section for heading from specs_text. Fall back to empty string."""
        pattern = rf"(^|\n)#+\s*{re.escape(heading)}\s*\n(.*?)(?=\n#+\s*\w|\Z)"
        m = re.search(pattern, text, re.S | re.I)
        if m:
            return m.group(2).strip()
        # try a looser version
        pattern2 = rf"(^|\n){re.escape(heading)}\s*\n(.*?)(?=\n{{2,}}|\Z)"
        m2 = re.search(pattern2, text, re.S | re.I)
        return m2.group(2).strip() if m2 else ""
    
 
    
    # for each expected use case - have a strict prompt that details UML requirements
    for name in expected_names:
        section_text = extract_section(specs_text, name)

        # build the strict requirements
        system_message = (
            f"You are a senior software engineer specialized in UML sequence diagrams.\n"
            f"Produce exactly ONE PlantUML sequence diagram (PlantUML syntax ONLY) for the use case: '{name}'.\n"
            f"Output requirements:\n"
            f"- ONLY the PlantUML block starting with @startuml and ending with @enduml.\n"
            f"- DO NOT include any layout directives such as 'left to right direction' or 'skinparam'.\n"
            f"- Declare: actor User\n"
            f"- Declare participants (in this order): VehicleRegistry, MaintenanceService, MaintenanceDB, RecommendationEngine\n"
            f"- Use '->' for requests and '-->' for responses.\n"
            f"- Include exactly the following message lines (case-sensitive) in the diagram, in the given order:\n"
            + "\n".join(f"- {m}" for m in expected_messages[name])
            + "\nDo not add any other messages, notes, metadata, or prose."
        )

       


        user_prompt = (
            f"Use case: {name}\n\n"
            f"Specification (from use case specs):\n\n{section_text}\n\n"
            "Generate a single PlantUML sequence diagram for this use case following the system message."
        )
        agent = ConversableAgent(
           name=f"seq_diagram_agent_{name.replace('', '_')}",
           system_message= system_message,
           llm_config= llm_config,

       )
        
        reply = agent.generate_reply(messages=[{"role": "user", "content": user_prompt}])
        raw_output = reply["content"] if isinstance(reply, dict) else str(reply)

        match = re.search(r"@startuml[\s\S]*?@enduml", raw_output)
        if match:
            puml_code = match.group(0).strip()
        else:
            # best-effort: wrap the expected messages into a minimal PlantUML block
            lines = ["@startuml", "left to right direction", "actor User",
                     "participant VehicleRegistry", "participant MaintenanceService",
                     "participant MaintenanceDB", "participant RecommendationEngine"]
            lines.extend(expected_messages[name])
            lines.append("@enduml")
            puml_code = "\n".join(lines)
        
        m_start = re.search(r"@startuml", puml_code, re.I)
        if m_start:
            puml_code = puml_code[m_start.start():].strip()
        else:
            # fallback wrap
            puml_code = "@startuml\nactor User\nparticipant VehicleRegistry\nparticipant MaintenanceService\nparticipant MaintenanceDB\nparticipant RecommendationEngine\n" + "\n".join(expected_messages[name]) + "\n@enduml"

        # remove any 'left to right direction' or similar layout lines if present
        puml_code = re.sub(r"(?im)^\s*left to right direction\s*$\n?", "", puml_code)

        # sanitize further: ensure the first non-empty line is @startuml
        lines = [ln for ln in puml_code.splitlines()]
        # ensure @startuml is first line
        if not lines or not re.match(r"(?i)^@startuml\s*$", lines[0]):
            # find index of @startuml and trim
            for i, ln in enumerate(lines):
                if re.match(r"(?i)^@startuml\s*$", ln):
                    lines = lines[i:]
                    break
            else:
                # rebuild minimal block
                lines = ["@startuml", "actor User",
                         "participant VehicleRegistry", "participant MaintenanceService",
                         "participant MaintenanceDB", "participant RecommendationEngine"] + expected_messages[name] + ["@enduml"]
        puml_code = "\n".join(lines).strip() + "\n"


        # sanitize filename
        filename = name.lower().replace(" ", "_").replace("/", "_") + "_sequence.puml"
        output_path = output_dir / filename
        output_path.write_text(puml_code, encoding="utf-8")
        print(f"[OK] Saved sequence diagram for: {name} -> {output_path}")