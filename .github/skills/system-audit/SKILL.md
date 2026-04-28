---
name: system-audit
description: 'Mandatory technical validation. Use when: finishing a feature, initializing a stack, or creating new instructions.'
roles: [tech-lead, appsec, qa]
---

# SKILL: Quality & Integrity Audit

## CONTEXT
This skill ensures that all generated code, configurations, and documentation adhere to professional engineering standards and the specific rules of this framework.

## CHECKLIST

### 1. Architectural Integrity (@tech-lead)
- [ ] **SRP**: Does every new file have a single responsibility?
- [ ] **DRY**: Are there obvious duplications of logic or config?
- [ ] **Coupling**: Is the new feature properly decoupled from unrelated modules?
- [ ] **Standard Compliance**: Does the folder structure match the chosen stack's conventions?

### 2. Security (@appsec)
- [ ] **No Secrets**: Are there API keys, passwords, or PII in the code?
- [ ] **Input Validation**: Are all external inputs sanitized/validated?
- [ ] **Permissions**: Are file permissions and access levels appropriate?

### 3. Framework Alignment (@qa)
- [ ] **TSON Integrity**: Are the `.tson` files regenerated and valid?
- [ ] **Context Economy**: Is the new feature adding unnecessary noise to the context?
- [ ] **Discovery**: Can the new files be found by `discovery.py`?

## PROTOCOL
1. If any item is marked [ ], the task is **NOT** complete.
2. Use `context7` to verify the latest standards if the stack is new.
3. Produce an `ADR` (Architecture Decision Record) if a significant standard was changed or established.
