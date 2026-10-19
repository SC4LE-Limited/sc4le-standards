# Foundations

The Foundations layer defines the core concepts, principles, architectural assumptions and shared language that underpin SC4LE.

It provides the intellectual and structural basis upon which all operating models, governance structures, standards, practices and services are built.

The Foundations layer exists to create coherence without unnecessary centralisation. It establishes the shared understanding that enables federated autonomy, consistent decision-making and organisational adaptability.

Foundations are intentionally stable, relatively slow-changing and expected to outlive individual operating-model implementations.

They are not operational procedures or implementation guidance. They are the load-bearing architecture of SC4LE.

---

# 1. Purpose of the Foundations Layer

The Foundations layer exists to:

- establish the core principles that guide behaviour and decision-making
- define the underlying concepts and architectural patterns that shape SC4LE
- provide shared language and conceptual clarity across organisations, CDAs, LDAs and teams
- create alignment without requiring heavy governance
- reduce cognitive load through common mental models
- support federated autonomy without fragmentation
- maintain coherence as SC4LE evolves across domains and implementations

The Foundations layer answers:

> Why does SC4LE work the way it does?

It does not define implementation details.

Implementation guidance belongs within the Operating Model, Standards and Operating Practices layers.

---

# 2. Foundation Architecture

The Foundations layer operates through a defined architecture of artefacts.

```text
Narrative Architecture
          ↓
SC4LE Meta-Principles
          ↓
Principle Interpretation
          ↓
Operating Model
          ↓
Standards and Practices
```

Each layer derives its context from the layers above it and provides context for the layers below it.

The purpose of the Foundations layer is to establish and explain the first three levels of this architecture.

---

# 3. What Foundations Contain

## 3.1 Narrative Architecture

The Narrative Architecture explains the worldview, assumptions and conceptual patterns that underpin SC4LE.

It establishes:

- why SC4LE exists
- how SC4LE views organisations and complexity
- the relationship between principles, governance and adaptation
- the conceptual structure of the SC4LE pattern

Primary artefact:

- `sc4le-narrative-architecture.md`

---

## 3.2 SC4LE Meta-Principles

The Meta-Principles are the authoritative behavioural and decision-making guardrails for SC4LE.

They define the core principles that apply across:

- governance
- operating models
- enablement
- sensing
- delivery
- continuous improvement

The principles are normative.

They define what must remain true.

Primary artefact:

- `sc4le-principles.md`

---

## 3.3 Principle Interpretation

The Principle Interpretation Guide explains how the Meta-Principles collectively shape and govern the SC4LE system.

It provides:

- architectural interpretation
- behavioural interpretation
- operating-model context
- organisational significance
- principle relationships

The interpretation guide is explanatory rather than normative.

It explains how the principles are expressed.

Primary artefact:

- `principle-interpretation-guide.md`

---

# 4. Relationship to the Operating Model Layer

The Foundations layer establishes the concepts and principles that guide SC4LE.

The Operating Model layer defines how those principles are expressed through:

- governance structures
- authority boundaries
- decision pathways
- sensing mechanisms
- enablement approaches
- organisational rhythms

The Operating Model does not redefine the principles.

It operationalises them.

The Operating Model should be understood as the primary structural expression of the principles operating together as a coherent system.

---

# 5. Governance of Foundation Artefacts

The Central Design Authority (CDA) is responsible for stewarding the Foundations layer.

Changes to foundation artefacts should be approached with caution because they influence every downstream layer of SC4LE.

Changes to foundation artefacts should normally originate from the CDA or be reviewed and ratified by the CDA before adoption.

When updating a foundation artefact:

1. Preserve alignment with existing principles and architectural intent.
2. Avoid introducing competing terminology or alternative frameworks.
3. Ensure changes remain consistent with the Narrative Architecture.
4. Assess impacts on the Operating Model and supporting standards.
5. Maintain clarity and minimise unnecessary complexity.

Foundation artefacts should evolve when understanding improves, not in response to local implementation preferences.

---

# 6. Relationship Between Foundation Artefacts

The relationship between the core foundation artefacts is:

| Artefact | Purpose |
|-----------|----------|
| `sc4le-narrative-architecture.md` | Explains the SC4LE worldview, assumptions and conceptual model |
| `sc4le-principles.md` | Defines the authoritative normative principles and guardrails |
| `principle-interpretation-guide.md` | Explains how the principles shape and govern the wider SC4LE system |

Together, these artefacts establish the conceptual and behavioural foundations of SC4LE.

Where interpretation guidance conflicts with a normative principle statement, the principle statement takes precedence.

---

# 7. Design Philosophy

The Foundations layer itself should embody the SC4LE principles.

In particular:

- Clarity Over Complexity
- Principles Before Processes
- Federated Autonomy
- Continuous Improvement as Culture

Foundation artefacts should remain concise, understandable and maintainable.

The goal is not to create additional governance.

The goal is to create shared understanding.

---

# 8. Related Repository Layers

The Foundations layer should be read alongside:

- `/operating-model/` – structural expression of SC4LE
- `/standards/` – governed implementation standards
- `/founder-operating-practices/` – documented operational practices and organisational memory

Together these layers provide a complete view of SC4LE from principle through implementation.

```text
Narrative Architecture
        ↓
Meta-Principles
        ↓
Principle Interpretation
        ↓
Operating Model
        ↓
Standards
        ↓
Founder Operating Practices
```
