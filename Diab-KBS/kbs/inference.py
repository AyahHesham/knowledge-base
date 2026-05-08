"""
Inference Engine — Forward & Backward Chaining with Explanation Facility
========================================================================
Lecture mapping
---------------
* L1: Knowledge Base + Inference Engine = Knowledge-Based System
* L4: Production rules, Forward & Backward chaining, Why/How explanation
* L4: Uncertainty handled via Certainty Factors (kbs.certainty)

Key features
------------
1. Forward chaining (data-driven) — starts from patient facts, fires every
   rule whose premise becomes true, derives new facts, iterates to fixed point.
2. Backward chaining (goal-driven) — given a hypothesis, recursively tries
   to prove it by finding rules whose conclusion matches the goal and proving
   their premises.
3. Explanation facility — for every fired rule the engine records WHY it
   fired (which premise facts), allowing "Why?" and "How?" answers.
"""
from __future__ import annotations
import json, re, operator, copy
from dataclasses import dataclass, field
from typing import Any
from .certainty import combine, cf_and, cf_or, cf_rule

OPS = {
    "==": operator.eq, "!=": operator.ne,
    ">=": operator.ge, "<=": operator.le,
    ">":  operator.gt, "<":  operator.lt,
}

# ---------------------------------------------------------------------------
# Working memory — fact = (slot, value, cf)
# ---------------------------------------------------------------------------
@dataclass
class Fact:
    slot: str
    value: Any
    cf: float = 1.0
    source: str = "input"           # rule id or 'input'

    def __repr__(self):
        return f"<{self.slot}={self.value!r} cf={self.cf:+.2f} src={self.source}>"


@dataclass
class FiredRule:
    rule_id: str
    premises_used: list[str]
    derived: Fact
    rule_cf: float
    explanation: str


# ---------------------------------------------------------------------------
# Premise evaluation
# ---------------------------------------------------------------------------
_TOKEN = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(==|!=|>=|<=|>|<)\s*(.+?)\s*$")

def _eval_atom(atom: str, wm: dict[str, Fact]) -> tuple[bool, float]:
    """Evaluate a single boolean atom like 'BMI >= 30' against working memory.
    Returns (truth, cf)."""
    # Support disjunctive atoms: "BMI_cat == 'obese_I' OR BMI_cat == 'obese_II'"
    if " OR " in atom:
        parts = [p.strip() for p in atom.split(" OR ")]
        results = [_eval_atom(p, wm) for p in parts]
        truths = [r[0] for r in results]
        cfs    = [r[1] for r in results if r[0]]
        return (any(truths), max(cfs) if cfs else 0.0)

    m = _TOKEN.match(atom)
    if not m:
        return (False, 0.0)
    slot, op, rhs = m.group(1), m.group(2), m.group(3).strip()

    # parse rhs literal
    if rhs.startswith("'") and rhs.endswith("'"):
        rhs_val = rhs[1:-1]
    else:
        try:    rhs_val = float(rhs)
        except: rhs_val = rhs

    # Look up the slot in working memory.
    # Multi-valued slots store entries as 'slot::value', so search them too.
    candidates = []
    if slot in wm:
        candidates.append(wm[slot])
    for k, v in wm.items():
        if k.startswith(slot + "::"):
            candidates.append(v)
    if not candidates:
        return (False, 0.0)

    best = (False, 0.0)
    for fact in candidates:
        lhs = fact.value
        if isinstance(rhs_val, float):
            try:    lhs = float(lhs)
            except: continue
        try:
            ok = OPS[op](lhs, rhs_val)
        except Exception:
            continue
        if ok and fact.cf > best[1]:
            best = (True, fact.cf)
    return best


def _eval_premise(premise: dict, wm: dict[str, Fact]):
    """Evaluate a premise block of form {'all':[...]} or {'any':[...]}.
    Returns (satisfied: bool, premise_cf, premises_used: list[str])."""
    if "all" in premise:
        cfs, used = [], []
        for atom in premise["all"]:
            ok, cf = _eval_atom(atom, wm)
            if not ok:
                return False, 0.0, []
            cfs.append(cf); used.append(atom)
        return True, cf_and(cfs), used
    if "any" in premise:
        cfs, used = [], []
        for atom in premise["any"]:
            ok, cf = _eval_atom(atom, wm)
            if ok:
                cfs.append(cf); used.append(atom)
        if cfs:
            return True, cf_or(cfs), used
        return False, 0.0, []
    return False, 0.0, []


# ---------------------------------------------------------------------------
# The engine
# ---------------------------------------------------------------------------
class InferenceEngine:
    def __init__(self, rules_path: str):
        with open(rules_path, encoding="utf-8") as f:
            self.kb = json.load(f)
        self.rules = self.kb["rules"]
        self.reset()

    # ---------------------------------------------------------------- state
    def reset(self):
        self.wm: dict[str, Fact] = {}
        self.fired: list[FiredRule] = []
        self.trace: list[str] = []

    # Slots that may hold multiple distinct values simultaneously
    MULTI_SLOTS = {"diagnosis", "risk_factor", "complication_risk",
                   "recommended_treatment", "alert"}

    def assert_fact(self, slot: str, value: Any, cf: float = 1.0, source="input"):
        if value is None or (isinstance(value, float) and value != value):  # NaN
            return
        if slot in self.MULTI_SLOTS:
            key = f"{slot}::{value}"
            existing = self.wm.get(key)
            if existing:
                self.wm[key] = Fact(slot, value, combine(existing.cf, cf), source)
            else:
                self.wm[key] = Fact(slot, value, cf, source)
            return
        # Single-valued slot: combine when same value, replace otherwise
        existing = self.wm.get(slot)
        if existing and existing.value == value:
            new_cf = combine(existing.cf, cf)
            self.wm[slot] = Fact(slot, value, new_cf, source)
        else:
            self.wm[slot] = Fact(slot, value, cf, source)

    def load_patient(self, patient_dict: dict):
        """Load a patient record (dict of slot -> value) into working memory."""
        self.reset()
        for slot, value in patient_dict.items():
            self.assert_fact(slot, value)

    # --------------------------------------------------------- forward chain
    def forward_chain(self, max_iters: int = 10) -> list[FiredRule]:
        """Data-driven inference: iterate until no new facts derived."""
        for it in range(max_iters):
            new_fact = False
            for rule in self.rules:
                ok, premise_cf, used = _eval_premise(rule["if"], self.wm)
                if not ok:
                    continue
                if any(fr.rule_id == rule["id"] for fr in self.fired):
                    continue
                derived_cf = cf_rule(premise_cf, rule["then"]["cf"])
                self.assert_fact(rule["then"]["fact"], rule["then"]["value"],
                                 derived_cf, rule["id"])
                fact = Fact(rule["then"]["fact"], rule["then"]["value"],
                            derived_cf, rule["id"])
                self.fired.append(FiredRule(rule["id"], used, fact,
                                            rule["then"]["cf"],
                                            rule["explanation"]))
                self.trace.append(f"[FC iter {it}] {rule['id']} fired -> "
                                  f"{fact.slot}={fact.value} (cf={fact.cf:+.2f})")
                new_fact = True
            if not new_fact:
                break
        return self.fired

    # --------------------------------------------------------- backward chain
    def backward_chain(self, goal_slot: str, goal_value, depth=0,
                       visited=None) -> tuple[bool, float, list[str]]:
        """Goal-driven proof: try to prove (goal_slot == goal_value)."""
        visited = visited or set()
        indent = "  " * depth
        self.trace.append(f"{indent}[BC] try to prove {goal_slot} == {goal_value!r}")

        # 1. already in working memory?
        if goal_slot in self.wm and self.wm[goal_slot].value == goal_value:
            f = self.wm[goal_slot]
            self.trace.append(f"{indent}  ✓ found in WM (cf={f.cf:+.2f})")
            return True, f.cf, [f.source]

        # 2. find rules that conclude this goal
        for rule in self.rules:
            if rule["then"]["fact"] != goal_slot or rule["then"]["value"] != goal_value:
                continue
            if rule["id"] in visited:
                continue
            visited.add(rule["id"])

            # try to prove every atom in the premise
            atoms = rule["if"].get("all", []) + rule["if"].get("any", [])
            results, sub_chain = [], []
            for atom in atoms:
                ok, cf = _eval_atom(atom, self.wm)
                if ok:
                    results.append((True, cf, atom))
                    continue
                # try to derive missing atom by recursion
                m = _TOKEN.match(atom)
                if m:
                    slot = m.group(1)
                    rhs = m.group(3).strip().strip("'\"")
                    proved, p_cf, sub = self.backward_chain(slot, rhs, depth+1, visited)
                    results.append((proved, p_cf, atom))
                    sub_chain.extend(sub)
                else:
                    results.append((False, 0.0, atom))
            if "all" in rule["if"]:
                if all(r[0] for r in results):
                    cf = cf_rule(cf_and([r[1] for r in results]), rule["then"]["cf"])
                    self.trace.append(f"{indent}  ✓ proved via {rule['id']} (cf={cf:+.2f})")
                    self.fired.append(FiredRule(rule["id"], [r[2] for r in results],
                                                Fact(goal_slot, goal_value, cf,
                                                     rule["id"]),
                                                rule["then"]["cf"],
                                                rule["explanation"]))
                    return True, cf, [rule["id"]] + sub_chain
            elif "any" in rule["if"]:
                ok_results = [r for r in results if r[0]]
                if ok_results:
                    cf = cf_rule(cf_or([r[1] for r in ok_results]), rule["then"]["cf"])
                    self.fired.append(FiredRule(rule["id"], [r[2] for r in ok_results],
                                                Fact(goal_slot, goal_value, cf,
                                                     rule["id"]),
                                                rule["then"]["cf"],
                                                rule["explanation"]))
                    return True, cf, [rule["id"]] + sub_chain
        self.trace.append(f"{indent}  ✗ cannot prove {goal_slot} == {goal_value!r}")
        return False, 0.0, []

    # ------------------------------------------------------------ explanation
    def why(self, rule_id: str) -> str:
        for fr in self.fired:
            if fr.rule_id == rule_id:
                bits = ", ".join(fr.premises_used)
                return (f"Rule {fr.rule_id} fired because: {bits}.\n"
                        f"Reasoning: {fr.explanation}\n"
                        f"Conclusion: {fr.derived.slot} = {fr.derived.value} "
                        f"(certainty {fr.derived.cf:+.2f}).")
        return f"Rule {rule_id} did not fire in this session."

    def how(self, slot: str, value=None) -> str:
        for fr in self.fired:
            if fr.derived.slot == slot and (value is None or fr.derived.value == value):
                return (f"How was '{fr.derived.value}' concluded?\n"
                        f"   • Rule {fr.rule_id}: {fr.explanation}\n"
                        f"   • Premises matched: {fr.premises_used}\n"
                        f"   • Certainty: {fr.derived.cf:+.2f}")
        return f"No rule has concluded '{slot}'."

    # --------------------------------------------------------------- summary
    def diagnoses(self):
        return [fr for fr in self.fired if fr.derived.slot == "diagnosis"]

    def treatments(self):
        return [fr for fr in self.fired if fr.derived.slot == "recommended_treatment"]

    def risk_factors(self):
        return [fr for fr in self.fired if fr.derived.slot == "risk_factor"]

    def complications(self):
        return [fr for fr in self.fired if fr.derived.slot == "complication_risk"]

    def alerts(self):
        return [fr for fr in self.fired if fr.derived.slot == "alert"]


# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    eng = InferenceEngine("/home/user/workspace/Diab-KBS/knowledge_base/rules.json")
    test_patient = {
        "Age": 55, "Gender": "male", "BMI": 33.2, "BMI_cat": "obese_I",
        "HbA1c": 8.3, "HbA1c_cat": "diabetes_range",
        "FPG": 168, "FPG_cat": "diabetes_range",
        "PP2H": 248, "PP_cat": "diabetes_range",
        "RBS": 220, "HTN": 1, "Paresthesia": 1, "BlurredVision": 1,
        "Creatinine": 1.6, "TSH": 2.1, "TSH_cat": "normal",
        "Fatigue": 0, "WeightLoss": 0, "PolyuriaPolydipsia": 1,
    }
    eng.load_patient(test_patient)
    eng.forward_chain()
    print("\n=== DIAGNOSES ===")
    for d in eng.diagnoses(): print(" ", d.derived, "←", d.rule_id)
    print("\n=== RISK FACTORS ===")
    for d in eng.risk_factors(): print(" ", d.derived, "←", d.rule_id)
    print("\n=== COMPLICATIONS ===")
    for d in eng.complications(): print(" ", d.derived, "←", d.rule_id)
    print("\n=== TREATMENTS ===")
    for d in eng.treatments(): print(" ", d.derived, "←", d.rule_id)
    print("\n=== ALERTS ===")
    for d in eng.alerts(): print(" ", d.derived, "←", d.rule_id)
    print("\n=== WHY R01? ===\n", eng.why("R01"))
    print("\n=== HOW diagnosis? ===\n", eng.how("diagnosis"))
