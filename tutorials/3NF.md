# 3NF Extension — Two Separate Tasks

This is a programming guide, not a lesson on normalization. Use the concepts taught in class.

## Task 1: Check for 3NF violations (+1 extra credit point)

Edit `dbagent/normalization.py` and implement:

```python
def find_3nf_violations(attributes, functional_dependencies):
    # Return the 3NF violations found in the input relation.
    raise NotImplementedError
```

**Input:** a relation's attributes and functional dependencies (FDs). **Output:** the detected violations, or an empty result if the relation satisfies 3NF. Include tests for a relation that satisfies 3NF and one that violates 3NF. This task does not require decomposition.

Test locally (no API needed):

```bash
python3 -m dbagent.three_nf_cli --input examples/normalization_case.json --task violations
```

## Task 2: Decompose into 3NF (+2 extra credit points total)

Edit the **separate** function in the same file:

```python
def decompose_to_3nf(attributes, functional_dependencies):
    # Return a correct 3NF decomposition when needed.
    raise NotImplementedError
```

**Input:** the same relation and FDs. **Output:** a 3NF decomposition if the input violates 3NF; otherwise, preserve the already-normalized relation. Implement the decomposition using the method taught in class. Demonstrate correct output, dependency preservation, and lossless join with tests. You may reuse helpers from `dbagent/fd_tools.py`.

The FD helper removes redundant rules **sequentially**: temporarily exclude the current FD, compute the left-hand side closure using the remaining FDs, and permanently remove the FD if its right-hand side remains in that closure. Previously removed rules are not reused.

Test locally (no API needed):

```bash
python3 -m dbagent.three_nf_cli --input examples/normalization_case.json --task decompose
python3 -m unittest discover -s tests -v
```

The functions initially raise `NotImplementedError` until you implement them. Add tests in `tests/test_normalization_student.py`. The +1 and +2 options are **alternatives, not cumulative**: the maximum additional credit is 2 points.

## Files to use

- `dbagent/normalization.py`: implement the two tasks independently.
- `dbagent/fd_tools.py`: optional reusable FD helpers.
- `dbagent/three_nf_cli.py`: runs either task offline.
- `examples/normalization_case.json`: editable input example.
- `examples/redundant_fd_case.json`: another test case.
- `examples/key_relation_case.json`: additional test case.
- `tests/test_normalization_student.py`: add meaningful assertions.

You do not need GitHub Copilot, OpenAI, or any API key to implement or test either task.
