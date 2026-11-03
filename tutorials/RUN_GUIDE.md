# COMP.3090 Database Design AI Agent — Complete Run Guide

## 1. Choose your option

- **Option 1 — Offline Demo:** No account, API key, LLM, or payment. Run the supplied example and generate E-R, relational schema, and Oracle DDL. Implement and test 3NF using local Python. **All 5 extra-credit points are achievable without a live model.**
- **Option 2 — GitHub Copilot Live AI:** Enter new natural-language requirements through the terminal or a `.txt` file. Uses GitHub Copilot SDK and the Copilot entitlement/quota on your GitHub account. **No OpenAI API key is required.** UML provides students Copilot access, but you must verify your account can use the SDK and has available quota.

The original OpenAI backend remains in the code as an optional alternative; **it is not required for this assignment**. These instructions use Copilot for live AI.

## 2. Install Python

**Windows:** Download Python from https://www.python.org/downloads/ . For Option 2, install **Python 3.11 or newer**. During installation, enable *Add Python to PATH* if offered. Open PowerShell and run `py --version` and `py -m pip --version`. Use `py` instead of `python3` in the commands below. If you have multiple versions, use `py -3.11` or the installed version.

**macOS:** Download Python 3.11+ from https://www.python.org/downloads/ and install it. Open Terminal and run `python3 --version` and `python3 -m pip --version`. macOS may already have Python 3.9.6; it is sufficient for Option 1, **not** Option 2. A Python 3.11+ installation can be invoked explicitly if necessary.

**Recommendation:** Python 3.11+ for either option, to avoid switching interpreters. Option 1 itself supports Python 3.9+.

## 3. Extract and open the package

1. Download the course ZIP and extract it (do not run code from inside the ZIP).
2. Open Terminal or PowerShell.
3. Change directory (`cd`) into the extracted folder **containing `dbagent/` and `examples/`**. For example, `cd ~/Downloads/database_design_agent_two_options_3nf_guided` on macOS, or `cd "$HOME\Downloads\database_design_agent_two_options_3nf_guided"` in PowerShell.
4. Run `ls` on macOS or `dir` on Windows. You should see `dbagent`, `examples`, `tests`, and `tutorials`.

Commands below use `python3` for macOS. On Windows replace `python3` with `py` (or `py -3.11`).

## 4. Option 1: Offline Demo (no API)

```bash
python3 -m dbagent --demo --out output_demo
```

The terminal should report **Generated 5 files**. Open `output_demo/`:

- `design.json` — candidate entities, attributes, relationships and assumptions.
- `relational_schema.json` — mapped tables, columns and keys.
- `er_diagram.mmd` — Mermaid E-R diagram source.
- `create_tables.sql` — Oracle SQL DDL; inspect before executing in Oracle.
- `design_report.md` — human-readable design summary and warnings.

This mode uses a predefined model. It does **not** interpret new natural-language requirements or call AI.

## 5. View the `.mmd` E-R diagram

Open `output_demo/er_diagram.mmd` in a text editor, copy all text, open https://mermaid.live/ and paste it into the left pane. The E-R diagram appears on the right. Export PNG or SVG if needed. The `.mmd` file itself is text, not an image.

## 6. View and edit `.json` files

JSON is a **plain-text data format**, not a picture. It uses objects `{}`, arrays `[]`, and key/value pairs. Use any of these:

- **VS Code (recommended):** File > Open File > select `design.json` or `relational_schema.json`. Use *Format Document* for indentation; collapse/expand nested fields using the arrows beside line numbers.
- **macOS:** Right-click file > Open With > TextEdit, or use VS Code. In Terminal: `python3 -m json.tool output_demo/design.json` to display formatted JSON.
- **Windows:** Open in Notepad or VS Code. In PowerShell: `py -m json.tool output_demo\design.json`.
- **Browser:** Drag the `.json` file into a browser window to view its text (formatting varies by browser).

Example:

```json
{
  "attributes": ["A", "B", "C"],
  "functional_dependencies": [
    {"lhs": ["A"], "rhs": ["B"]},
    {"lhs": ["B"], "rhs": ["C"]}
  ]
}
```

For a syntax check: `python3 -m json.tool examples/normalization_case.json` (replace `python3` with `py` on Windows). To create a new normalization test, **copy** `examples/normalization_case.json`, edit its `attributes` and `functional_dependencies`, and save as a new `.json` file. Keep double quotes, commas, and square brackets correct. Never put passwords/API keys in JSON submitted to Canvas.

**Important:** `design.json` is the AI/database-design intermediate model; `examples/normalization_case.json` is the **3NF test input**. They have different structures. Do not pass `design.json` directly to the 3NF CLI unless you convert it to the normalization input format.

## 7. Option 2: Live AI with GitHub Copilot (no OpenAI key)

1. Confirm your GitHub account has Copilot access. UML access may require activating a particular GitHub identity; use the university's instructions if needed. SDK usage is subject to plan/model availability and quotas.
2. Install **Python 3.11+** (Section 2).
3. Install and sign into **GitHub Copilot CLI** following https://docs.github.com/en/copilot/how-tos/copilot-cli . This CLI is distinct from the VS Code Copilot chat extension.
4. Install the Python SDK in the same Python environment used to run the agent:

```bash
python3 -m pip install github-copilot-sdk
```

5. Run **file input** with the provided example:

```bash
python3 -m dbagent --provider copilot --requirements examples/hospital.txt --out output_hospital
```

6. Or run **interactive input**:

```bash
python3 -m dbagent --provider copilot --interactive --out output_custom
```

Type several lines describing your database, then type `END` on a line by itself:

```text
A library has books and physical copies of each book.
Members borrow individual copies. A loan has checkout and return dates.
END
```

7. Inspect the five output files as in Sections 4–6. AI-generated designs may contain incorrect keys, cardinalities or missing constraints; **review them before trusting them**. The package does not automatically execute the DDL against Oracle.

**If Copilot authentication or SDK calls fail:** Confirm CLI login, Python version, SDK installation, Copilot entitlement and available quota. The SDK interface may change; follow GitHub's current SDK documentation: https://github.com/github/copilot-sdk . Option 1 always remains available and can earn all 5 points. **The live Copilot path has not been verified with a real UML account in this environment.**

## 8. Add 3NF code and test it offline (both options)

Edit `dbagent/normalization.py` and implement:

- `find_3nf_violations(attributes, functional_dependencies)` — +1 point option.
- `decompose_to_3nf(attributes, functional_dependencies)` — full +2 point option (not cumulative).

`dbagent/fd_tools.py` already provides course-supplied FD helpers. **Use the exact algorithm sequence in `tutorials/THREE_NF_STUDENT_GUIDE.md`** (also available bilingually). In particular, when checking if `X -> A` is redundant, temporarily exclude **that** FD, calculate `X+` using the other **currently retained** FDs, and permanently remove the FD if `A` is still in `X+`. Already removed FDs must **never** participate in subsequent checks.

Run the standalone 3NF test commands:

```bash
python3 -m dbagent.three_nf_cli --input examples/normalization_case.json --task violations
python3 -m dbagent.three_nf_cli --input examples/normalization_case.json --task decompose
python3 -m unittest discover -s tests -v
```

Before implementing student functions, `NotImplementedError` is expected; it is not an installation problem. The built-in tests for unfinished student work may be skipped. Add your own tests showing the original relation, FDs, minimal basis, 3NF relations, and reasoning about lossless join and dependency preservation. Multiple valid decompositions may exist; do not hard-code one output.

**Neither the 3NF Python code nor its tests require an LLM or API.** Using Copilot to help write code is optional; students must understand and verify the result.

## 9. Canvas submission

Submit **one ZIP per team of 1–3 students**. Include full Python source, a `README.md` listing every team member's **full name**, screenshots of successful execution, generated outputs, and any modified 3NF code, tests and results. A GitHub link is optional. Do not submit credentials or environment secrets.

## 10. Troubleshooting

| Problem | Action |
|---|---|
| `No module named dbagent` | Run from the folder that contains `dbagent/`. |
| `python3: command not found` on Windows | Use `py` or `py -3.11`. |
| `No module named copilot` | Install `github-copilot-sdk` with the same Python interpreter. |
| Copilot login/quota error | Check GitHub Copilot CLI login and quota; use Option 1 if necessary. |
| `NotImplementedError` from 3NF CLI | Complete the student 3NF functions in `normalization.py`. |
| JSON parsing error | Use double quotes, correct commas/brackets; check with `python3 -m json.tool FILE.json`. |
| Mermaid does not render | Paste the full `.mmd` source into https://mermaid.live/ and inspect syntax. |
