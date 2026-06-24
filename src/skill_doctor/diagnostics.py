from __future__ import annotations

from dataclasses import asdict, dataclass
import re

from .infer_contract import SkillContract
from .parse_markdown import MarkdownDocument
from .risk_scoring import confidence_for, severity_rank


CATEGORIES = {
    "invocation_clarity",
    "input_output_contract",
    "preconditions",
    "acceptance_criteria",
    "execution_hazards",
    "instruction_conflicts",
    "security_prompt_injection",
    "tool_permission_risk",
    "context_load_discipline",
    "host_adapter_compatibility",
    "verification_gaps",
    "maintainer_handoff",
}


@dataclass(frozen=True)
class DiagnosticRecord:
    diagnostic_id: str
    category: str
    severity: str
    title: str
    evidence: str
    risk: str
    recommended_fix: str
    patchable: bool
    confidence: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def run_diagnostics(document: MarkdownDocument, contract: SkillContract) -> list[DiagnosticRecord]:
    diagnostics = [
        diagnostic
        for diagnostic in [
            _invocation_clarity(document, contract),
            _missing_non_goals(contract),
            _missing_io_contract(contract),
            _missing_acceptance_criteria(contract),
            _execution_hazards(document, contract),
            _prompt_injection(document, contract),
            _tool_permission_risk(document, contract),
            _verification_gaps(contract),
            _maintainer_handoff(contract),
        ]
        if diagnostic is not None
    ]
    return sorted(diagnostics, key=lambda item: (-severity_rank(item.severity), item.diagnostic_id))


def _invocation_clarity(document: MarkdownDocument, contract: SkillContract) -> DiagnosticRecord | None:
    description = document.frontmatter.get("description", "")
    use_text = " ".join(contract.use_when + [description]).lower()
    vague_terms = ["agent workflows", "project work", "anything", "any task", "general help", "helps agents"]
    if contract.use_when and not any(term in use_text for term in vague_terms):
        return None
    evidence = description or contract.purpose or "No explicit trigger language found."
    return DiagnosticRecord(
        diagnostic_id="SD001",
        category="invocation_clarity",
        severity="major",
        title="Trigger description is missing or too broad",
        evidence=_short(evidence),
        risk="Agents may over-apply the skill to unrelated tasks or miss its intended activation boundary.",
        recommended_fix="Add explicit 'Use when' and 'Do not use when' guidance with concrete triggering tasks.",
        patchable=True,
        confidence=confidence_for(1),
    )


def _missing_non_goals(contract: SkillContract) -> DiagnosticRecord | None:
    if contract.do_not_use_when:
        return None
    return DiagnosticRecord(
        diagnostic_id="SD002",
        category="invocation_clarity",
        severity="major",
        title="No non-use cases are defined",
        evidence="No 'Do not use when', non-goals, or out-of-scope guidance was inferred.",
        risk="The skill can be invoked for nearby but inappropriate tasks.",
        recommended_fix="Add a short 'Do not use this skill when' list covering trivial, unrelated, or unsafe cases.",
        patchable=True,
        confidence=confidence_for(1),
    )


def _missing_io_contract(contract: SkillContract) -> DiagnosticRecord | None:
    missing = []
    if not contract.inputs:
        missing.append("inputs")
    if not contract.outputs:
        missing.append("outputs")
    if not missing:
        return None
    return DiagnosticRecord(
        diagnostic_id="SD003",
        category="input_output_contract",
        severity="major",
        title="Input/output contract is incomplete",
        evidence=f"Missing inferred contract fields: {', '.join(missing)}.",
        risk="Agents may start without required context or finish without producing the expected artifacts.",
        recommended_fix="Document required inputs and durable outputs, including filenames or artifact shapes when applicable.",
        patchable=True,
        confidence=confidence_for(len(missing)),
    )


def _missing_acceptance_criteria(contract: SkillContract) -> DiagnosticRecord | None:
    if contract.acceptance_criteria:
        return None
    return DiagnosticRecord(
        diagnostic_id="SD004",
        category="acceptance_criteria",
        severity="major",
        title="Acceptance criteria are missing",
        evidence="No acceptance criteria or definition-of-done section was inferred.",
        risk="Agents may overstate completion or stop before the skill's required outcome is produced.",
        recommended_fix="Add measurable acceptance criteria that define the minimum complete outcome.",
        patchable=True,
        confidence=confidence_for(1),
    )


def _execution_hazards(document: MarkdownDocument, contract: SkillContract) -> DiagnosticRecord | None:
    hazard_terms = ["delete", "overwrite", "remove", "apply", "execute", "run", "install", "token", "credential"]
    hits = [
        line
        for line in document.imperative_lines
        if any(re.search(rf"\b{term}\b", line.text, re.IGNORECASE) for term in hazard_terms)
    ]
    if not hits or contract.safety or contract.preconditions:
        return None
    evidence = "; ".join(f"line {hit.line}: {hit.text}" for hit in hits[:3])
    return DiagnosticRecord(
        diagnostic_id="SD005",
        category="execution_hazards",
        severity="critical",
        title="Potentially hazardous instructions lack safety boundaries",
        evidence=_short(evidence),
        risk="Agents may run, install, overwrite, or delete without clear permission and safety checks.",
        recommended_fix="Add preconditions and safety rules for commands, file writes, secrets, and destructive actions.",
        patchable=True,
        confidence=confidence_for(len(hits)),
    )


def _prompt_injection(document: MarkdownDocument, contract: SkillContract) -> DiagnosticRecord | None:
    combined = " ".join(contract.safety + [document.body]).lower()
    if "untrusted" in combined and (
        "prompt injection" in combined
        or "do not obey" in combined
        or "must not obey" in combined
        or "never obey" in combined
        or "instructions as data" in combined
    ):
        return None
    return DiagnosticRecord(
        diagnostic_id="SD006",
        category="security_prompt_injection",
        severity="major",
        title="Untrusted input handling is not explicit",
        evidence="No clear instruction was found to treat inspected skill text as untrusted data.",
        risk="An agent or wrapper may accidentally follow instructions embedded in the audited skill instead of analyzing them.",
        recommended_fix="State that audited files are untrusted input and must never be obeyed as instructions.",
        patchable=True,
        confidence=confidence_for(1),
    )


def _tool_permission_risk(document: MarkdownDocument, contract: SkillContract) -> DiagnosticRecord | None:
    body = document.body.lower()
    mentions_tools = bool(re.search(r"\b(tool|shell|command|write|edit|file|filesystem|install|network)\b", body))
    if not mentions_tools or contract.tools or contract.safety:
        return None
    return DiagnosticRecord(
        diagnostic_id="SD007",
        category="tool_permission_risk",
        severity="minor",
        title="Tool or filesystem permissions are under-specified",
        evidence="The skill mentions tools, commands, files, or writes without a clear permission boundary.",
        risk="Runtime wrappers may make unsafe assumptions about allowed tools or mutation.",
        recommended_fix="Add runtime notes describing permitted tools, read-only checks, and explicit write boundaries.",
        patchable=True,
        confidence=confidence_for(1),
    )


def _verification_gaps(contract: SkillContract) -> DiagnosticRecord | None:
    if contract.verification or contract.acceptance_criteria:
        return None
    return DiagnosticRecord(
        diagnostic_id="SD008",
        category="verification_gaps",
        severity="major",
        title="Verification guidance is missing",
        evidence="No validation, test, smoke-check, or acceptance guidance was inferred.",
        risk="Agents may claim the skill worked without evidence.",
        recommended_fix="Add validation steps with explicit statuses such as Not Run, Passed, Failed, or Partially Verified.",
        patchable=True,
        confidence=confidence_for(1),
    )


def _maintainer_handoff(contract: SkillContract) -> DiagnosticRecord | None:
    if contract.handoff:
        return None
    return DiagnosticRecord(
        diagnostic_id="SD009",
        category="maintainer_handoff",
        severity="minor",
        title="Handoff and recovery behaviour is absent",
        evidence="No handoff, recovery, resume, or closeout guidance was inferred.",
        risk="Another agent may be unable to continue safely after interruption or context loss.",
        recommended_fix="Add concise recover and handoff instructions for durable artifacts and validation status.",
        patchable=True,
        confidence=confidence_for(1),
    )


def _short(text: str, limit: int = 260) -> str:
    normalized = re.sub(r"\s+", " ", text.strip())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."
