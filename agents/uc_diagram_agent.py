from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from autogen.agentchat import ConversableAgent

from config.llm_config import get_llm_config

def generate_use_case_diagram(summary_path: Path, output_path: Path) -> None:
    """Reads the system summary and asks an LLM agent to generate a UML-style use case diagram description"""

    summary_text = summary_path.read_text(encoding="utf-8")
    llm_config = get_llm_config()


    agent = ConversableAgent(
        name="use_case_diagram",
        system_message=(
            "You are a senior software engineer specializing in UML diagrams.\n"
            "Your task is to generate a **UML Use Case Diagram** in **PlantUML syntax ONLY**.\n\n"

            "STRICT REQUIREMENTS:\n"
            "- Use ONLY PlantUML.\n"
            "- Begin with @startuml and end with @enduml.\n"
            "- Arrange diagram left-to-right.\n"
            "- Define one actor named User.\n"
            "- Include EXACTLY these 5 use cases:\n"
            "    (Register Vehicle)\n"
            "    (Log Maintenance Event)\n"
            "    (Edit/Delete Maintenance Record)\n"
            "    (View Maintenance History)\n"
            "    (Get Service Recommendation)\n"
            "- Show connections: User --> (Use Case Name)\n"
            "- DO NOT add extra text, explanation, comments, or anything outside the diagram.\n\n"

            "OUTPUT FORMAT (example structure):\n"
            "@startuml\n"
            "left to right direction\n"
            "actor User\n"
            "User --> (Example Use Case)\n"
            "@enduml\n"
        ),
        llm_config=llm_config,
    )
    user_prompt = f"""
Here is the system description:

\"\"\"{summary_text}\"\"\"

Generate the UML use case diagram as requested in the system message.
Remember: one actor 'User' and the five specific use cases.
"""

    reply = agent.generate_reply(messages=[{"role": "user", "content": user_prompt}])

    # reply is a dict-like object; extract the text content
    if isinstance(reply, dict) and "content" in reply:
        diagram_text = reply["content"]
    else:
        diagram_text = str(reply)

    output_path.write_text(diagram_text, encoding="utf-8")
    print(f"[OK] Use case diagram generated at: {output_path}")


  
       