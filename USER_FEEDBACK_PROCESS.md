# AlphaMind AI v3 — User Feedback Triage & Processing Protocol

**Date**: August 5, 2026  
**Build Version**: `v3.0.0-beta`  

---

## 1. Feedback Submission Channels

1. **In-App Feedback Modal (`/settings`)**: Users select feedback type (**General Feedback**, **Report a Bug**, **Feature Request**), enter details, and submit directly to the backend queue.
2. **Global Beta Admin Queue (`/beta-admin`)**: Displays real-time categorized submissions, bug triage priority badges, browser environment tags, affected page routes, and app version.

---

## 2. Categorization Rules

Every item in the queue is assigned exactly one category:
- **Bug**: Functional breakdown, calculation defect, or API request error.
- **UI Issue**: Visual layout misalignment, contrast issue, or spacing problem.
- **AI Quality**: Hallucination, low confidence score output, or citation gap.
- **Performance**: High latency, slow chart rendering, or SSE reconnection delay.
- **Feature Request**: New feature or component proposal from beta users.
- **Other**: Miscellaneous inquiry or general comment.

---

## 3. Mandatory Bug Metadata Context

Every bug submission automatically captures:
- **Affected Page Route** (e.g. `/mission-control`, `/v2-fund`, `/risk`)
- **User Browser & OS Environment** (e.g. `Chrome 127.0 (macOS)`)
- **Timestamp (UTC)**
- **Platform Version** (`v3.0.0-beta`)

---

## 4. Export & Reporting Tools

- **CSV Export**: `GET /api/v1/admin/beta/feedback/export?format=csv` or click **Export CSV** in `/beta-admin`.
- **JSON Export**: `GET /api/v1/admin/beta/feedback/export?format=json` or click **Export JSON** in `/beta-admin`.
- **Weekly Summary**: Generated via `GET /api/v1/admin/beta/summary`.
