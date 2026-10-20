---
schema: sc4le-standard-v1
title: "SC4LE Golden Source Discovery Impact Assessment Standard"
tags:
  - standards
  - governance
  - discovery
  - golden-source
  - copilot
  - ai-governance
owner: CDA
status: proposed
version: 0.3.0
updated: 2026-10-20
description: "Defines the mandatory discovery impact assessment process used to identify, classify and govern repository changes that could affect discoverability, navigation, authority, metadata, dependencies, Golden Source compliance or understanding across the SC4LE Golden Source."
---

# SC4LE Golden Source Discovery Impact Assessment Standard

© 2026 SC4LE Limited

---

# 1. Purpose

This standard establishes a mandatory governance control intended to prevent:

- discovery drift
- authority drift
- navigation drift
- metadata drift
- dependency drift
- Golden Source drift

across the SC4LE Golden Source.

The standard supports the SC4LE principles of:

- Clarity Over Complexity
- Federated Alignment
- Continuous Improvement
- Flow Over Friction
- Sustainable Governance

The objective is not to increase governance activity.

The objective is to create a lightweight self-regulating feedback loop that automatically identifies the minimum actions required to preserve repository coherence as the Golden Source evolves.

---

# 2. Scope

## 2.1 Applicability

| Applies To | Included |
|------------|-----------|
| Microsoft 365 Copilot | Yes |
| SC4LE AI Agents | Yes |
| CDA Reviews | Yes |
| LDA Reviews | Yes |
| Repository Contributors | Yes |
| Repository Maintainers | Yes |
| Governance Reviews | Yes |
| Pull Requests | Yes |
| Golden Source Change Proposals | Yes |

## 2.2 Covered Change Types

| Change Type | Covered |
|------------|-----------|
| Create | Yes |
| Modify | Yes |
| Move | Yes |
| Rename | Yes |
| Merge | Yes |
| Split | Yes |
| Deprecate | Yes |
| Archive | Yes |
| Remove | Yes |

---

# 3. Discovery Assessment Trigger

A Discovery Impact Assessment is only required when a change could reasonably affect discoverability, authority, navigation, metadata, dependencies, Golden Source compliance or understanding.

## 3.1 Trigger Matrix

| Change Type | Assessment Required |
|------------|------------|
| Grammar correction | No |
| Typographical correction | No |
| Formatting correction | No |
| Non-material wording improvement | No |
| Metadata change | Yes |
| New artefact | Yes |
| Artefact move | Yes |
| Artefact rename | Yes |
| Cross-reference change | Yes |
| New dependency | Yes |
| Dependency removal | Yes |
| New index | Yes |
| Index modification | Yes |
| Navigation change | Yes |
| Governance change | Yes |
| Schema change | Yes |
| Repository structure change | Yes |
| AI instruction change | Yes |

### Editorial Change Exemption

Editorial-only changes are exempt from assessment and are automatically classified as D0.

The exemption applies only where no impact exists beyond the artefact being modified.

---

# 4. Assessment Ownership

| Activity | Owner |
|------------|------------|
| Initial Discovery Impact Assessment | Change Proposer |
| Technical Review | Reviewer |
| Governance Review | Applicable Governance Authority |
| Final Approval | Applicable Governance Authority |
| Exception Approval | Applicable Governance Authority |

The change proposer remains accountable for ensuring the assessment is completed and recorded.

---

# 5. Mandatory Assessment Questions

Every Discovery Impact Assessment must evaluate the proposed change against the following assessment areas.

| Assessment Area | Required Question |
|------------|------------|
| Discoverability | Does the change affect how users or AI systems locate content? |
| Authority | Does the change affect governance authority, ownership or source hierarchy? |
| Navigation | Does the change affect repository navigation? |
| Metadata | Does the change affect metadata, schemas or validation rules? |
| Understanding | Does the change affect interpretation, concepts or terminology? |
| Dependency | Does the change affect referenced artefacts, indexes, manifests, prompts, AI systems or governance controls? |
| Golden Source Compliance | Does the change remain fully aligned with the authoritative SC4LE Golden Source and avoid introducing concepts, terminology, governance structures or interpretations not defined by approved SC4LE content? |

All seven assessment areas must be considered before classification is completed.

---

# 6. Discovery Impact Classification

Every Discovery Impact Assessment must be assigned a Discovery Impact Classification.

Classification must be based on objective repository impact rather than perceived importance.

Where multiple criteria apply, the highest classification reached by any criterion becomes the final classification.

## 6.1 Discovery Impact Classification Decision Table

| Question | D0 | D1 | D2 | D3 |
|-----------|-----------|-----------|-----------|-----------|
| How many artefacts are affected? | 1 | 1–3 | Multiple within one domain | Multiple domains or repository-wide |
| Are file paths changing? | No | Optional | Yes | Yes |
| Are cross-references affected? | No | Local references only | Multiple references within one domain | References across multiple domains |
| Is metadata affected? | No | Single artefact metadata | Multiple artefacts | Schema or repository-wide metadata impact |
| Is navigation affected? | No | Local navigation only | Domain navigation changes | Repository navigation changes |
| Are indexes affected? | No | Optional local index update | Domain index update required | Multiple indexes or repository-level indexes affected |
| Is authority affected? | No | No | Local governance relationships affected | Source hierarchy, ownership model or governance authority affected |
| Is discoverability affected? | No | Local discoverability only | Domain discoverability affected | Repository-wide discoverability affected |
| Is interpretation affected? | No | No | Domain guidance affected | Principles, standards, operating model or AI behaviour affected |
| Is a README update required? | No | Usually not | Domain README update required | Repository README or multiple README updates required |
| Are AI governance artefacts affected? | No | No | Rare | Yes |
| Typical approval level | Normal review | Normal review | Domain owner review | CDA review recommended |

## 6.2 Classification Categories

| Classification | Description |
|------------|------------|
| D0 | No discovery impact |
| D1 | Local discovery impact |
| D2 | Domain discovery impact |
| D3 | Repository discovery impact |

## 6.3 Classification Examples

| Scenario | Classification |
|------------|------------|
| Grammar correction | D0 |
| Formatting correction | D0 |
| Single metadata correction | D1 |
| Local reference update | D1 |
| New playbook in an existing domain | D1 |
| Domain artefact relocation | D2 |
| Domain restructuring | D2 |
| Domain index update | D2 |
| Schema change | D3 |
| Repository restructuring | D3 |
| Source hierarchy change | D3 |
| Discovery Manifest change affecting navigation | D3 |
| Knowledge Instructions update | D3 |
| Copilot Context Manifest update | D3 |

---

# 7. Classification Rules

| Rule | Requirement |
|------------|------------|
| Highest Impact Rule | The highest identified impact becomes the final classification |
| Escalation Rule | If uncertain, select the higher classification |
| Repository Override Rule | Repository-wide artefacts automatically classify as D3 |
| Dependency Rule | Dependencies must be assessed before classification is complete |
| Uncertainty Rule | Uncertainty must be reported and must never reduce classification |

## 7.1 Repository-Wide Override

A change must automatically be classified as D3 if it affects:

- repository structure
- source hierarchy
- schema definitions
- governance authority
- SC4LE Principles
- Operating Model structure
- Discovery Manifest
- Knowledge Instructions
- Copilot Context Manifest
- repository-wide indexes
- repository-wide navigation structures

## 7.2 Uncertainty Handling

Where the correct classification cannot be determined with confidence:

| Ambiguous Result | Final Classification |
|------------|------------|
| D0 or D1 | D1 |
| D1 or D2 | D2 |
| D2 or D3 | D3 |

Uncertainty must never reduce impact classification.

---

# 8. Mandatory Discovery Impact Report

Every completed Discovery Impact Assessment must produce a Discovery Impact Report.

## 8.1 Required Report Structure

| Required Output | Description |
|------------|------------|
| Change | Description of proposed change |
| Classification | D0–D3 |
| Discovery Impact | Discoverability implications |
| Authority Impact | Governance implications |
| Navigation Impact | Navigation implications |
| Metadata Impact | Metadata implications |
| Dependency Impact | Dependency implications |
| Golden Source Compliance Impact | Golden Source alignment implications |
| Understanding Impact | Interpretation implications |
| Required Updates | Required follow-on actions |
| Risks | Identified risks |
| Recommendation | Recommended action |

---

# 9. Discovery Compliance Criteria

An assessment is considered complete only when all mandatory compliance criteria have been satisfied.

| Requirement | Mandatory |
|------------|------------|
| Classification assigned | Yes |
| Discovery impact assessed | Yes |
| Authority impact assessed | Yes |
| Navigation impact assessed | Yes |
| Metadata impact assessed | Yes |
| Dependency impact assessed | Yes |
| Golden Source compliance assessed | Yes |
| Understanding impact assessed | Yes |
| Risks recorded | Yes |
| Required updates identified | Yes |
| Outstanding actions assigned an owner | Yes |
| Residual risks documented | Yes |

Until all mandatory requirements have been satisfied, the Discovery Impact Assessment remains open.

---

# 10. AI Behaviour Requirements

All SC4LE AI systems must execute this standard automatically whenever Golden Source changes are proposed.

## 10.1 Mandatory AI Requirements

| AI Requirement | Mandatory |
|------------|------------|
| Perform assessment before recommendation | Yes |
| Report uncertainty | Yes |
| Surface dependencies | Yes |
| Identify discovery drift risk | Yes |
| Identify authority drift risk | Yes |
| Identify navigation drift risk | Yes |
| Identify metadata drift risk | Yes |
| Identify dependency drift risk | Yes |
| Identify Golden Source drift risk | Yes |
| Recommend minimum corrective actions | Yes |
| Apply highest-impact classification rule | Yes |
| Protect Golden Source authority | Yes |

AI systems must:

- treat the SC4LE Golden Source as authoritative;
- avoid introducing concepts not defined within approved SC4LE content;
- identify potential Golden Source conflicts before recommending changes; and
- assess repository-wide implications before recommending implementation.

---

# 11. Discovery Health Monitoring

The Discovery Impact Assessment Standard operates as a continuous governance feedback loop.

## 11.1 Health Metrics

| Metric | Target |
|------------|------------|
| Metadata compliance | 100% |
| Schema validation success | 100% |
| Broken references | 0 |
| Orphan artefacts | 0 |
| Orphan approved artefacts | 0 |
| Critical artefact discoverability | 100% |
| Repository navigation integrity | 100% |
| Discovery Impact Assessment completion | 100% |
| Critical indexing failures | 0 unresolved |

## 11.2 Feedback Loop

The governance feedback loop operates continuously through:

1. Repository change
2. Impact assessment
3. Risk identification
4. Corrective action
5. Validation
6. Monitoring
7. Continuous improvement

The objective is to detect and correct drift before it becomes embedded in the Golden Source.

---

# 12. Governance Intent

This standard is a governance safeguard.

It is not intended to create governance overhead.

The standard must always be interpreted and applied in a manner consistent with the SC4LE principle of Clarity Over Complexity.

Where multiple governance responses are available, preference should be given to the simplest approach capable of maintaining repository coherence, discoverability and governance integrity.

---

# 13. Consistency Validation

Before approval or amendment of this standard, reviewers must verify alignment with the governing artefacts listed below.

| Governing Artefact | Validation Requirement |
|------------|------------|
| foundations/sc4le-principles.md | No principle conflict introduced |
| foundations/principle-interpretation-guide.md | No interpretation conflict introduced |
| standards/sc4le-knowledge-instructions.md | SC4LE Golden Source remains the authoritative source and no unauthorised concepts, terminology, governance structures or interpretations are introduced |
| standards/copilot-context-manifest.md | AI behaviour remains consistent |
| standards/golden-source-discovery-manifest.md | Discovery assumptions remain aligned |
| schemas/schema-index.json | Metadata remains compliant |

Any identified conflict must be:

- resolved through amendment;
- explicitly accepted by the applicable governance authority; or
- escalated for governance review.

Approval must not proceed while unresolved governance conflicts remain.

---

# 14. Governance

## 14.1 Governance Responsibilities

| Responsibility | Owner |
|------------|------------|
| Standard ownership | CDA |
| Assessment production | Change Proposer |
| Technical review | Reviewer |
| Governance review | Applicable Governance Authority |
| Final approval | Applicable Governance Authority |
| Exception approval | Applicable Governance Authority |
| Discovery health monitoring | CDA or Delegated Steward |

---

# 15. Review Record

| Version | Date | Status | Summary | Owner |
|----------|----------|----------|----------|----------|
| 0.3.0 | 2026-10-20 | Proposed | Consolidated review-ready standard including deterministic impact classification, Golden Source compliance controls, feedback-loop governance and consistency validation controls | CDA |
