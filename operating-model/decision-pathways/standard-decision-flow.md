---
schema: sc4le-standard-v1
title: "Standard SC4LE Decision Flow"
tags: ["decision-flow", "governance", "pathways"]
owner: "Scott Zebedee"
status: "draft"
version: "1.0.3"
updated: "2026-08-22"
description: "The standardised decision flow used across SC4LE, showing how decisions move through teams, LDAs, CDAs, and leadership."
---


# Standard Decision Flow

## 1. Purpose
The Standard Decision Flow defines how decisions move through the SC4LE federated governance system. It ensures decisions are made at the lowest responsible level, with escalation only when thresholds are exceeded.

## 2. Scope
Applies to all decisions made by:
- operational teams
- Local Design Authorities (LDAs)
- Central Design Authority (CDA)

## 3. Decision Flow (Mermaid)

```mermaid
    flowchart TD
        A[Team identifies decision] --> B[Apply SC4LE principles]

        B --> C{Reversible,<br/>low-risk,<br/>local impact?}
        C -->|Yes| D[Team decides]
        C -->|No| E{Contextual,<br/>domain-specific?}

        E -->|Yes| F[LDA decides]
        E -->|No| G[Cross-domain,<br/>high-impact,<br/>ethical/regulatory risk]

        G --> H[CDA decides]

        D --> I[Decision logged]
        F --> I
        H --> I

        I --> J[Sensing loop captures impact]
```

## 4. Decision Rights Summary
- Teams: reversible, low-risk, local decisions
- LDAs: contextual, domain-specific decisions
- CDA: enterprise, ethical, regulatory, systemic decisions

## 5. Behaviours
- clarity
- transparency
- principle-driven judgement
- minimal escalation

## 6. Anti‑Patterns
- unnecessary escalation
- decision hoarding
- bypassing LDAs
- opaque decision-making

## 7. Maturity Indicators
- reduced decision latency
- fewer escalations
- consistent principle interpretation
