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
- Total signals emitted: 0

### Metadata Signals
- metadata_missing_header: 5
- metadata_invalid_schema: 21
- metadata_invalid_version: 0
- metadata_invalid_date: 21
- metadata_missing_tags: 21

### Structural Signals
- structure_missing_section: 117
- structure_invalid_order: 0
- structure_schema_violation: 0

### Naming Signals
- naming_invalid_filename: 0
- naming_taxonomy_violation: 0

## 3. Folder Breakdown
Counts per folder:

### meta/
- metadata issues: 0
- structural issues: 0
- naming issues: 0

### foundations/
- metadata issues: 0
- structural issues: 0
- naming issues: 0

### operating-model/
- metadata issues: 0
- structural issues: 0
- naming issues: 0

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