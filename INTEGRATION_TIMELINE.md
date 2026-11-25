# Retrace: Master Integration Timeline

This document sequences all phases from `PLAN_CODEX.md`, `PLAN_CURSOR.md`, and `PLAN_ANTIGRAVITY.md` against the eight project integration gates (G0 to G7). It defines the critical path, parallel tracks, cross-agent handoffs, and estimated review times for Praveen.

---

## 1. Integration Gates Overview

| Gate | Name | Core Deliverables Merged | What It Unblocks |
| --- | --- | --- | --- |
| **G0** | Repo Exists | Root workspace scaffold (CX-00), Compose baseline (CU-00), Frontend preflight (AG-00) | All library, contract, and primitive development |
| **G1** | Shared Libs and Contracts Frozen | Contracts skeleton (CX-01), Shared libraries (CX-02..CX-05), CI pipeline (CU-01), Gateway (CU-02), Frontend API layer and MSW mocks (AG-01..AG-04) | All service implementations; frontend offline development against MSW mocks |
| **G2** | Identity and Tenancy | Core control plane, accounts, orgs, provisioning (CX-06..CX-10), Ingestion skeleton (CU-03, CU-04), Migration runner (CU-17), Frontend auth and org screens (AG-05, AG-06) | Ingestion tenant schema; live authentication cutover |
| **G3** | Incident and Evidence Contracts Published | Incidents API (CX-11), Audit log (CX-12), Ingestion connectors, normalization, discovery, snapshots, timeline, and internal API (CU-05..CU-13), Frontend incident, preview, and timeline screens (AG-07..AG-12) | AI pipeline integration with Ingestion timeline; frontend live timeline cutover |
| **G4** | Draft Loop | AI model adapter and pipeline stages S0 to S13 (CX-18..CX-22), Blameless checker (CX-23), Inline AI SSE (CX-24), Postmortem storage (CX-13), Frontend editor, citations, suggestions, and review (AG-13..AG-18) | End-to-end incident drafting and editing; cross-service integration test suite |
| **G5** | Close the Loop | Review lifecycle and approvals (CX-14), Action items (CX-15), Exports and jobs (CX-16), Analytics (CX-17), Notifications and reminders (CU-14..CU-16, CU-18), Frontend action board, analytics, exports, notifications, and cutover (AG-19..AG-23) | Full product loop; complete workflow execution against live backend |
| **G6** | Deployable | Isolation and contract hardening (CX-25), AI evaluation package (CX-26), Docker image builds (CU-20), Azure IaC (CU-21), Observability (CU-22), Backups and pooling (CU-23), Frontend a11y audit (AG-24) | Demo infrastructure and cloud staging environment |
| **G7** | Release Candidate | Docs update (CX-27), Demo seed data (CU-24), E2E integration suite (CU-25), Release hardening (CU-26), Playwright E2E suite (AG-25), P1 extras (AG-26) | Final capstone live demonstration |

---

## 2. Gate-by-Gate Execution Sequence and Parallel Tracks

```
           CODEX (Backend Foundation & Brains)     CURSOR (Integrations & Platform)        ANTIGRAVITY (Frontend & Hallmark UI)
GATE G0    CX-00 (Repo Scaffold)                   CU-00 (Compose Baseline)                AG-00 (Frontend Preflight)
           ----------------------------------------[ GATE G0 PASSES ]-------------------------------------------------
GATE G1    CX-01 (Contracts & ADRs)                CU-01 (CI Skeleton)                     AG-01 (Design System Tokens)
           CX-02 (retrace_common)                  CU-02 (Traefik Gateway)                 AG-02 (Shared Primitives)
           CX-03 (retrace_auth)                                                            AG-03 (AppShell & Routing)
           CX-04 (retrace_tenancy)                                                         AG-04 (API Client & MSW Mocks)
           CX-05 (retrace_events)
           ----------------------------------------[ GATE G1 PASSES ]-------------------------------------------------
GATE G2    CX-06 (Core Skeleton & Control DB)      CU-03 (Ingestion Skeleton)              AG-05 (M01 Auth Screens)
           CX-07 (Accounts & Sessions)             CU-04 (Connections & Secrets)           AG-06 (M02 Orgs & Switcher)
           CX-08 (OAuth & /me Profile)             CU-17 (Migration Runner Container)
           CX-09 (Orgs, Members, Invitations)
           CX-10 (Tenant Registry & Provisioning)
           ----------------------------------------[ GATE G2 PASSES ]-------------------------------------------------
GATE G3    CX-11 (Core Schema & Incidents)         CU-05 (PagerDuty Connector & Webhook)   AG-07 (M03 Dashboard)
           CX-12 (Audit Log & Hash Chain)          CU-06 (Slack History Fetcher)           AG-08 (M04 Incidents List/Detail)
                                                   CU-07 (Service Catalog)                 AG-09 (M05 Integrations View)
                                                   CU-08 (Evidence Normalization)          AG-10 (M06 Service Catalog View)
                                                   CU-09 (Discovery & Scoring Job)         AG-11 (M21 Jobs & M07 Preview)
                                                   CU-10 (Evidence Snapshots & Stale)      AG-12 (M08 Timeline View)
                                                   CU-11 (Timeline Builder)
                                                   CU-12 (Ingestion Internal API)
                                                   CU-13 (Ingestion Hardening)
           ----------------------------------------[ GATE G3 PASSES ]-------------------------------------------------
GATE G4    CX-13 (Postmortem Storage & Autosave)   (Integration support & monitoring)      AG-13 (M09 Generation & Settings)
           CX-18 (AI Skeleton & Adapter)                                                   AG-14 (M10 TipTap Editor Core)
           CX-19 (AI Pipeline S0 to S3)                                                    AG-15 (Citations & Claim Kinds)
           CX-20 (AI Pipeline S4 to S6)                                                    AG-16 (Inline AI SSE & Comments)
           CX-21 (AI Pipeline S7 to S9)                                                    AG-17 (M11 Blameless Panel)
           CX-22 (AI Pipeline S10 to S13)                                                  AG-18 (M12 Review & M13 Versions)
           CX-23 (Blameless Checker)
           CX-24 (Inline AI & Section Regenerate)
           ----------------------------------------[ GATE G4 PASSES ]-------------------------------------------------
GATE G5    CX-14 (Review Lifecycle & Approvals)    CU-14 (Notifications Skeleton)          AG-19 (M17 Exports & Library)
           CX-15 (Action Items & Stalled Logic)    CU-15 (Reminders Daily Scan)            AG-20 (M14 Action Items Board)
           CX-16 (Exports Engine & Public Jobs)    CU-16 (Email Delivery & Templates)      AG-21 (M19 Notifs & M15 Analytics)
           CX-17 (Analytics Engine)                CU-18 (Event Consumers & Relays)        AG-22 (M18 Audit Log Chain View)
                                                   CU-19 (GitHub Connector, Optional)      AG-23 (Cutover MSW to Live Gateway)
           ----------------------------------------[ GATE G5 PASSES ]-------------------------------------------------
GATE G6    CX-25 (Isolation & Contract Hardening)  CU-20 (Docker Images & Staging CD)      AG-24 (A11y & States Audit)
           CX-26 (AI Evaluation Package)           CU-21 (Azure Infrastructure IaC)
                                                   CU-22 (Observability & Dashboards)
                                                   CU-23 (Backups & PgBouncer)
           ----------------------------------------[ GATE G6 PASSES ]-------------------------------------------------
GATE G7    CX-27 (Docs Update & Final Alignment)   CU-24 (Demo Seed Dataset)               AG-25 (Playwright Core Loop E2E)
                                                   CU-25 (E2E Integration Test Suite)      AG-26 (P1 Command Palette, Opt)
                                                   CU-26 (Release Hardening & Runbooks)
           ------------------------------------[ FINAL RELEASE CANDIDATE ]--------------------------------------------
```

---

## 3. Critical Path and Dependencies

The critical path determines the minimum calendar time to complete Retrace. The sequential bottlenecks are:

1. **Repo and Environment Baseline (Gate G0):** CX-00 and CU-00 must establish the workspace before any code can be committed.
2. **Contracts and Shared Libraries (Gate G1):** Codex phases CX-01 through CX-05 build the foundation (`retrace_common`, `retrace_auth`, `retrace_tenancy`, `retrace_events`). All services depend on these libraries.
3. **Identity and Tenancy (Gate G2):** Codex CX-06 through CX-10 establish the control plane and provisioning worker. Cursor CU-17 must match with the migration runner. This unblocks tenant-scoped schemas in Ingestion and Notifications.
4. **Evidence and Timeline Pipeline (Gate G3):** Ingestion phases CU-05 through CU-12 build the normalization and timeline builder, culminating in the internal timeline API (CU-12). AI pipeline cannot proceed past S0 without this API.
5. **AI Pipeline S0 to S13 and Core Integration (Gate G4):** Codex CX-18 through CX-22 implement structured generation, deterministic validation, read-only verification, and section assembly, persisting postmortem versions to Core.
6. **Live Cutover and Core Loop (Gate G5):** Antigravity cuts over from MSW mocks to the live gateway in AG-23 across all implemented modules.
7. **Release Candidate (Gate G7):** Cursor's E2E integration test suite (CU-25) and Antigravity's Playwright suite (AG-25) confirm system integrity against live services.

---

## 4. Cross-Agent Handoff Milestones

| Milestone | Producer | Consumer | Artifact / Contract | Unblocks |
| --- | --- | --- | --- | --- |
| **H-01** | Codex (CX-01) | Cursor, Antigravity | `contracts/common/*` (error, pagination, envelope, job schemas) | CU-02 gateway, AG-04 API client |
| **H-02** | Codex (CX-05) | Cursor | `libs/retrace_events`, `retrace_auth`, `retrace_tenancy` | CU-03 ingestion, CU-14 notifications |
| **H-03** | Codex (CX-10) | Cursor | `contracts/events/core/tenant.provisioned.json` and registry client | CU-17 migration runner |
| **H-04** | Codex (CX-11) | Cursor | `contracts/core/openapi.json` (Incidents API) | CU-05 incident reporting, AG-08 incident UI |
| **H-05** | Cursor (CU-12) | Codex | `contracts/ingestion/internal.json` (Internal timeline and snapshot API) | CX-19 AI pipeline S1 evidence packet |
| **H-06** | Codex (CX-22) | Cursor, Antigravity | `contracts/events/ai/draft.ready.json` and Core version persistence | CU-18 notifications consumer, AG-14 editor |
| **H-07** | Codex (CX-15) | Cursor | Core internal stalled items endpoint (`GET /api/v1/internal/action-items/stalled`) | CU-15 reminders scan job |
| **H-08** | Cursor (CU-02) | Antigravity | Gateway routing and local Compose endpoints | AG-23 live backend cutover |

---

## 5. Review Bottleneck Management for Praveen

Because Praveen is the sole reviewer and approver for every pull request, review load is the primary project constraint. The 82 total phases across the three agents are distributed with the following review budget:

### Phase Effort Distribution

| Agent | Total Phases | Small (S, ~20 mins) | Medium (M, ~30 mins) | Large (L, ~35-40 mins) | Total Est. Review Time |
| --- | --- | --- | --- | --- |
| **Codex** | 28 | 2 (40 mins) | 10 (300 mins) | 16 (600 mins) | ~15.7 hours |
| **Cursor** | 27 | 2 (45 mins) | 12 (360 mins) | 13 (485 mins) | ~14.8 hours |
| **Antigravity** | 27 | 2 (40 mins) | 8 (240 mins) | 17 (630 mins) | ~15.2 hours |
| **Total** | **82** | **6 (125 mins)** | **30 (900 mins)** | **46 (1715 mins)** | **~45.7 hours** |

### Guidelines for Review Efficiency

1. **Review in batches by gate:** Wait until all parallel tracks for a gate reach PR stage, review them together to verify contract compatibility, and merge in dependency order.
2. **Standard PR checklist:** Every PR must include the exact document sections implemented, test execution outputs, and for frontend phases, screenshots of all four mandatory states (loading, empty, error, permission-denied).
3. **Decide backlog items early:** Items marked NEEDS PRAVEEN (R-05, R-07, R-08, R-15, R-16, R-17, R-18, R-21) should be answered during Gate G0 and G1 so agents do not pause during execution.
