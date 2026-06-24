from __future__ import annotations

from dataclasses import dataclass, field
import re

from .parse_markdown import MarkdownDocument, normalize_title, section_map


@dataclass(frozen=True)
class SkillContract:
    purpose: str = ""
    use_when: list[str] = field(default_factory=list)
    do_not_use_when: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    preconditions: list[str] = field(default_factory=list)
    failure_behavior: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
    handoff: list[str] = field(default_factory=list)
    safety: list[str] = field(default_factory=list)


SECTION_ALIASES = {
    "use_when": {"trigger", "use_when", "when_to_use", "activation", "purpose"},
    "do_not_use_when": {"do_not_use", "do_not_use_when", "non_goals", "non_triggers", "out_of_scope"},
    "inputs": {"inputs", "input", "requirements", "preconditions"},
    "outputs": {"outputs", "output", "artifacts", "deliverables", "required_outputs"},
    "tools": {"tools", "tooling", "runtime_notes", "permissions"},
    "preconditions": {"preconditions", "requirements", "before_you_start"},
    "failure_behavior": {"failure_behaviour", "failure_behavior", "errors", "fallback"},
    "acceptance_criteria": {"acceptance_criteria", "done", "definition_of_done"},
    "verification": {"validate", "validation", "test", "tests", "verification"},
    "handoff": {"handoff", "recover", "recovery", "resume", "close"},
    "safety": {"safety", "security", "threat_model", "privacy"},
}


def infer_contract(document: MarkdownDocument) -> SkillContract:
    sections = section_map(document)
    frontmatter_description = document.frontmatter.get("description", "")
    purpose = _first_paragraph(document.body)
    fields: dict[str, list[str]] = {name: [] for name in SECTION_ALIASES}

    for title, content in sections.items():
        for field_name, aliases in SECTION_ALIASES.items():
            if title in aliases or any(alias in title for alias in aliases):
                fields[field_name].extend(_extract_items(content))

    if frontmatter_description:
        fields["use_when"].extend(_sentences_with(frontmatter_description, ["use", "when", "for"]))
        fields["do_not_use_when"].extend(_sentences_with(frontmatter_description, ["do not", "not use", "except"]))

    for bullet in document.bullets:
        text = bullet.text
        normalized = normalize_title(text)
        if _contains_any(normalized, ["do_not", "not_use", "never", "non_goal"]):
            fields["do_not_use_when"].append(text)
        elif _contains_any(normalized, ["use_when", "when", "trigger"]):
            fields["use_when"].append(text)
        elif _contains_any(normalized, ["input", "target", "requires"]):
            fields["inputs"].append(text)
        elif _contains_any(normalized, ["output", "artifact", "report", "diagnostic"]):
            fields["outputs"].append(text)
        elif _contains_any(normalized, ["test", "validate", "verify", "check"]):
            fields["verification"].append(text)
        elif _contains_any(normalized, ["handoff", "resume", "recover"]):
            fields["handoff"].append(text)
        elif _contains_any(normalized, ["safety", "secret", "untrusted", "prompt_injection"]):
            fields["safety"].append(text)

    return SkillContract(
        purpose=purpose,
        use_when=_dedupe(fields["use_when"]),
        do_not_use_when=_dedupe(fields["do_not_use_when"]),
        inputs=_dedupe(fields["inputs"]),
        outputs=_dedupe(fields["outputs"]),
        tools=_dedupe(fields["tools"]),
        preconditions=_dedupe(fields["preconditions"]),
        failure_behavior=_dedupe(fields["failure_behavior"]),
        acceptance_criteria=_dedupe(fields["acceptance_criteria"]),
        verification=_dedupe(fields["verification"]),
        handoff=_dedupe(fields["handoff"]),
        safety=_dedupe(fields["safety"]),
    )


def _first_paragraph(body: str) -> str:
    for block in re.split(r"\n\s*\n", body.strip()):
        cleaned = block.strip()
        if cleaned and not cleaned.startswith("#"):
            return cleaned
    return ""


def _extract_items(content: str) -> list[str]:
    items: list[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        stripped = re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", stripped).strip()
        if stripped:
            items.append(stripped)
    return items


def _sentences_with(text: str, needles: list[str]) -> list[str]:
    found: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        lower = sentence.lower()
        if any(needle in lower for needle in needles):
            found.append(sentence.strip())
    return found


def _contains_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = re.sub(r"\s+", " ", item.strip())
        key = normalized.lower()
        if normalized and key not in seen:
            seen.add(key)
            result.append(normalized)
    return result

