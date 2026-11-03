"""Command-line entry point: select input mode and write five design artifacts."""

import argparse
import json
from pathlib import Path
from .llm import extract_requirements
from .model import load_model
from .mapping import map_relations
from .render import mermaid, oracle_ddl, review_report

def main(argv=None):
    """Parse arguments, build a candidate design, and save output files."""
    parser = argparse.ArgumentParser(description='Educational Database Design AI Agent')
    # Exactly one input source is allowed: demo, existing JSON, or live LLM.
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument('--demo', action='store_true', help='Use included sample model; no API key needed')
    src.add_argument('--model-file', help='Read pre-generated model JSON; no API key needed')
    src.add_argument('--requirements', help='Text file of requirements for live LLM mode')
    src.add_argument('--interactive', action='store_true', help='Type requirements interactively for live LLM mode')
    parser.add_argument('--provider', choices=['openai', 'copilot'], default='openai', help='Live LLM backend (ignored for offline modes)')
    parser.add_argument('--llm-model', default=None, help='Optional model ID for selected live provider')
    parser.add_argument('--out', default='output')
    args = parser.parse_args(argv)
    # Resolve sample files relative to the installed package, not the terminal directory.
    base = Path(__file__).resolve().parent.parent
    if args.demo:
        model = load_model(base / 'examples' / 'university_model.json')
        description = (base / 'examples' / 'university.txt').read_text(encoding='utf-8')
    elif args.model_file:
        model = load_model(args.model_file)
        description = 'Design model supplied via JSON; see source model.'
    else:
        if args.interactive:
            # Collect multiple lines until the user enters END on a separate line.
            print('Describe your database requirements. Type END on a new line to finish:')
            lines = []
            while True:
                try:
                    line = input('> ')
                except EOFError:
                    break
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            description = '\n'.join(lines).strip()
            if not description:
                parser.error('No requirements entered; please enter text before END.')
        else:
            # Read natural-language requirements from a UTF-8 text file.
            description = Path(args.requirements).read_text(encoding='utf-8').strip()
            if not description:
                parser.error('Requirements file is empty.')
        if args.provider == 'copilot':
            from .copilot_provider import extract_requirements_copilot
            model = extract_requirements_copilot(description, model=args.llm_model)
        else:
            model = extract_requirements(description, model=args.llm_model or 'gpt-4.1-mini')
    # Deterministic mapping does not call the LLM; review its warnings.
    tables, warnings = map_relations(model)
    out = Path(args.out)
    # Create output folder and serialize each intermediate artifact for inspection.
    out.mkdir(parents=True, exist_ok=True)
    (out / 'design.json').write_text(json.dumps(model, indent=2) + '\n', encoding='utf-8')
    (out / 'relational_schema.json').write_text(json.dumps(tables, indent=2) + '\n', encoding='utf-8')
    (out / 'er_diagram.mmd').write_text(mermaid(model), encoding='utf-8')
    (out / 'create_tables.sql').write_text(oracle_ddl(tables), encoding='utf-8')
    (out / 'design_report.md').write_text(review_report(description, model, tables, warnings), encoding='utf-8')
    print(f'Generated 5 files in {out.resolve()}')
    print('IMPORTANT: This is a candidate design; review the report and validate in Oracle.')

if __name__ == '__main__':
    main()
