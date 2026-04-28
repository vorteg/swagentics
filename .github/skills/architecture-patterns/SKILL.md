---
name: architecture-patterns
description: 'Software architecture and design patterns. Use when: designing system architecture, choosing patterns, creating ADRs, defining interfaces, structuring modules, applying SOLID principles, choosing between monolith/microservices/modular.'
---

# Architecture Patterns

## When to Use
- Designing a new module, service, or system boundary
- Choosing between architectural patterns (Clean Architecture, Hexagonal, CQRS)
- Creating an Architecture Decision Record (ADR)
- Defining interfaces, contracts, or ports

## Core Principles
- **Contract-First:** Define inputs and outputs (interfaces/schemas) before implementation.
- **Interface Segregation:** Keep interfaces small and focused — clients should not depend on methods they don't use.
- **Dependency Inversion:** Depend on abstractions, not concretions. Core business logic should not import infrastructure.
- **High Cohesion, Low Coupling:** Group related functionality together. Minimize dependencies between modules.

## Pattern Selection Guide

| Scenario | Pattern | Why |
|----------|---------|-----|
| CRUD with simple domain | Layered (Controller → Service → Repository) | Low overhead, familiar |
| Complex business rules | Clean Architecture (Domain → Application → Infrastructure) | Isolates domain logic |
| Event-driven workflows | CQRS + Event Sourcing | Separates reads from writes |
| Multiple external integrations | Hexagonal / Ports & Adapters | Swappable infrastructure |
| Rapid prototyping | Vertical Slices | Feature-based grouping, fast iteration |

## ADR Template

```markdown
# ADR-NNN: [Title]

## Status: [Proposed | Accepted | Deprecated | Superseded by ADR-NNN]

## Context
[What forces are at play? What is the problem?]

## Decision
[What is the change being proposed?]

## Consequences
[What are the tradeoffs? What becomes easier/harder?]
```
