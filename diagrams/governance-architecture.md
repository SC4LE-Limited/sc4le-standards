---
schema: sc4le-diagram-v1
title: "Governance Architecture Diagram"
diagram_type: "governance-architecture"
source_file: "governance-architecture.md"
tags: ["diagram", "governance", "architecture", "sc4le"]
---


# SC4LE Governance Architecture Diagram

This diagram shows how governance flows through the SC4LE federated model:  
Executive Leadership → Shared Principles → CDA → LDAs → Operational Teams → Sensing → Improvement.

```mermaid
flowchart TD

    A["Executive Leadership"] --> B["Shared Principles"]

    B --> C["Central Design Authority (CDA)"]

    C --> D1["Local Design Authority\n(LDA 1)"]
    C --> D2["Local Design Authority\n(LDA 2)"]
    C --> D3["Local Design Authority\n(LDA 3)"]

    D1 --> E1["Operational Teams"]
    D2 --> E2["Operational Teams"]
    D3 --> E3["Operational Teams"]

    E1 --> F["Sensing Signals"]
    E2 --> F
    E3 --> F

    F --> G["Insight and Analysis"]
    G --> H["Governance Adjustments"]
    H --> C

    H --> I["Continuous Improvement"]
    I --> E1
    I --> E2
    I --> E3

```
