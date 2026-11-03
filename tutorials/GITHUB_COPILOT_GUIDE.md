# GitHub Copilot Setup and Usage Guide (COMP.3090)

**For the Database Design AI Agent v2 starter package**  
Updated October 2026. Official references: https://github.com/github/copilot-sdk and https://docs.github.com/en/copilot/how-tos/copilot-sdk/auth/authenticate

## 1. Know the difference: Copilot as a coding assistant vs. Copilot as an LLM backend

- **GitHub Copilot in VS Code:** helps you read, explain, write, and debug the Python source code. This is the **recommended option for the optional 3NF extension**. It does not automatically power the agent's Live Mode.
- **GitHub Copilot SDK for Python:** allows a separate Python program to call Copilot programmatically. It is optional, requires **Python 3.11 or newer**, and a Copilot-enabled GitHub account with remaining usage allowance (or a separate BYOK provider). The SDK is not integrated into the provided `dbagent` Live Mode.
- **The supplied agent:** `--demo` and `--model-file` work offline, without an API key. `--requirements` and `--interactive` currently use **OpenAI Responses API** via `dbagent/llm.py` and require `OPENAI_API_KEY`. Installing Copilot alone does **not** change that.

**Grading:** The 3-point base task works in Demo Mode without Copilot or paid API access. The 3NF extension can be coded and tested locally without any LLM.

## 2. GitHub Copilot in VS Code: easiest path for students

### Step A. Get a GitHub account

1. Open https://github.com/ and create an account (or sign in).
2. Review Copilot access at https://github.com/settings/copilot or https://github.com/features/copilot .
3. GitHub offers a limited free Copilot tier; eligible students may be able to request additional access through https://education.github.com/ . Eligibility, availability, quotas, and billing can change. **Do not purchase a plan just for this optional assignment.**

### Step B. Install VS Code

1. Download VS Code from https://code.visualstudio.com/ .
2. Install and open VS Code.
3. Open **Extensions**, search for **GitHub Copilot Chat**, and install the official GitHub extension (and GitHub Copilot Chat if it is offered separately).
4. Follow the **Sign in with GitHub** prompt and authorize the connection.
5. Check that Copilot Chat is available. If not, confirm your GitHub account has Copilot access and reload VS Code.
6. If you've had Copilot but closed it use **CTRL + ALT + I**

### Step C. Open the course package

1. Extract `database_design_agent_v2_input_3nf.zip` (or this updated ZIP).
2. In VS Code, choose **File > Open Folder** and select `database_design_agent`.
3. Open a terminal in VS Code (**Terminal > New Terminal**).
4. Verify Python: `python3 --version` (macOS/Linux) or `py --version` (Windows).
5. Run the original agent: `python3 -m dbagent --demo --out output_demo` (Windows: `py -m dbagent --demo --out output_demo`).
6. Open `dbagent/normalization.py` and `tutorials/3NF.md` to start Part 2.

### Step D. Use Copilot to understand and extend 3NF code

In Copilot Chat, try prompts such as:

> Explain the interfaces and expected input/output of `dbagent/normalization.py` without changing any files.

> Explain how attribute closure can be used to find candidate keys for a relation with functional dependencies. Include a worked example.

> Suggest edge-case unit tests for 3NF violations and 3NF synthesis. Do not assume that an LLM-generated decomposition is correct.

> Review my `decompose_to_3nf` implementation for lossless join and dependency preservation. Explain any counterexample.

**Important:** Copilot may produce incorrect normalization algorithms. Students must understand the FDs, candidate keys, 3NF condition, and decomposition properties and validate their code with tests.

## 3. Optional: run the GitHub Copilot SDK from Python

**This section is optional and NOT required for any of the five extra-credit points.** It demonstrates programmatic use of GitHub Copilot separately from the course agent.

### Requirements

- Python **3.11+**. Your macOS system Python 3.9.6 may run the original agent but is **not sufficient for the current Copilot SDK**.
- GitHub Copilot access with available quota. Free-tier access is limited; requests may count against the account's allowance.
- Internet access and GitHub authentication.

### Create a separate Python environment

macOS/Linux:

```bash
python3.11 -m venv .venv-copilot
source .venv-copilot/bin/activate
python -m pip install --upgrade pip
python -m pip install github-copilot-sdk
python -m copilot download-runtime
```

Windows PowerShell (assuming Python 3.11+ is installed):

```powershell
py -3.11 -m venv .venv-copilot
.venv-copilot\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install github-copilot-sdk
python -m copilot download-runtime
```

If there is an error message in the venv for being unable to install pydantic-core, you may need to install rust from https://rust-lang.org/tools/install/

and

Update your pip, wheel, and setuptools
```powershell
python -m pip install --upgrade pip setuptools wheel
```

or 

Verify if you used py on a Mac machine or python on a Windows machine. If either is the case, swap the commands and verify that you have python 3.11 installed.

If the runtime command fails, see the official Python SDK README: https://github.com/github/copilot-sdk/tree/main/python .

### Authenticate

Sign into GitHub Copilot through the Copilot CLI's GitHub sign-in flow if prompted, or use an existing signed-in CLI session. The SDK can reuse stored OAuth credentials. Consult https://docs.github.com/en/copilot/how-tos/copilot-sdk/auth/authenticate for supported methods. **Do not put tokens in source code or ZIP submissions.**

### Run a standalone example

From the extracted `database_design_agent` directory, with the Copilot environment active:

```bash
python examples/copilot_sdk_example.py
```

This example asks Copilot to describe 3NF and prints its response. It **does not** generate E-R diagrams or Oracle DDL, and does **not** replace the OpenAI backend in `dbagent/llm.py`.

If your account is not authorized, a model is unavailable, or quota is exhausted, the example may fail. **Demo Mode remains available without Copilot.**

## 4. How students add their 3NF implementation

1. Keep the original package structure.
2. Open `dbagent/normalization.py` and implement the provided student functions, including `find_3nf_violations` and `decompose_to_3nf`.
3. Use `examples/normalization_case.json` as an initial test case. Include FDs, expected candidate keys, and expected 3NF output.
4. Add tests to `tests/test_normalization_student.py` or a new test module; do not rely only on screenshots.
5. Run `python -m unittest discover -s tests -v` and your own examples.
6. In `README.md`, list every team member's **full name**, modified files, how to run tests, and the 3NF results.
7. Submit one ZIP per team via Canvas. Do not include `.venv-copilot`, tokens, `.env`, or credentials.

**1 extra point:** identify and demonstrate 3NF violations from supplied FDs.  
**2 extra points (instead of 1):** implement and test 3NF synthesis/decomposition with the intended lossless-join and dependency-preserving properties.

## 5. Troubleshooting

| Problem | What to do |
| --- | --- |
| `python` shows 3.9.6 | Original Demo Mode may still work; install Python 3.11+ separately for Copilot SDK. |
| `No module named copilot` | Activate the Copilot virtual environment and install `github-copilot-sdk`. |
| Authentication/entitlement error | Check GitHub sign-in and Copilot access; do not assume GitHub account alone grants SDK usage. |
| Quota/usage error | Wait for allowance renewal or use Demo Mode; do not purchase credits for this assignment. |
| Agent Live Mode says `OPENAI_API_KEY is not set` | Expected: the original agent still uses OpenAI for live inputs. Use `--demo` without a key. |
| Copilot suggests a 3NF result | Independently verify candidate keys, FDs, dependency preservation and lossless join. |

## Official resources

- GitHub Copilot SDK: https://github.com/github/copilot-sdk
- Python SDK: https://github.com/github/copilot-sdk/tree/main/python
- Authentication: https://docs.github.com/en/copilot/how-tos/copilot-sdk/auth/authenticate
- Python runtime setup: https://docs.github.com/en/copilot/how-tos/copilot-sdk/setup/bundled-cli
- GitHub Education: https://education.github.com/
