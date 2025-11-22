from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from autogen.agentchat import ConversableAgent

from config.llm_config import get_llm_config

def generate_class_diagram(uc_specs_path: Path, output_path: Path) -> None:
    """Reads the system summary and asks an LLM agent to generate a UML-style use case diagram description"""

    class_text = uc_specs_path.read_text(encoding="utf-8")
    llm_config = get_llm_config()
   


    agent = ConversableAgent(
        name="class_diagram_agent",
        llm_config=llm_config,
        system_message=(
            "You are an expert software engineer. "
            "Your ONLY task is to output a VALID PlantUML CLASS DIAGRAM.\n\n"
            
            "STRICT REQUIREMENTS:\n"
            "- Output ONLY a PlantUML block.\n"
            "- First line MUST be: @startuml\n"
            "- Last line MUST be: @enduml\n"
            "- No markdown, no code fences, no explanation.\n\n"

            "CONTENT RULES:\n"
            "- Include these classes:\n"
            "    User\n"
            "    Vehicle\n"
            "    MaintenanceRecord\n"
            "    RecommendationService\n"
            "    MaintenanceDB\n"
            "- Include attributes (+ public, - private) and basic types.\n"
            "- Include at least 1–2 methods per class.\n"
            "- Include associations with multiplicities:\n"
            "    User \"1\" -- \"*\" Vehicle\n"
            "    Vehicle \"1\" *-- \"*\" MaintenanceRecord\n"
            "- Include RecommendationService ..> Vehicle : analyzes\n"
            "- Include MaintenanceDB ..> MaintenanceRecord : stores\n"
            "- DO NOT invent unrelated classes.\n"
    )
)

    user_prompt = f"""
Here is the the system summary:

\"\"\"{class_text}\"\"\"

Generate a comprehensive PlantUML class diagram for this system following the system message instructions. Output ONLY the PlantUML block.
"""

    reply = agent.generate_reply(
        messages=[{"role": "user", "content": user_prompt}]
    )
    

    specs_text = reply["content"] if isinstance(reply, dict) else str(reply)
    
    
    import re
    match = re.search(r"@startuml[\s\S]*?@enduml", specs_text, re.I)
    if match:
        specs_text = match.group(0).strip()
        print(f"[OK] Extracted PlantUML block: {len(specs_text)} chars")
    else:
        print("[WARNING] No @startuml...@enduml block found in agent reply!")
        print(f"[DEBUG] Reply preview: {specs_text[:300]}")

    output_path.write_text(specs_text, encoding="utf-8")
    print(f"[OK] Class Diagram saved to: {output_path}")

        