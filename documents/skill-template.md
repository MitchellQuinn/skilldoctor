# Skill Template

This guide describes how to design, document, package, and validate a reusable
agent skill. It is intended for skills that need clear behaviour across
different agent runtimes, especially when the skill has durable artifacts,
state, validation requirements, handoff behaviour, or runtime-specific
installation paths.

The template favours a layered architecture:

1. A small core contract that defines the skill's rules.
2. A data or artifact model for any files the skill creates or updates.
3. Explicit operation protocols.
4. Thin runtime wrappers.
5. Optional helper tooling.
6. Templates, examples, documentation, and evaluations.

No layer should silently redefine another layer.

## 1. Purpose

Start by writing the purpose in one or two paragraphs.

The purpose must answer:

- What problem does the skill solve?
- What tasks should trigger it?
- What durable outcome should exist after it runs?
- What does it deliberately not do?
- What safety or correctness property does it protect?

Use plain language. Avoid implementation detail in the first paragraph.

Template:

```markdown
# <Skill Name>

<Skill Name> is a reusable, agent-agnostic skill for <task category>.

It helps agents <primary behaviour> by <mechanism>. The skill is intended for
<triggering conditions> and should not be used for <non-triggering conditions>.

The skill does not replace <nearby system or workflow>. It adds <specific layer
or behaviour> so that <desired property> is preserved.
```

## 2. Core Architectural Principle

Define the one rule that keeps the skill coherent.

Good core principles are short, testable, and hard to misinterpret. Examples of
principle shapes:

- Each task has one active state scope.
- Generated artifacts have one human-readable authority.
- Runtime wrappers adapt invocation only.
- Validation claims require evidence or an explicit non-run status.
- Tools automate mechanical steps but do not become the source of truth.

Template:

```markdown
## Core Principle

<One sentence stating the invariant that keeps the skill safe and coherent.>

An agent must <required behaviour>.

An agent must not <forbidden behaviour>.
```

## 3. Separation Of Concerns

Separate the skill into layers. Each layer should have one job.

| Layer | Responsibility | Must Not |
| --- | --- | --- |
| Core standard | Defines required behaviour, invariants, lifecycle, and acceptance criteria. | Depend on one runtime. |
| Data model | Defines durable files, folders, sections, schemas, and status values. | Hide authoritative state in sidecars. |
| Operation protocols | Defines step-by-step permitted operations. | Leave failure behaviour implicit. |
| Runtime wrappers | Adapts the skill to a specific agent environment. | Redefine the core contract. |
| Optional tooling | Automates creation, checks, summaries, or conversions. | Invent new rules outside the standard. |
| Templates | Provides reusable skeletons. | Become normative without the spec saying so. |
| Docs, examples, evals | Teaches and tests the skill. | Override the core contract. |

When a skill is small, some layers can be lightweight. The separation still
matters because it prevents examples, wrappers, or tools from becoming accidental
standards.

## 4. Recommended Repository Structure

Use this layout for a full skill project:

```text
<skill-repo>/
  README.md
  LICENSE
  CHANGELOG.md

  spec/
    SPEC.md
    invariants.md
    lifecycle.md
    ownership-model.md
    validation-model.md
    threat-model.md

  protocols/
    create.md
    adopt.md
    orient.md
    update.md
    validate.md
    recover.md
    handoff.md
    close.md
    supersede.md

  templates/
    <artifact>.md.template
    <sidecar>.json.template

  skills/
    <skill-name>/
      SKILL.md
      templates/
        <bundled-template>.md.template

  wrappers/
    <runtime-name>/
      SKILL.md
      prompt-wrapper.md
      project-instructions-snippet.md
      runtime-capabilities.md

  docs/
    quickstart.md
    installation.md
    anti-patterns.md
    faq.md

  examples/
    <scenario-name>/

  evals/
    README.md
    scenarios/
    rubrics/

  tools/
    <tool-name>/

  tests/
```

For a smaller skill, keep at minimum:

```text
skills/<skill-name>/SKILL.md
spec/SPEC.md
protocols/
templates/
wrappers/<runtime-name>/
docs/quickstart.md
```

## 5. Skill Metadata

The distributable skill should have a trigger-rich `SKILL.md` front matter block.

Template:

```yaml
---
name: <skill-name>
description: Use for <triggering task types>. Helps agents <main action> by <mechanism>. Creates or updates <artifact type> when needed. Maintains <important properties>. Do not use for <clear non-trigger cases>.
---
```

The description should front-load:

- the task types that should trigger the skill
- the artifact or behaviour the skill provides
- the strongest safety or correctness boundary
- the most common non-trigger cases

Avoid vague descriptions such as "helps with project work". A good description
lets an agent decide quickly whether to invoke the skill.

## 6. Core `SKILL.md` Structure

The core `SKILL.md` should be short enough to load into context but complete
enough to run the skill correctly.

Recommended sections:

```markdown
# <Skill Name>

One short paragraph describing when to use the skill.

## Trigger

Use this skill when:
- <trigger>
- <trigger>

Do not use this skill when:
- <non-trigger>
- <non-trigger>

## Core Rule

<The main invariant.>

## Create Or Initialize

Steps for first use.

## Adopt Or Resume

Steps for using an existing state scope, artifact, or task context.

## Maintain

What must be updated, when, and with what statuses.

## Validate

What checks are required, optional, or explicitly not run.

## Handoff And Close

How to prepare the work for another agent or mark the task complete.

## Runtime Notes

What wrappers may adapt and what they must not change.

## Safety

Secrets, privacy, destructive actions, and unsafe assumptions.
```

If the skill includes templates, bundle the minimum templates needed for a copied
skill installation. Do not assume the full repository is available after install.

## 7. Contracts And Invariants

Write contracts as explicit obligations. Use `must`, `must not`, `should`, and
`may` consistently:

- `must`: required for correctness or safety
- `must not`: forbidden behaviour
- `should`: recommended unless there is a good reason
- `may`: allowed but optional

Recommended invariant categories:

- Activation: when the skill is active
- Ownership: who may update each artifact or scope
- Authority: which file or field wins on conflict
- State: allowed lifecycle states and transitions
- Validation: how claims are supported
- Boundaries: what the skill is not allowed to replace
- Safety: privacy, secrets, permissions, and destructive operations
- Consistency: how duplicated data must stay aligned

Template:

```markdown
# Invariants

1. <Artifact or scope> is active only when <condition>.
2. <Human-readable file> is the authority for <state type>.
3. <Machine-readable sidecar> mirrors <authority> and must not contain unique
   authoritative state.
4. Validation claims must include <evidence type> or an explicit status.
5. Runtime wrappers must not redefine <core rule>.
6. Examples are illustrative and do not override the core standard.
7. The skill must not store secrets, credentials, private keys, tokens, or
   unnecessary personal data.
```

## 8. Data And Artifact Model

If the skill creates or updates files, define the artifact model precisely.

For each artifact, document:

- path and naming convention
- required or optional status
- owner or writer
- purpose
- authority level
- required sections or fields
- permitted status values
- update triggers
- safety constraints

Template:

```markdown
## Artifact Responsibilities

### `<primary-artifact>`

Purpose: <human-readable authority for the task state or output>.

Rules:
- Must exist when <condition>.
- Must contain <required sections>.
- Must be updated after <events>.
- Wins if it conflicts with <sidecar or generated summary>.

### `<evidence-or-supporting-artifact>`

Purpose: <supporting material, logs, screenshots, notes, or generated output>.

Rules:
- Must be referenced from the primary artifact when used as evidence.
- Must not contain secrets or unnecessary personal data.
- Should be summarized if too large to review directly.

### `<machine-readable-sidecar>`

Purpose: <optional structured mirror for tools>.

Rules:
- May be regenerated from the primary artifact.
- Must not contain authoritative state absent from the primary artifact.
- Must include a schema version if persisted.
```

## 9. Operation Protocols

Every meaningful operation should have a protocol. Protocols are better than
loose prose because they define preconditions, steps, and failure behaviour.

Use this structure:

```markdown
# Protocol: <Operation Name>

Use this protocol when <trigger>.

## Inputs

- <input>

## Preconditions

- <condition that must be true before starting>

## Steps

1. <step>
2. <step>

## Failure Behaviour

If <failure condition>, <required response>.

## Postconditions

- <state that must be true after success>
```

Common protocols:

- Create or initialize a new state scope or artifact.
- Adopt an existing state scope or artifact.
- Orient before implementation.
- Update progress, assumptions, discoveries, and decisions.
- Record validation evidence.
- Recover after interruption or context loss.
- Produce a handoff note.
- Close completed work.
- Supersede obsolete work.

Not every skill needs every protocol. Include only operations that agents must
perform consistently.

## 10. Runtime-Specific Wrappers

Wrappers adapt the core skill to a runtime. They are thin by design.

A wrapper may define:

- install path for that runtime
- how the runtime exposes session, thread, or task identity
- how to invoke the skill
- runtime-specific command syntax
- file permission assumptions
- subagent or parallel-agent behaviour
- hooks or project instruction snippets
- known limitations

A wrapper must not:

- change the core artifact schema
- invent lifecycle states or statuses
- loosen ownership rules
- hide authoritative state in runtime-only memory
- make examples normative
- bypass validation expectations

Recommended wrapper files:

```text
wrappers/<runtime-name>/
  SKILL.md
  prompt-wrapper.md
  project-instructions-snippet.md
  runtime-capabilities.md
```

The runtime capabilities file should answer:

- Does the runtime expose a stable session or thread ID?
- Can it create and edit files?
- Can it run shell commands?
- Can it run tests?
- Does it support native skills?
- Does it support project-level instructions?
- Does it support subagents?
- Does it persist state across sessions?
- What safety or approval constraints apply?

## 11. Optional Tooling

Tooling should automate mechanical operations, not redefine the skill.

Useful tools include:

- `new`: create an artifact or state scope from templates
- `check`: validate required structure and allowed statuses
- `summarize`: produce a compact review or handoff summary
- `list`: discover existing artifacts without adopting them
- `close`: help close completed work
- `supersede`: mark one state scope or artifact replaced by another

Tooling rules:

- Read-only commands must not mutate files.
- Mutating commands must require explicit targets.
- Tools must refuse to overwrite existing artifacts unless the operation is
  explicitly designed to update them.
- Tools must use the same status values, lifecycle states, and ownership rules
  as the core standard.
- Tools must report enough detail for an agent or human to audit what happened.

## 12. Validation Model

Define validation statuses before implementation. Agents need a controlled
vocabulary to avoid overstating correctness.

Example status set:

- `Not Run`
- `Failed`
- `Passed`
- `Partially Verified`
- `Stale`
- `Not Applicable`

Each validation entry should include:

- command, check, or manual review performed
- result status
- evidence or short output summary
- date or checkpoint
- follow-up if failed, stale, partial, or not run

Validation must be proportional. A smoke test does not prove full correctness.
A manual inspection must be labelled as manual. A previously passed check can
become stale after later changes.

## 13. Documentation

Keep documentation practical and layered.

Recommended docs:

- `quickstart.md`: shortest successful path
- `installation.md`: how to install the skill and wrappers
- `concepts.md`: core model and terminology
- `anti-patterns.md`: common failure modes
- `comparison-with-plans.md`: boundaries with nearby workflows
- `multi-agent-use.md`: parent, child, and parallel agent guidance
- `faq.md`: likely user questions

The README should explain:

- what the skill does
- why it exists
- when to use it
- what it provides
- repository layout
- quick start
- validation commands
- release boundary

## 14. Examples And Evaluations

Examples teach usage. Evaluations test whether the skill works under pressure.

Examples should be realistic but non-normative. They may demonstrate:

- normal task flow
- interruption and recovery
- failed validation
- stale assumptions
- handoff
- parallel or subagent work

Evaluation scenarios should include a rubric. Useful rubric dimensions:

- resumability
- auditability
- contamination resistance
- validation quality
- trigger precision
- safety and privacy
- wrapper conformance

Template:

```markdown
# Scenario: <Scenario Name>

## Setup

<Initial task and files.>

## Expected Agent Behaviour

- <behaviour>

## Evaluation Questions

- Can another agent continue without the original chat?
- Are decisions and validation evidence visible?
- Did the agent avoid unrelated state or artifacts?
- Did it mark stale or failed validation accurately?
```

## 15. Anti-Patterns

Call out failures explicitly. Agents respond better to concrete negative rules
than vague warnings.

Common anti-patterns:

- Triggering the skill for trivial one-shot tasks.
- Creating durable state without a clear owner.
- Silently adopting the newest or nearest existing artifact.
- Updating multiple state scopes for one task without explicit coordination.
- Treating examples as normative.
- Letting runtime wrappers fork the core contract.
- Letting tools invent statuses or states.
- Recording aspirational progress instead of actual progress.
- Marking validation as passed without evidence.
- Leaving stale validation marked as current.
- Storing secrets, credentials, private keys, tokens, or unnecessary personal
  data.
- Using the skill as a substitute for tests, source control, issue tracking, or
  project planning.

## 16. Acceptance Criteria

Define what "done" means for the skill itself.

Template:

```markdown
## Acceptance Criteria

The skill is working when:

1. The trigger description selects the intended task types and rejects trivial
   cases.
2. `SKILL.md` contains enough instruction to run the skill after installation.
3. The core contract is documented in `spec/SPEC.md`.
4. Invariants are explicit and testable.
5. Required artifacts, sections, fields, statuses, and lifecycle states are
   defined.
6. Operation protocols define inputs, preconditions, steps, failure behaviour,
   and postconditions.
7. Runtime wrappers adapt invocation mechanics without changing the core
   standard.
8. Optional tooling follows the same rules as the spec.
9. Examples are clearly illustrative.
10. Validation expectations prevent overstated correctness claims.
11. Safety and privacy rules are explicit.
12. A new agent can use the skill from the installed package without reading the
    entire source repository.
```

## 17. Release Checklist

Use this checklist before publishing or copying the skill.

- `SKILL.md` has valid front matter.
- The description contains clear trigger and non-trigger language.
- The core rule is visible near the top of `SKILL.md`.
- Required templates are bundled inside the distributable skill package.
- `spec/SPEC.md` defines the normative behaviour.
- Invariants are short, numbered, and testable.
- Protocols include failure behaviour.
- Status values and lifecycle states are controlled vocabularies.
- Wrappers are thin and do not fork the schema or contract.
- Runtime capability files describe limits rather than changing rules.
- Optional tools are tested.
- Read-only commands are actually read-only.
- Mutating commands require explicit targets.
- Examples do not contain secrets or private data.
- Documentation explains what the skill is not.
- Evaluation scenarios cover interruption, recovery, failed validation, stale
  assumptions, and wrapper conformance when relevant.
- The package can be installed or copied into a fresh environment and used from
  its own files.

## 18. Minimal Skill Package

A minimal release should prove the architecture before adding broad tooling.

```text
<skill-repo>/
  README.md
  LICENSE

  spec/
    SPEC.md
    invariants.md

  protocols/
    create.md
    update.md
    validate.md
    recover.md

  templates/
    <primary-artifact>.md.template

  skills/
    <skill-name>/
      SKILL.md
      templates/
        <primary-artifact>.md.template

  wrappers/
    <runtime-name>/
      SKILL.md
      runtime-capabilities.md

  docs/
    quickstart.md
    anti-patterns.md
```

Add more protocols, tools, examples, and evaluations only when the core contract
is stable enough that they will not encode the wrong behaviour.

## 19. One-Sentence Architecture

Use this sentence shape to test whether the skill is coherent:

```text
<Skill Name> is a layered, agent-agnostic skill in which <activation rule>;
the core standard defines <invariants>, the artifact model defines
<durable state>, protocols define <safe operations>, wrappers adapt the skill
to <runtime environments>, and optional tools <automate mechanical tasks>
without becoming the source of truth.
```
