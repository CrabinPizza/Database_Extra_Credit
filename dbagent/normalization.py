"""Two independent optional Python extensions for 3NF.

Task 1 checks whether a relation violates 3NF.
Task 2 produces a 3NF decomposition when needed.
Neither function requires an API key. Implementations are intentionally omitted.
"""

# Return the 3NF violations found in the input relation.
def find_3nf_violations(attributes, functional_dependencies):
    """Task 1 (+1 point): return detected 3NF violations, or [] if none.

    attributes: list of attribute names, e.g. ["A", "B", "C"].
    functional_dependencies: list of {"lhs": [...], "rhs": [...]} dictionaries.
    Add tests for both a passing and a failing relation.
    """
    raise NotImplementedError("Implement Task 1: check for 3NF violations")


def decompose_to_3nf(attributes, functional_dependencies):
    """Task 2 (+2 points total): return a correct 3NF decomposition.

    Decompose if the relation violates 3NF; otherwise preserve the relation.
    Verify the resulting relations with test cases. You may use fd_tools.py.
    """
    raise NotImplementedError("Implement Task 2: decompose into 3NF")