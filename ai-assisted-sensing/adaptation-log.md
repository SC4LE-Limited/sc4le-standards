---
schema: sc4le-meta-v1
version: 1.0.0
type: sensing-dashboard
status: draft
owner: SC4LE Limited
updated: 2026-08-20
tags:
  - sensing
  - ai-assisted-sensing
  - slice-2
  - dashboard
  - internal
---

# AI‑Assisted Sensing — Outcome Dashboard  
### Full Internal Sensing — Slice 2

## 1. Purpose
This dashboard provides a summary of all sensing signals emitted across SC4LE’s internal standards folders:
- meta/
- foundations/
- operating-model/

It aggregates counts by folder and by signal type to give a clear view of sensing health.

## 2. Dashboard Metrics (Slice 2)
The sensing engine updates these metrics automatically based on entries in adaptation-log.md.

### Total Signals
- Total signals emitted: <count>

### Metadata Signals
- metadata_missing_header: <count>
- metadata_invalid_schema: <count>
- metadata_invalid_version: <count>
- metadata_invalid_date: <count>
- metadata_missing_tags: <count>

### Structural Signals
- structure_missing_section: <count>
- structure_invalid_order: <count>
- structure_schema_violation: <count>

### Naming Signals
- naming_invalid_filename: <count>
- naming_taxonomy_violation: <count>

## 3. Folder Breakdown
Counts per folder:

### meta/
- metadata issues: <count>
- structural issues: <count>
- naming issues: <count>

### foundations/
- metadata issues: <count>
- structural issues: <count>
- naming issues: <count>

### operating-model/
- metadata issues: <count>
- structural issues: <count>
- naming issues: <count>

## 4. Example Summary (Illustrative Only)
This example shows how the dashboard might look after several sensing events:

### Total Signals
- 14

### Metadata Signals
- metadata_missing_header: 3
- metadata_invalid_schema: 2
- metadata_invalid_version: 1
- metadata_invalid_date: 1
- metadata_missing_tags: 2

### Structural Signals
- structure_missing_section: 3
- structure_invalid_order: 1
- structure_schema_violation: 0

### Naming Signals
- naming_invalid_filename: 1
- naming_taxonomy_violation: 0

### Folder Breakdown
#### meta/
- metadata: 5
- structural: 1
- naming: 0

#### foundations/
- metadata: 3
- structural: 2
- naming: 0

#### operating-model/
- metadata: 1
- structural: 2
- naming: 1

## 5. Relationship to Adaptation Log
The dashboard is a derived view of adaptation-log.md.  
Every metric must correspond to one or more log entries.  
No metric may be manually edited without a matching log entry.

## 6. Golden Source Rule
This dashboard is drafted in Confluence.  
It must be migrated to the SC4LE Standards Repo only after Slice 2 verification.

## 7. Future Evolution
Future versions may add:
- trend charts (daily, weekly, monthly)
- severity levels
- remediation tracking
- folder health scores
- sensing coverage indicators
2026-08-21T20:00:27Z | meta/ | governance-standard.md | structure_missing_section:Workflow | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | governance-standard.md | structure_missing_section:Versioning | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | governance-brand.md | structure_missing_section:Scope | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | governance-brand.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | page-templates.md | structure_missing_section:Scope | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | page-templates.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | page-templates.md | structure_missing_section:Workflow | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | website-content-matrix.md | structure_missing_section:Scope | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | website-content-matrix.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | website-content-matrix.md | structure_missing_section:Workflow | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | website-ia.md | structure_missing_section:Scope | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | website-ia.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | website-ia.md | structure_missing_section:Workflow | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | README.md | structure_missing_section:Scope | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | README.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | README.md | structure_missing_section:Workflow | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | messaging-matrix.md | structure_missing_section:Scope | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | messaging-matrix.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | messaging-matrix.md | structure_missing_section:Workflow | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | meta/ | website-publishing-playbook.md | structure_missing_section:Scope | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-principles.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-principles.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-principles.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-principles.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-principles.md | structure_missing_section:Description | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-principles.md | structure_missing_section:Behaviour | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-principles.md | structure_missing_section:Anti‑patterns | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | evidence-base.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | evidence-base.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | evidence-base.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | evidence-base.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | evidence-base.md | structure_missing_section:Description | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | evidence-base.md | structure_missing_section:Behaviour | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | evidence-base.md | structure_missing_section:Anti‑patterns | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-narrative-architecture.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-narrative-architecture.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-narrative-architecture.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-narrative-architecture.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-narrative-architecture.md | structure_missing_section:Description | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-narrative-architecture.md | structure_missing_section:Behaviour | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | foundations/ | sc4le-narrative-architecture.md | structure_missing_section:Anti‑patterns | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | federated-governance.md | metadata_missing_header | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | federated-governance.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | federated-governance.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | federated-governance.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | operating-model-index.md | metadata_missing_header | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | operating-model-index.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | operating-model-index.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | operating-model-index.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | ai-enabled-sensing-operating-model.md | metadata_missing_header | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | ai-enabled-sensing-operating-model.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | ai-enabled-sensing-operating-model.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | ai-enabled-sensing-operating-model.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | ai-enabled-sensing-operating-model.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-federated-governance-standard.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-federated-governance-standard.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-federated-governance-standard.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-federated-governance-standard.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-federated-governance-standard.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-federated-governance-standard.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-federated-governance-standard.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | README.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | README.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | README.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | README.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | README.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | README.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | README.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-operating-model-standard.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-operating-model-standard.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-operating-model-standard.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-operating-model-standard.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-operating-model-standard.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-operating-model-standard.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-operating-model-standard.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-operating-model-standard.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-model-overview.md | metadata_missing_header | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-model-overview.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-model-overview.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-model-overview.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | sc4le-model-overview.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | maturity-model.md | metadata_missing_header | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | maturity-model.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | maturity-model.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | maturity-model.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | maturity-model.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/leadership-cadence.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/leadership-cadence.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/leadership-cadence.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/leadership-cadence.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/leadership-cadence.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/leadership-cadence.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/leadership-cadence.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/leadership-cadence.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/sensing-cadence.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/sensing-cadence.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/sensing-cadence.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/sensing-cadence.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/sensing-cadence.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/sensing-cadence.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/sensing-cadence.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/sensing-cadence.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/flow-cadence.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/flow-cadence.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/flow-cadence.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/flow-cadence.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/flow-cadence.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/flow-cadence.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/flow-cadence.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/flow-cadence.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/improvement-cadence.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/improvement-cadence.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/improvement-cadence.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/improvement-cadence.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/improvement-cadence.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/improvement-cadence.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/improvement-cadence.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | rhythms/improvement-cadence.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/standard-decision-flow.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/standard-decision-flow.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/standard-decision-flow.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/standard-decision-flow.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/standard-decision-flow.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/standard-decision-flow.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/standard-decision-flow.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/standard-decision-flow.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/cda-decision-guide.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/cda-decision-guide.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/cda-decision-guide.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/cda-decision-guide.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/cda-decision-guide.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/cda-decision-guide.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/cda-decision-guide.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/cda-decision-guide.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/escalation-thresholds.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/escalation-thresholds.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/escalation-thresholds.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/escalation-thresholds.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/escalation-thresholds.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/escalation-thresholds.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/escalation-thresholds.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/escalation-thresholds.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/lda-decision-guide.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/lda-decision-guide.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/lda-decision-guide.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/lda-decision-guide.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/lda-decision-guide.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/lda-decision-guide.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/lda-decision-guide.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | decision-pathways/lda-decision-guide.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-insight-architect.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-insight-architect.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-insight-architect.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-insight-architect.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-insight-architect.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-insight-architect.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-insight-architect.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-insight-architect.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-flow-architect.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-flow-architect.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-flow-architect.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-flow-architect.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-flow-architect.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-flow-architect.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-flow-architect.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-flow-architect.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/cda.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/cda.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/cda.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/cda.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/cda.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/cda.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/cda.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/cda.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-academy-lead.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-academy-lead.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-academy-lead.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-academy-lead.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-academy-lead.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-academy-lead.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-academy-lead.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-academy-lead.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-governance-architect.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-governance-architect.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-governance-architect.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-governance-architect.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-governance-architect.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-governance-architect.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-governance-architect.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-governance-architect.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-enablement-lead.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-enablement-lead.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-enablement-lead.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-enablement-lead.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-enablement-lead.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-enablement-lead.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-enablement-lead.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/sc4le-enablement-lead.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/lda.md | metadata_invalid_schema | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/lda.md | metadata_invalid_date | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/lda.md | metadata_invalid_owner | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/lda.md | metadata_missing_tags | metadata_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/lda.md | structure_missing_section:Domains | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/lda.md | structure_missing_section:Cadences | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/lda.md | structure_missing_section:Decision pathways | structure_non_compliant | Governance Workspace
2026-08-21T20:00:27Z | operating-model/ | roles/lda.md | structure_missing_section:Roles | structure_non_compliant | Governance Workspace
