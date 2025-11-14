from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from autogen.agentchat import ConversableAgent

from config.llm_config import get_llm_config

def generate_use_case_specs(uc_diagram_path: Path, output_path: Path) -> None:
    """Reads the system summary and asks an LLM agent to generate a UML-style use case diagram description"""

    diagram_text = uc_diagram_path.read_text(encoding="utf-8")
    llm_config = get_llm_config()


    agent = ConversableAgent(
        name="use_case_spec_agent",
        system_message=(
            "You are a senior software engineer specializing writing formal use case specifications.\n"
            "INPUT: A UML use case diagram in PlantUML" \
            "OUTPUT: A structured use case specification for EACH use case." \
            "For each use case, include these fields:" \
            "- Use Case Name\n"
            "- Brief Description\n"
            "- Primary Actor (should be User)\n"
            "- Preconditions\n"
            "- Postconditions\n"
            "- Main Success Scenario (numbered steps)\n"
            "- Alternate / Exception Flows (if any)\n\n"
            "Write the result in clear Markdown, with a level-2 heading (##) per use case.\n"
            "Do NOT invent new use cases. Only document the ones in the diagram."
        ),
        llm_config=llm_config,
    )

    user_prompt = f"""
Here is the UML use case diagram (PlantUML):

\"\"\"{diagram_text}\"\"\"

Generate the use case specifications as described. Output Markdown only.
"""

    reply = agent.generate_reply(
        messages=[{"role": "user", "content": user_prompt}]
    )

    specs_text = reply["content"] if isinstance(reply, dict) else str(reply)
    output_path.write_text(specs_text, encoding="utf-8")

    print(f"[OK] Use case specifications generated at: {output_path}")
        