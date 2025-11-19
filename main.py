from pathlib import Path
from agents.uc_diagram_agent import generate_use_case_diagram
from agents.uc_specs_agent import generate_use_case_specs
from agents.seq_diagram_agent import generate_seq_diagram

BASE_DIR = Path(__file__).parent
SUMMARY_PATH = BASE_DIR / "summary" / "system_summary.txt"

GENERATED_DIR = BASE_DIR / "generated"
DIAGRAMS_DIR = GENERATED_DIR / "diagrams"
SPECS_DIR = GENERATED_DIR / "specs"
SEQ_DIR = DIAGRAMS_DIR / "sequence"

DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)
SPECS_DIR.mkdir(parents=True, exist_ok=True)
SEQ_DIR.mkdir(parents=True, exist_ok=True)


def main():

    output_file = DIAGRAMS_DIR / "use_case_diagram.puml"  # .puml is the PlantUML extension
    uc_specs_file = SPECS_DIR / "use_case_specs.md"

    generate_use_case_diagram(SUMMARY_PATH, output_file)

    generate_use_case_specs(output_file, uc_specs_file)

    generate_seq_diagram(uc_specs_file, SEQ_DIR)

if __name__ == "__main__":
    main()
