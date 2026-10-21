---
title: "GitHub Development Workflow"
owner: "Scott Zebedee"
status: "draft"
version: "0.1.0"
updated: "2026-10-21"
tags:
  - repository
  - github
  - workflow
  - founder-operating-practice
description: "Personal operating practice for evolving and maintaining the SC4LE Golden Source repository."
---

# GitHub Development Workflow

## Purpose

This operating practice documents how the SC4LE Golden Source is typically evolved and maintained.

It is intended to provide a practical, repeatable way of making repository changes while preserving traceability, discoverability and governance alignment.

This is guidance rather than governance.

---

## When to Use This Practice

Use this workflow for:

- creating new artefacts;
- updating existing artefacts;
- repository alignment activities;
- operating model maintenance;
- standards maintenance;
- founder operating practice maintenance;
- Golden Source governance improvements.

---

## Standard Workflow

```text
Issue
↓
Discovery
↓
Ready
↓
In Progress
↓
Review
↓
Done
```

The GitHub Project is used to track workflow status.

---

## Step 1 - Create an Issue

Create an issue before starting significant work.

Typical issue structure:

- Problem
- Current State
- Desired State
- Related Artefacts
- Impact Assessment
- Success Criteria

Minor editorial corrections may be completed without creating an issue.

---

## Step 2 - Perform Discovery

Review existing Golden Source content before proposing changes.

Typical discovery activities:

- identify related artefacts;
- check for existing standards;
- review dependencies;
- identify affected domains;
- assess governance implications.

Discovery may conclude that no change is required.

---

## Step 3 - Move to Ready

Move the issue to Ready when:

- discovery is complete;
- the problem is understood;
- the proposed approach is clear.

No implementation should begin before discovery is complete.

---

## Step 4 - Create a Branch

Create a branch from the issue.

Example:

```text
11-feature/add-git-workflow-standard
```

Work should be completed in branches rather than directly on the main branch.

---

## Step 5 - Implement Changes

Use:

- GitHub Desktop
- Visual Studio Code

Make changes within the branch only.

Where appropriate:

- update related artefacts;
- maintain consistency with governing standards;
- preserve Golden Source integrity.

---

## Step 6 - Commit Changes

Use meaningful commit messages that describe the outcome.

Examples:

```text
Add Git Workflow Standard

Align Operating Model artefacts

Update repository guidance
```

Avoid vague commit messages.

---

## Step 7 - Push and Create Pull Request

Push the branch and create a Pull Request.

The Pull Request should explain:

- why the change is required;
- what was changed;
- which artefacts were affected;
- any relevant discovery findings.

---

## Step 8 - Review

Review should verify:

- Golden Source alignment;
- consistency with existing artefacts;
- governance implications;
- unintended duplication.

Significant discovery findings should be retained in the issue history.

---

## Step 9 - Merge

Merge the Pull Request once satisfied that the change is complete.

Preferred merge method:

```text
Squash and Merge
```

to preserve a clean repository history.

---

## Step 10 - Close the Issue

Move the issue to Done and capture any lessons learned.

Discovery outcomes are considered valuable even when no repository change is ultimately implemented.

---

## Copilot Usage

Copilot may be used for:

- discovery support;
- content drafting;
- consistency reviews;
- impact assessments;
- repository analysis.

Copilot recommendations remain proposals until reviewed and accepted.

---

## Guiding Principle

```text
Use the lightest process capable of protecting the Golden Source.
```

The objective is not process compliance.

The objective is sustainable evolution of the SC4LE Golden Source.