# AlphaMind AI v3 — Private Beta Operations Guide

**Date**: August 5, 2026  
**Build Version**: `v3.0.0-beta`  
**Scope**: Private Beta Operational Standard Operating Procedures (SOPs)  
**Status**: **ACTIVE — CODE FROZEN**  

---

## 1. Operational Overview & Beta Architecture

AlphaMind AI v3 is currently operating in **Private Beta Execution Mode**. Development is under **CODE FREEZE** — no new feature development or architectural alterations will take place unless fixing a verified Critical or High bug submitted by beta users.

Core Operations Stack:
- **Beta Admin Control**: Accessible via `/beta-admin`
- **User Settings & Diagnostics**: Accessible via `/settings`
- **Feedback & Bug Triage Engine**: REST API `GET/POST /api/v1/admin/beta/feedback`
- **Feedback Export Formats**: CSV (`/api/v1/admin/beta/feedback/export?format=csv`) and JSON (`/api/v1/admin/beta/feedback/export?format=json`)

---

## 2. Bug Triage & Classification Protocol

All incoming issues are triaged according to strict severity rules:

| Severity Level | Definition | SLA Target | Required Linking Metadata |
|---|---|---|---|
| **Critical** | System crash, security flaw, or complete API outage | < 2 Hours | Affected Page, Browser, Timestamp, `v3.0.0-beta` |
| **High** | Major feature unavailable or incorrect calculation | < 8 Hours | Affected Page, Browser, Timestamp, `v3.0.0-beta` |
| **Medium** | Minor UI layout glitch or non-blocking API latency | < 24 Hours | Affected Page, Browser, Timestamp, `v3.0.0-beta` |
| **Low** | Cosmetic tweak, typo, or minor enhancement suggestion | < 72 Hours | Affected Page, Browser, Timestamp, `v3.0.0-beta` |

---

## 3. Weekly Beta Operations Cadence

1. **Daily Triaging**: Review the `/beta-admin` queue every morning; classify incoming submissions into Bug, UI Issue, AI Quality, Performance, Feature Request, or Other.
2. **Weekly Summary Generation**: Call `GET /api/v1/admin/beta/summary` every Friday to compile weekly progress reports.
3. **Data Export**: Export feedback items via CSV/JSON for backlog analysis.
