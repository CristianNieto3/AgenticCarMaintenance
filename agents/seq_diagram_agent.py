from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from autogen.agentchat import ConversableAgent

from config.llm_config import get_llm_config

def generate_sequence_diagram(summary_path: Path, output_path: Path) -> None:
    """Reads the system summary and asks an LLM agent to generate a sequence diagram (PlantUML)"""

    sequence_summary = summary_path.read_text(encoding="utf-8")
    llm_config = get_llm_config()


    agent = ConversableAgent(
        name="seq_diagram",
        system_message=(
            "You are a senior software engineer specializing in UML diagrams.\n"
            "Your task is to generate a **UML Sequence Diagram** in **PlantUML syntax ONLY**.\n\n"

            "STRICT REQUIREMENTS:\n"
            "- Use ONLY PlantUML.\n"
            "- Begin with @startuml and end with @enduml.\n"
            "- Depict interactions between the User and the System for the main functionalities.\n"
            "- Include lifelines for User and System.\n"
            "- Show messages exchanged in the sequence of operations.\n"
            "- DO NOT add extra text, explanation, comments, or anything outside the diagram.\n\n"

            "OUTPUT FORMAT (example structure):\n"
            "@startuml\n"
            "actor User\n"
            "participant System\n"
            "User -> System: Action\n"
            "System --> User: Response\n"
            "@enduml\n"
            
        ),
        llm_config=llm_config,
    )
    user_prompt = f"""
Here is the system description:

\"\"\"{sequence_summary}\"\"\"

Generate the UML sequence diagram as requested in the system message.
Remember: depict interactions between 'User' and 'System'.
"""

    reply = agent.generate_reply(messages=[{"role": "user", "content": user_prompt}])

    # reply is a dict-like object; extract the text content
    if isinstance(reply, dict) and "content" in reply:
        diagram_text = reply["content"]
    else:
        diagram_text = str(reply)

    output_path.write_text(diagram_text, encoding="utf-8")
    print(f"[OK] Use sequence diagram generated at: {output_path}")

