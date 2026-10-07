# SC4LE Sensing Engine — Architecture & Design Notes  
© 2026 SC4LE Limited

---

## 1. Purpose of This Document

This document explains the **design intent**, **architecture**, and **governance rationale** behind the SC4LE sensing engine (`sense.py`).  
It provides long‑form documentation that does not belong inside the Python file itself.

The sensing engine is part of the **AI‑Assisted Sensing Operating Model**, enabling:

- metadata integrity  
- early drift detection  
- CDA → LDA feedback  
- LDA → CDA escalation  
- continuous improvement  
- governed content generation  

---

## 2. Overview of the Sensing Engine

The sensing engine performs **metadata validation** across the SC4LE Standards repository.

It checks:

- YAML front‑matter  
- schema correctness  
- required fields  
- ownership fields  
- versioning fields  
- updated timestamps  

It produces:

- an **adaptation log**  
- an **outcome dashboard**  

These outputs help LDAs and the CDA maintain structural coherence across the entire SC4LE ecosystem.

---

## 3. Why Metadata Validation Matters

Metadata is foundational to SC4LE governance.

It ensures:

- predictable structure  
- consistent templates  
- correct schema alignment  
- correct versioning  
- correct ownership  
- correct publishing workflows  
- correct sensing outputs  
- correct Copilot Business behaviour  

Without metadata validation, SC4LE would drift over time and lose coherence.

---

## 4. Why Schema Definitions Must Be Governed

Originally, schema definitions were hard‑coded inside `sense.py`.  
This created risks:

- hidden logic  
- duplication  
- drift  
- forgotten updates  
- governance violations  

To fix this, SC4LE now uses:

`/schemas/schema-index.json`


This file is the **single source of truth** for metadata schemas.

`sense.py` loads this file dynamically, ensuring:

- schema evolution is governed  
- editors never touch Python  
- schemas are visible and versioned  
- sensing engine stays aligned with governance  

---

## 5. Skip Rule Rationale

The sensing engine intentionally skips certain files and directories.

### 5.1 Skipped Filenames

- `readme.md`  
- `license.md`  
- `contributing.md`  
- `trademarks.md`  
- `index.md`  

**Reason:**  
These are documentation or legal artefacts.  
They do not require YAML metadata.

### 5.2 Skipped Directories

- `ai-assisted-sensing/`

**Reason:**  
This directory contains sensing output files:

- adaptation log  
- outcome dashboard  

These must not be validated.

### 5.3 Skipped File Types

Only `.md` files are validated.

**Reason:**  
SC4LE Standards use governed Markdown with YAML front‑matter.

---

## 6. Metadata Philosophy

Metadata must be:

- governed  
- consistent  
- predictable  
- machine‑readable  
- human‑readable  
- versioned  
- owned  
- aligned with schemas  

Metadata is not optional.  
It is part of SC4LE’s structural integrity.

---

## 7. Schema Governance Rules

All SC4LE metadata schemas must:

1. Be defined in `/schemas/schema-index.json`  
2. Follow semantic versioning  
3. Include required fields  
4. Include descriptions  
5. Be owned by the Governance Architect  
6. Be updated through CDA review  
7. Be validated by the sensing engine  

No schema may be defined inside code.

---

## 8. Error Message Philosophy

Errors must be:

- actionable  
- clear  
- governed  
- helpful  
- non‑technical  
- aligned with SC4LE tone  

Example:

`metadata_unknown_schema — Schema 'sc4le-role-v1' is not registered.
Add it to schemas/schema-index.json.`


This reduces cognitive load and prevents editor confusion.

---

## 9. Severity Levels

Currently, only **high severity** issues exist:

- missing metadata  
- missing schema  
- missing required fields  

Medium and low severity categories are reserved for future expansion.

---

## 10. Roadmap for Future Enhancements

### 10.1 Medium/Low Severity Classification  
Introduce warnings for:

- outdated metadata  
- missing optional fields  
- non‑critical drift  

### 10.2 Content Schema Validation  
Validate content structure using:

- page-template-schema.json  
- service-definition-schema.json  
- value-proposition-schema.json  

### 10.3 Parallel Sensing  
Parallelise sensing once deterministic ordering is guaranteed.

### 10.4 Sensing Engine CLI  
Add optional command‑line flags:

- `--changed-only`  
- `--schema sc4le-service-v1`  
- `--strict`  

### 10.5 Integration with Copilot Business  
Expose sensing results to Copilot Business for:

- metadata correction  
- drift detection  
- automated governance  

---

## 11. LDA Responsibilities

LDAs must:

- interpret sensing results  
- correct metadata issues  
- escalate structural issues to CDA  
- ensure local artefacts remain governed  
- maintain metadata integrity  

---

## 12. CDA Responsibilities

CDA must:

- approve schema changes  
- maintain the schema index  
- update sensing logic  
- govern metadata standards  
- ensure structural coherence  
- prevent fragmentation  

---

## 13. Change History

### **v1.0.0 — 2026‑10‑07**
- Introduced governed schema index  
- Updated sensing engine to load schemas dynamically  
- Added essential inline notes  
- Created external documentation file  
- Improved error messages  
- Formalised skip rule rationale  

---
