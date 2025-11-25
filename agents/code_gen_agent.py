from pathlib import Path
from autogen.agentchat import ConversableAgent
import sys
import subprocess
import re
from typing import Dict, Optional
from datetime import datetime, timedelta
from config.llm_config import get_llm_config

# Demonstrates all 4 agentic patterns:
# 1) Tool-based agent (date calculation tools)
# 2) Coding agent (generates executable Python)
# 3) Multi-agent collaboration (Architect -> Coder -> Tester)
# 4) Observer/reflection (CodeReviewer provides feedback, Coder refines)

llm_config = get_llm_config()

# --- PATTERN 1: Tool-based agent functions ---
def calculate_service_due_date(last_service: str, months: int = 6) -> str:
    """Tool: calculates next service due date."""
    last = datetime.strptime(last_service, "%Y-%m-%d")
    next_date = last + timedelta(days=30*months)
    return next_date.strftime("%Y-%m-%d")

def days_since_last_service(last_service: str) -> int:
    """Tool: calculates days since last service."""
    last = datetime.strptime(last_service, "%Y-%m-%d")
    return (datetime.now() - last).days

# --- Helper: run agent and extract reply ---
def ask_agent(name: str, system_msg: str, user_msg: str) -> str:
    """Creates an agent, sends a message, and returns the response content."""
    agent = ConversableAgent(name=name, system_message=system_msg, llm_config=llm_config)
    reply = agent.generate_reply(messages=[{"role": "user", "content": user_msg}])
    content = reply.get("content", "") if isinstance(reply, dict) else str(reply)
    return content.strip()

# --- Load sequence diagrams ---
def load_sequence_diagrams(seq_dir: Path) -> Dict[str, str]:
    """Loads all .puml files from sequence directory and extracts PlantUML blocks."""
    diagrams = {}
    if not seq_dir.exists():
        return diagrams
    
    for f in sorted(seq_dir.glob("*.puml")):
        raw = f.read_text(encoding="utf-8-sig")
        m = re.search(r"@startuml[\s\S]*?@enduml", raw, re.I)
        if m:
            name = f.stem.replace("_sequence", "").replace("_", " ").title()
            diagrams[name] = m.group(0).strip()
    return diagrams

# --- PATTERN 2: Coding agent with code executor ---
def write_code(output_dir: Path, name: str, code: str) -> Optional[Path]:
    """Writes code to file and syntax-checks it."""
    target = output_dir / f"{name.lower().replace(' ', '_')}_impl.py"
    target.write_text(code, encoding="utf-8")
    
    # Syntax check using py_compile
    res = subprocess.run(
        [sys.executable, "-m", "py_compile", str(target)],
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        print(f"[ERROR] Syntax error in {target.name}:")
        print(res.stderr[:500])
        return None
    
    print(f"[OK] Code written and validated: {target.name}")
    return target

def execute_code(path: Path, timeout: int = 5) -> tuple:
    """Executes Python file and returns (stdout, stderr, returncode)."""
    try:
        res = subprocess.run(
            [sys.executable, str(path)],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return res.stdout, res.stderr, res.returncode
    except subprocess.TimeoutExpired:
        return "", "Execution timed out", -1
    except Exception as e:
        return "", f"Execution error: {str(e)}", -1

# --- PATTERN 3 & 4: Multi-agent collaboration with reflection ---
def generate_code_from_sequences(seq_dir: Path, output_dir: Path) -> None:
    """Main orchestrator that demonstrates all 4 agentic patterns."""
    
    print(f"\n{'='*60}")
    print("Starting Code Generation Agent")
    print(f"Sequence diagrams: {seq_dir}")
    print(f"Output directory: {output_dir}")
    print('='*60)
    
    diagrams = load_sequence_diagrams(seq_dir)
    if not diagrams:
        print(f"[WARN] No sequence diagrams found in {seq_dir}")
        return
    
    print(f"[INFO] Found {len(diagrams)} sequence diagrams to process\n")

    for use_case, puml in diagrams.items():
        print(f"\n{'='*60}")
        print(f"Processing: {use_case}")
        print('='*60)

        # PATTERN 1: Use tools and include results in prompt
        sample_date = "2024-06-01"
        try:
            next_service = calculate_service_due_date(sample_date, months=6)
            days_since = days_since_last_service(sample_date)
            tool_context = (
                f"Tool results: next_service_due={next_service}, "
                f"days_since_last_service('{sample_date}')={days_since}"
            )
            print(f"[TOOL] {tool_context}")
        except Exception as e:
            tool_context = f"Tool error: {str(e)}"
            print(f"[TOOL] {tool_context}")

        # PATTERN 3: Multi-agent collaboration
        # Agent 1: Architect - designs class structure
        print("\n[ARCHITECT] Designing class structure...")
        architect_sys = (
            "You are a software architect. Given a sequence diagram, produce a Python class outline "
            "(class names, method signatures, attributes). Output only the outline, no implementation."
        )
        architect_prompt = (
            f"{tool_context}\n\n"
            f"Sequence Diagram:\n{puml}\n\n"
            f"Provide Python class outline with class names, attributes, and method signatures."
        )
        
        try:
            outline = ask_agent(f"architect_{use_case}", architect_sys, architect_prompt)
            print(f"[ARCHITECT] Generated outline ({len(outline)} chars)")
            print(f"[ARCHITECT] Preview: {outline[:200]}...")
        except Exception as e:
            print(f"[ERROR] Architect agent failed: {str(e)}")
            continue

        # Agent 2: Coder - implements the outline
        print("\n[CODER] Generating implementation...")
        coder_sys = (
            "You are a coding agent. Generate a complete, executable Python file implementing the provided outline. \n"
            "Requirements:\n"
            "- Use in-memory storage (dict) or JSON file\n"
            "- Include if __name__ == '__main__' with a simple demo\n"
            "- Use only Python stdlib\n"
            "- Output ONLY Python code, no markdown or explanations"
        )
        coder_prompt = (
            f"Outline:\n{outline}\n\n"
            f"Sequence Diagram:\n{puml}\n\n"
            f"Generate complete Python implementation."
        )
        
        try:
            code = ask_agent(f"coder_{use_case}", coder_sys, coder_prompt)
            
            # Clean code (remove markdown fences if present)
            code = re.sub(r"```python\n?", "", code)
            code = re.sub(r"```\n?", "", code)
            
            print(f"[CODER] Generated code ({len(code)} chars)")
        except Exception as e:
            print(f"[ERROR] Coder agent failed: {str(e)}")
            continue
        
        # PATTERN 2: Execute generated code
        print("\n[EXECUTOR] Writing and validating code...")
        impl_path = write_code(output_dir, use_case, code)
        if not impl_path:
            print(f"[SKIP] {use_case} - code failed syntax check\n")
            continue

        print("[EXECUTOR] Executing generated code...")
        stdout, stderr, returncode = execute_code(impl_path)
        print(f"[EXECUTE] returncode={returncode}")
        if stdout:
            print(f"[STDOUT] {stdout[:500]}")
        if stderr:
            print(f"[STDERR] {stderr[:500]}")

        # PATTERN 4: Observer/Reflection - review and refine
        print("\n[REVIEWER] Analyzing code quality...")
        reviewer_sys = (
            "You are a code reviewer. Analyze the generated code and execution results. "
            "Provide specific, actionable feedback if there are errors or improvements needed. "
            "If code is good, say 'APPROVED'."
        )
        reviewer_prompt = (
            f"Use Case: {use_case}\n"
            f"Code:\n{code[:1000]}\n...\n"
            f"Execution stdout: {stdout[:300]}\n"
            f"Execution stderr: {stderr[:300]}\n"
            f"Return code: {returncode}\n\n"
            "Provide review feedback."
        )
        
        try:
            feedback = ask_agent(f"reviewer_{use_case}", reviewer_sys, reviewer_prompt)
            print(f"[REVIEWER] {feedback[:400]}")
        except Exception as e:
            print(f"[ERROR] Reviewer agent failed: {str(e)}")
            feedback = ""

        # Reflection: if not approved, refine once
        if feedback and "APPROVED" not in feedback.upper():
            print("\n[REFINE] Requesting code refinement...")
            refine_prompt = (
                f"{coder_prompt}\n\n"
                f"Reviewer feedback:\n{feedback}\n\n"
                f"Generate improved code addressing the feedback."
            )
            
            try:
                refined_code = ask_agent(f"coder_refined_{use_case}", coder_sys, refine_prompt)
                refined_code = re.sub(r"```python\n?", "", refined_code)
                refined_code = re.sub(r"```\n?", "", refined_code)
                
                refined_path = write_code(output_dir, use_case + "_v2", refined_code)
                if refined_path:
                    stdout2, stderr2, rc2 = execute_code(refined_path)
                    print(f"[REFINED EXECUTE] returncode={rc2}")
                    if stdout2:
                        print(f"[REFINED STDOUT] {stdout2[:300]}")
            except Exception as e:
                print(f"[ERROR] Refinement failed: {str(e)}")

        # Agent 3: Tester - generates test cases
        print("\n[TESTER] Generating test cases...")
        tester_sys = (
            "You are a testing agent. Generate a simple test script (using unittest or plain asserts) "
            "that validates the main functionality. Output only Python code."
        )
        tester_prompt = f"Implementation:\n{code[:1000]}\n\nGenerate test script."
        
        try:
            tests = ask_agent(f"tester_{use_case}", tester_sys, tester_prompt)
            tests = re.sub(r"```python\n?", "", tests)
            tests = re.sub(r"```\n?", "", tests)
            
            test_path = output_dir / f"test_{impl_path.name}"
            test_path.write_text(tests, encoding="utf-8")
            print(f"[TESTER] Test script written: {test_path.name}")
        except Exception as e:
            print(f"[ERROR] Tester agent failed: {str(e)}")

    print(f"\n{'='*60}")
    print("Code generation complete!")
    print(f"Output directory: {output_dir}")
    print(f"Generated {len(diagrams)} implementations")
    print('='*60)

