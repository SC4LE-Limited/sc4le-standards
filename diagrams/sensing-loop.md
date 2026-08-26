---
schema: sc4le-diagram-v1
title: "SC4LE Sensing Loop Diagram"
diagram_type: "sensing-loop"
source_file: "sensing-loop.md"
tags: ["diagram", "sensing", "loop", "sc4le"]
---


# SC4LE Sensing Loop Diagram

This diagram shows the continuous sensing cycle:  
Sensing → Insight → Decision → Action → Outcome → Sensing.

```mermaid
flowchart TD

    A[Sensing Signals] --> B[Insight Generation]
    B --> C[Decision Making]
    C --> D[Action / Intervention]
    D --> E[Outcome Observed]
    E --> A
