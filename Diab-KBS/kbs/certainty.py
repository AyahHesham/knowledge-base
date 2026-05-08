"""
Certainty Factor algebra (MYCIN-style)
======================================
Lecture mapping: L4 — Uncertainty / Certainty Factors

CF ∈ [-1, +1]   -1 = absolute disbelief, 0 = unknown, +1 = absolute belief
"""
from __future__ import annotations


def combine(cf1: float, cf2: float) -> float:
    """Combine two CFs that support the same hypothesis (MYCIN combination)."""
    if cf1 is None: return cf2
    if cf2 is None: return cf1
    if cf1 >= 0 and cf2 >= 0:
        return cf1 + cf2 * (1 - cf1)
    if cf1 <= 0 and cf2 <= 0:
        return cf1 + cf2 * (1 + cf1)
    return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))


def cf_and(cfs: list[float]) -> float:
    """CF for a conjunction of premises = min."""
    return min(cfs) if cfs else 1.0


def cf_or(cfs: list[float]) -> float:
    """CF for a disjunction of premises = max."""
    return max(cfs) if cfs else 0.0


def cf_rule(premise_cf: float, rule_cf: float) -> float:
    """CF transmitted by the rule when premise is partially true."""
    return max(0.0, premise_cf) * rule_cf
