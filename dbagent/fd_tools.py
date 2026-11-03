"""FD utilities for the 3NF extra-credit project.

These helpers implement attribute closure and sequential redundant-FD removal.
They DO NOT implement 3NF violation detection, left-side minimization, candidate
keys, or 3NF synthesis; those remain student extension tasks.
"""


def _normalize_fds(functional_dependencies):
    """Validate FDs and convert each side to a set of attribute names."""
    normalized = []
    for fd in functional_dependencies:
        lhs, rhs = set(fd["lhs"]), set(fd["rhs"])
        if not rhs:
            raise ValueError("An FD must have a nonempty right-hand side")
        normalized.append((lhs, rhs))
    return normalized


def attribute_closure(lhs, functional_dependencies):
    """Compute lhs+ by repeatedly applying FDs until no attribute can be added.

    Example: with A->B and B->C, closure({A}) = {A, B, C}.
    The argument functional_dependencies can be the JSON-style list of dicts.
    """
    closure = set(lhs)
    fds = _normalize_fds(functional_dependencies)
    changed = True
    while changed:
        changed = False
        for determinant, dependent in fds:
            if determinant <= closure and not dependent <= closure:
                closure.update(dependent)
                changed = True
    return closure


def split_rhs(functional_dependencies):
    """Return one FD per right-hand-side attribute, with stable ordering."""
    result = []
    for fd in functional_dependencies:
        for attribute in sorted(set(fd["rhs"])):
            result.append({"lhs": sorted(set(fd["lhs"])), "rhs": [attribute]})
    return result


def remove_redundant_fds(functional_dependencies):
    """Remove redundant rules sequentially, using the CURRENT remaining FDs.

    For each rule X->A, temporarily exclude that rule and compute X+ using
    all the other CURRENT rules. If A is still in X+, delete the rule
    permanently. The deleted rule MUST NOT participate in later checks.

    This routine assumes singleton RHS FDs; it splits them automatically.
    Returns (remaining_fds, audit_log). Students may use this helper, but
    still need to implement the remaining 3NF synthesis steps themselves.
    """
    remaining = split_rhs(functional_dependencies)
    audit = []
    index = 0
    while index < len(remaining):
        candidate = remaining[index]
        without_candidate = remaining[:index] + remaining[index + 1:]
        closure = attribute_closure(candidate["lhs"], without_candidate)
        redundant = candidate["rhs"][0] in closure
        audit.append({
            "tested_fd": candidate,
            "closure_without_tested_fd": sorted(closure),
            "redundant": redundant,
            "action": "removed permanently" if redundant else "kept",
        })
        if redundant:
            remaining.pop(index)
            # Do not increment index: the next rule now occupies this slot.
        else:
            index += 1
    return remaining, audit
