from __future__ import annotations


SEVERITY_ORDER = {"info": 1, "minor": 2, "major": 3, "critical": 4}


def confidence_for(evidence_count: int, has_direct_evidence: bool = True) -> float:
    if evidence_count <= 0:
        return 0.45
    base = 0.65 + min(evidence_count, 3) * 0.08
    if has_direct_evidence:
        base += 0.08
    return min(base, 0.95)


def severity_rank(severity: str) -> int:
    return SEVERITY_ORDER.get(severity, 0)

