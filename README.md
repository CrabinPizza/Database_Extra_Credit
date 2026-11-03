# Database Design AI Agent — COMP.3090

Python package for exploring E-R models, relational schemas, and Oracle DDL. Includes offline demo, optional GitHub Copilot live mode, and two separate Python 3NF extension tasks.

## Getting started

Read `tutorials/RUN_GUIDE.md` for installation, commands, and troubleshooting. `tutorials/VIEW_JSON_AND_MMD.md` explains how to view output files.

### Option 1: Offline demo (no API)

```bash
python3 -m dbagent --demo --out output_demo
```

### Option 2: GitHub Copilot live mode (Copilot account and SDK required)

```bash
python3 -m dbagent --provider copilot --interactive --out output_live
python3 -m dbagent --provider copilot --requirements examples/hospital.txt --out output_hospital
```

GitHub Copilot SDK availability and usage quotas depend on the account. Live authentication has not been independently verified in this environment. Demo mode and both 3NF tasks need no API.

## 3NF programming — two separate tasks

**Task 1: Check for 3NF violations (+1 point)** — implement `find_3nf_violations()` in `dbagent/normalization.py`.

**Task 2: Decompose into 3NF (+2 points total)** — implement `decompose_to_3nf()` in the same file. Decompose when there is a violation; otherwise preserve the relation.

The +1 and +2 awards are alternatives, not cumulative. See `tutorials/3NF.md`. No detailed normalization theory is included; follow the classroom instruction.

```bash
python3 -m dbagent.three_nf_cli --input examples/normalization_case.json --task violations
python3 -m dbagent.three_nf_cli --input examples/normalization_case.json --task decompose
python3 -m unittest discover -s tests -v
```

Before students implement the functions, the two 3NF commands intentionally raise `NotImplementedError`.

## Submission

Submit one ZIP per team through Canvas. Include complete source code, a README listing every team member's **full name**, screenshots, generated files, and 3NF tests if applicable. Never upload API keys or passwords.
