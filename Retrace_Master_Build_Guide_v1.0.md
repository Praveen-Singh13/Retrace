# Retrace: Master Build Guide

Version 1.0 | 10 November 2026 | For use with Gemini to generate three agent implementation plans

Hindsight, without the bias.

---

## 0. What this document is and how to use it

This guide is the single brief that explains **how Retrace gets built by three coding agents**. It is not the implementation plans themselves. It is the rulebook and the skeleton from which the three implementation plans are generated.

**Workflow**

1. Attach to Gemini: this guide plus the nine project documents listed in section 1.
2. Paste the generation prompt from section 14.
3. Gemini produces three plans: `PLAN_CODEX.md`, `PLAN_CURSOR.md`, `PLAN_ANTIGRAVITY.md`.
4. Review each plan against sections 5 to 10 of this guide (checklist in section 13).
5. Give each plan to its agent, one phase at a time.

**The three agents**

| Agent | Role | Owns |
| --- | --- | --- |
| Codex | Backend foundation and brains | Repo scaffold, shared libs, contracts skeleton, Core service, AI service |
| Cursor | Backend integrations and platform | Ingestion service, Notifications service, gateway, Docker Compose, CI/CD, Azure infrastructure, migration runner |
| Antigravity | Frontend | The whole `web/` app, built with the already installed **hallmark** skill |

**Praveen's standing rules (apply to every plan)**

- English only. No em-dashes in any generated document or UI copy.
- Each agent works on its own branches and never on `main` directly.
- Every commit is authored by Praveen, never by the agent (section 8).
- Agents may ask Praveen to connect GitHub, supply credentials, or approve a merge. They never guess these.
- Each plan has **20 or more phases**, small enough that an agent can finish one in a single focused session.

---

## 1. Source documents and precedence

Attach all of these. Every phase in every plan must cite the exact sections it relies on.

| # | Document | Version | Governs |
| --- | --- | --- | --- |
| 1 | Retrace PRD | 0.6 | Product intent, requirement IDs |
| 2 | Retrace System Design | labeled 0.3 (Project Context calls it 0.4) | Architecture, service boundaries, endpoint inventory |
| 3 | Retrace Database Design | 0.1 | Tables, columns, indexes, roles |
| 4 | Retrace AI Pipeline Specification | 0.2 | AI behavior, prompts, validation |
| 5 | Retrace API and Event Contracts Specification | 1.0 | Wire contracts, events, errors, concurrency |
| 6 | Retrace Repository Conventions Specification | 1.0 | Tooling, git, CI, naming |
| 7 | Retrace Frontend Design and Workflow | 1.0 | Screens, modules, design system |
| 8 | SRE Postmortem Toil Analysis | n/a | Background research only |
| 9 | Incident Postmortem AI Agent hackathon document | n/a | Background only, not a build source |

**Precedence when documents disagree** (from the Repository Conventions, section 1): confirmed decisions in the API and Repository documents, then AI Pipeline Spec for AI behavior, then API and Event Contracts for wire contracts, then System Design for architecture, then Database Design for persistence, then PRD for intent. Documents 8 and 9 never override anything.

---

## 2. Ownership map (who may touch which path)

Path ownership is the main defense against merge conflicts and cross-agent hallucination. An agent may **read** anything but **write** only its own paths, except through the handoff protocol in section 7.

| Path | Owner | Notes |
| --- | --- | --- |
| `pyproject.toml`, `uv.lock`, `.nvmrc`, `.env.example`, root lint configs | Codex | Cursor and Antigravity request changes through a PR comment or handoff note |
| `libs/retrace_common`, `retrace_auth`, `retrace_tenancy`, `retrace_events` | Codex | Frozen after Gate G1 except by reviewed PR |
| `contracts/common/`, `contracts/core/`, `contracts/ai/`, `contracts/events/core/`, `contracts/events/ai/` | Codex | |
| `contracts/ingestion/`, `contracts/notifications/`, `contracts/events/ingestion/`, `contracts/events/notifications/` | Cursor | |
| `services/core/` | Codex | |
| `services/ai/` | Codex | |
| `services/ingestion/` | Cursor | |
| `services/notifications/` | Cursor | |
| `gateway/`, `infra/`, `.github/workflows/`, `compose.yaml`, `compose.override.yaml.example` | Cursor | |
| `web/` (including `web/src/generated/`) | Antigravity | Generated types come only from the generation command |
| `docs/`, `docs/decisions/` | Shared | One ADR file per decision, never edit another agent's ADR |
| `docs/progress/<agent>.md` | The named agent | One progress file per agent, so no two agents ever edit the same file |
| `services/realtime/` | Nobody in v1 | Later phase. Do not create |

If a task needs a change in a path the agent does not own, it writes a **handoff request** (section 7) and stops that task. It does not edit the other agent's files.

---

## 3. Global build order and integration gates

The three agents run mostly in parallel, but only between **gates**. A gate is a point where specific phases from several agents must be merged and green before any agent proceeds past it.

| Gate | Name | Must be merged first | Unblocks |
| --- | --- | --- | --- |
| G0 | Repo exists | Codex scaffold phase, Cursor infra baseline phase | Everything |
| G1 | Shared libs and contracts skeleton frozen | Codex libs phases, contracts common phase, Cursor CI skeleton and gateway | All service work, frontend API client |
| G2 | Identity and tenancy | Codex accounts, orgs, tenant provisioning; Cursor migration runner | Ingestion tenant schema, frontend auth and org screens against the real backend |
| G3 | Incident and evidence contracts published | Codex incidents API; Cursor evidence, timeline and snapshot contracts | AI pipeline integration, frontend evidence and timeline screens |
| G4 | Draft loop | Codex AI pipeline persisted to Core postmortem versions; Cursor timeline internal API | Frontend generation, editor, blameless, review |
| G5 | Close the loop | Action items, notifications, exports, analytics | Frontend action items, notifications, analytics |
| G6 | Deployable | Cursor Azure deployment, observability | Demo hardening |
| G7 | Release candidate | All isolation, contract and E2E suites green | Demo |

**Rule:** a phase may list dependencies only as phase IDs and gates. "Wait for the backend" is never an acceptable dependency.

**While waiting on a gate**, an agent works only on phases that do not need it. Antigravity builds against a **mock server generated from the OpenAPI contracts** (MSW handlers) until the real backend passes the gate, then cuts over (section 9.3).

---

## 4. Phase design rules (what makes a phase "good")

Every phase in every plan must satisfy all of these:

1. **One coherent change set.** One service or one module, one branch, one PR.
2. **Size limit.** Roughly one agent session of work: about 5 to 15 files changed, not counting generated output and tests. If a phase cannot fit, split it.
3. **Contracts before code.** A phase that adds or changes an API, event or table updates `contracts/` first (or requests it from the owner), then implements.
4. **Tests inside the phase.** Tests are written in the same phase as the feature, never deferred to a later "testing phase".
5. **Verifiable exit.** The phase ends with commands the agent runs and pastes real output for (section 5, field "Verification").
6. **No hidden dependencies.** If it needs something from another agent, that is a named gate or handoff.
7. **Explicit non-goals.** Each phase says what it must not build, to stop scope creep.

### 4.1 Mandatory phase template

Every phase in each generated plan must contain exactly these fields, in this order:

```
PHASE: <AGENT>-<NN> <short name>
GOAL: one or two sentences
OWNER AGENT: Codex | Cursor | Antigravity
BRANCH: <agent>/<NN>-<slug>   (see section 8)
DEPENDS ON: phase IDs and gates (or "none")
READ FIRST: exact document sections and requirement IDs
  (for example "PRD 8.11 ACT-1..ACT-9; DB Design section 5 action_items;
   API Contracts 3.6, 4.1; System Design 20.5")
ALLOWED PATHS: write access list
FORBIDDEN PATHS: everything else, plus any named sensitive path
CONTRACTS TOUCHED: OpenAPI fragments / event schemas created or consumed
TASKS: numbered, concrete, each traceable to a requirement ID
NON-GOALS: what not to build now
TESTS REQUIRED: named test types and the cases that must exist
VERIFICATION: exact commands to run and what passing output looks like
ACCEPTANCE CRITERIA: checkbox list
STOP AND ASK IF: the specific triggers that require asking Praveen or the owner
HANDOFF OUTPUT: what the next agent or phase needs (files, fixtures, notes)
COMMIT AND PR: Conventional Commit scope and PR checklist
PROGRESS ENTRY: the line to add to docs/progress/<agent>.md
```

A plan that omits a field for any phase is incomplete.

---

## 5. Anti-hallucination rules (copy into the top of every plan)

These are binding rules for each agent. They exist because a large multi-document project invites invention.

1. **Documents win over memory.** If a name, field, route, column, event, library API or number is not in the documents or already in the repo, the agent does not invent it. It records an open item and asks.
2. **Search before creating.** Before adding any route, table, event, schema, helper or component, search the repo and `contracts/` for an existing one.
3. **Cite sources in the PR.** The PR description lists the document sections and requirement IDs implemented.
4. **Read installed versions, not training memory.** For Django, DRF, Django Ninja, Celery, TipTap, TanStack Query, shadcn/ui and similar libraries, check the version pinned in the lockfile and read its installed docs or source before using an API. Do not assume an API from memory.
5. **No fabricated results.** The agent only reports tests or commands as passing if it actually ran them in this session and saw the output. It pastes real output. If it cannot run something, it says so.
6. **Unresolved items stay unresolved.** Open items listed in API Contracts section 13 and Frontend section 9 are resolved only through section 10 of this guide (the reconciliation backlog) and an ADR. Never silently pick a value.
7. **Fixtures over imagination.** Cross-service work uses shared fixtures committed under `contracts/` (example payloads, event examples). Agents build against fixtures, not against assumptions about what another service returns.
8. **Small steps, full stops.** After each phase the agent stops, summarizes, and waits for Praveen to merge. It does not start the next phase automatically.
9. **No scope creep.** Features in the "Later" and "P2" lists are not built. P1 items are built only if the plan marks them as optional phases and all P0 phases are done.
10. **No secrets.** Never write real secrets, tokens or personal data into code, fixtures, logs, prompts, commit messages or PR text.
11. **Ask in a structured way.** Questions to Praveen use this form: `QUESTION`, `WHY IT BLOCKS`, `OPTIONS`, `DEFAULT I WOULD USE`.
12. **Do not edit generated files.** `web/src/generated/` changes only via `pnpm generate:api`.
13. **Do not weaken security to make a test pass.** Tenant isolation, role checks, redaction and audit rules are never relaxed for convenience.

---

## 6. Per-agent operating notes

These notes tell Gemini how to shape each plan for the agent's strengths. They are guidance for shaping phases, not claims about product capabilities.

### 6.1 Codex plan (Foundation, Core, AI)

- Strength to lean on: long, well-specified, test-driven backend work with strict contracts.
- Phases should be tightly specified with exact tables, endpoints and state machines, and with the invariant tests written first (tenant isolation, state transitions, citation validation).
- The AI service phases must follow the AI Pipeline Specification stage by stage (S0 to S13), using a **fake provider with scripted outputs** until a real model is configured. No phase may depend on a real LLM being available.
- Prompts live in versioned files, never as inline strings.

### 6.2 Cursor plan (Ingestion, Notifications, platform)

- Strength to lean on: interactive, multi-file integration work and infrastructure wiring.
- Provider-facing phases (Slack, PagerDuty, GitHub) must use **recorded responses and a mock server** for tests. Live provider calls happen only in explicitly marked manual verification steps that use Praveen's test accounts.
- Slack history rate limits (System Design section 15) shape the connector: resumable job, Retry-After handling, own-app option. Gemini must tell Cursor to **check Slack's current documentation before building** and ask Praveen if reality differs.
- Infra phases must not invent Azure values. IaC tool choice is an ADR item (section 10).

### 6.3 Antigravity plan (Frontend)

- Every phase begins with: "Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask."
- The Frontend Design and Workflow document is the spec. Phases are cut by module chapter (M01 to M21) and by screen ID (S-01 to S-69, P0 only unless a plan marks a phase optional).
- Every phase must implement the four mandatory states (loading, empty, error, permission denied), the capability map (`can()`), and 412, 422, 429 and network failure handling (Frontend 5.2, 5.6, 5.7, Definition of Done 8.3).
- Build against the MSW mock server first. Never hand-write fields that the generated types do not contain. GAP items use the documented fallback.
- Dark theme only. Design tokens exactly as in Frontend section 2.

---

## 7. Cross-agent handoff protocol

Because three agents work at once, every dependency crosses a written boundary.

### 7.1 Contracts-first handoff

1. The **producer** agent merges the OpenAPI fragment or event schema into `contracts/` **before** implementing it fully, together with example request, response and event fixtures.
2. The **consumer** agent builds against those fixtures. Antigravity consumes via generated types and MSW handlers. Backend consumers use contract fixtures and fake clients.
3. The producer's implementation must then pass the contract tests against the same fixtures.
4. Any change to a consumed contract after the freeze is a **breaking-change PR**: it needs a handoff note, regenerated frontend types, and updated fixtures, and Praveen's approval.

### 7.2 Handoff request format

When an agent needs something from a path it does not own, it creates a file `docs/handoffs/<from>-to-<to>-<NN>.md`:

```
FROM / TO:
NEEDS: exact change or contract
WHY: requirement ID or acceptance criterion blocked
BLOCKING PHASE:
PROPOSED SHAPE: (optional)
STATUS: open | done
```

The owner picks it up in its next phase. Praveen can see all open handoffs in one folder.

### 7.3 Phase completion note

When a phase ends, the agent appends to its progress file: phase ID, PR link, merged commit, tests run, contracts changed, open items raised, handoffs created or closed.

---

## 8. Git and GitHub protocol

### 8.1 Identity: commits are Praveen's

Every commit must be authored and committed as Praveen.

1. Before the first commit, each agent checks: `git config user.name` and `git config user.email`. If they are not set to Praveen's identity, the agent **stops and asks** Praveen for the exact name and the GitHub-linked email. It does not guess an email.
2. Never use `--author` with another identity. Never set a git identity for an agent.
3. Remove all agent attribution: no `Co-authored-by` trailers, no "Generated with" lines, no agent signature in commit messages or PR text. Each tool has its own setting for commit attribution; the agent checks and turns it off.
4. After the first commit of each session, verify with `git log -1 --format='%an <%ae>%n%cn <%ce>%n%b'` that author and committer are Praveen and the body has no attribution trailer.
5. Praveen's GitHub handle (from his profile) is `Praveen-Singh13`. The agent confirms it before any push.

### 8.2 Connecting GitHub

Agents may ask Praveen to connect or authorize GitHub access. Standard asks:

- the repository URL and whether it exists yet,
- authorization of the agent's GitHub integration for that repository,
- branch protection settings (see 8.4).

Agents never ask Praveen to paste a personal access token into chat. If a token is needed, the agent tells Praveen where to configure it in the tool's own settings.

### 8.3 Branches and commits

- Branch names: `cx/<NN>-<slug>` (Codex), `cu/<NN>-<slug>` (Cursor), `ag/<NN>-<slug>` (Antigravity). Example: `cx/05-events-lib`.
- One phase equals one branch equals one PR.
- Commit format is Conventional Commits: `type(scope): imperative summary`. Scopes: `core`, `ai`, `ingestion`, `notifications`, `gateway`, `web`, `contracts`, `infra`, `libs`, `ci`, `docs`.
- Branch from the latest `main`. Rebase on `main` before opening the PR. Never force-push a branch another agent uses. Never rewrite `main`.

### 8.4 Pull requests

- Protected `main`: all required CI checks plus one approval. Praveen is the approver. Agents never merge their own PR.
- PR body must include: problem and implementation summary, document sections and requirement IDs implemented, services, contracts, migrations, generated files and config affected, test evidence (real output), rollback or compatibility note for schema, event, migration or deployment changes, and linked open items or ADRs.
- A PR that touches `contracts/` must say whether it is breaking.

---

## 9. Integration, testing and quality rules

### 9.1 Required checks for every backend phase

Ruff format and lint, pytest with pytest-django, contract validation, and for any phase touching tenant data: **two-tenant isolation tests** (routes, jobs, caches, event consumers, and direct database role tests where applicable). Tenant isolation tests and AI draft validation are never cut (PRD 15).

### 9.2 Required checks for every frontend phase

ESLint, Prettier, TypeScript check, Vitest with React Testing Library, and Playwright only for the core workflow phases. `pnpm generate:api` must leave no diff. Screenshots of loading, empty, error and permission-denied states in the PR.

### 9.3 Frontend cutover from mocks to real backend

After G2, G3, G4 and G5 respectively, Antigravity runs a **cutover phase** for the modules that became available: switch from MSW to the gateway, fix contract drift by raising handoffs (not by editing backend files), and re-run the E2E flow against the Compose stack.

### 9.4 Cross-agent integration tests

Cursor owns the integration environment (Compose stack plus CI job). It adds end-to-end checks for the core loop (describe, discover, confirm, generate, review, approve, export) as soon as G4 passes. Codex and Antigravity contribute test cases through handoffs.

---

## 10. Reconciliation backlog (resolve before code depends on it)

The source documents contain open items and some mismatches. Gemini must turn each into an **explicit early phase task or ADR**, owned as shown, not leave them for agents to guess. The "Proposed default" column is a suggestion for Praveen to approve or change. Anything marked **Needs Praveen** must be decided by him before the related phase starts.

| ID | Item | Source | Owner | Proposed default (needs approval) |
| --- | --- | --- | --- | --- |
| R-01 | Job resource across services: public `GET /jobs/{job_id}` is Core only, but Ingestion and AI own their own `jobs` tables | API-03, DB 3.3 | Codex | Core exposes the public job endpoint and calls the owning service's internal job endpoint, or records a job stub at creation. Needs an ADR. |
| R-02 | Outbox and inbox lack the event envelope fields (event_id, event_version, tenant, producer, correlation, aggregate_version) | EVT-02 | Codex (libs) with each service | Add a shared migration template in `retrace_events`; each service applies it to its own schema |
| R-03 | Aggregate-version source per aggregate | EVT-01 | Codex | Version counter column on the owning aggregate row, incremented in the same transaction as the outbox write |
| R-04 | Five evidence timestamp fields vs one `occurred_at` column | DB-01 | Cursor | Migration adding `occurred_at_raw`, `observed_at`, `timestamp_precision`, `timezone_known`; make `occurred_at` nullable |
| R-05 | Soft delete vs DB hard-delete statement | API 10.3, DB 2 | Codex | `deleted_at` on important public resources only; incident and org deletion stay destructive. Needs Praveen to confirm which tables. |
| R-06 | Evidence snapshot resource, hash, stale vs cancelled statuses | EVD-01 | Cursor with Codex | New `evidence_snapshots` table in `ingestion`; snapshot id referenced by draft runs and versions; statuses `stale` and `cancelled` |
| R-07 | Rolling 15-version queue vs foreign keys from `approvals.version_id` and `postmortems.approved_version_id` | PM-01 | Codex | Never delete a version referenced by an approval; archive instead of delete. Needs Praveen: archive table or flag? |
| R-08 | Explicit save and restore commands | PM-01, GAP-16 | Codex | `POST /postmortems/{id}/versions` (explicit save) and `POST /postmortems/{id}/versions/{n}/restore` creating a new version. These are new routes, so they need contract approval. Needs Praveen. |
| R-09 | Persistence for AI claims, verifier findings, stage artifacts, evidence snapshot reference | AI 19.2 | Codex | Use `draft_section_runs.output` for claims, add a `draft_run_stages` table for stage hashes and verifier reports |
| R-10 | Notifications needs recipient emails, but Core internal lookup lists display names only | System Design 14 | Codex | Extend the internal user lookup with email, service-token only |
| R-11 | Gateway routing: Core and AI share `/postmortems/{id}/...` paths | System Design 14 and 16 | Cursor | Route by exact path patterns per service, defined in `gateway/` and covered by routing tests |
| R-12 | Webhook public path | API-02 | Cursor | `/api/v1/webhooks/pagerduty/{token}`; needs gateway and OpenAPI entry |
| R-13 | Service-token claims, internal route names and schemas | SEC-01 | Codex | Define in `contracts/common` and per-service internal fragments |
| R-14 | SSE endpoint paths, reconnect, payloads | API-03 | Codex (AI) | Named events `progress`, `result`, `error`, `complete`; paths in AI OpenAPI |
| R-15 | Clarification question delivery and answer endpoint | GAP-15 | Codex | Questions inside the draft result; answers via a new AI or Core endpoint. Needs Praveen (new route). |
| R-16 | Postmortem list endpoint for the library | GAP-01 | Codex | `GET /postmortems` in Core, or keep the Frontend fallback. Needs Praveen. |
| R-17 | Delete incident, org deletion, provisioning retry, sign out of all devices, invitation list and revoke shape | GAP-06, 08, 09, 10 | Codex | Define routes in Core OpenAPI. Needs Praveen (new routes). |
| R-18 | Org switch token call | GAP-11 | Codex | `POST /api/v1/auth/switch-org` returning a new access token. Needs Praveen. |
| R-19 | Page-size defaults, rate limits, retries, backoff, dead-letter retention, polling intervals | CFG-01 | Each service | Single config module per service, labeled provisional |
| R-20 | Default Azure model, quota, verifier model | AI 19.2 | Praveen | Decide after benchmark; Codex builds the adapter and fake provider first |
| R-21 | IaC tool, email provider, custom domain, Kaggle dataset, PgBouncer arrangement | System Design 26 | Cursor | Needs Praveen: Bicep or Terraform; Azure Communication Services Email or SMTP |
| R-22 | Notification settings route placement | GAP-12 | Antigravity | Per-user under `account/`; confirm |
| R-23 | System Design version label | API 1.3 | Codex | Update to v0.4 in the docs update phase |

Any item that adds a new route, table or event is a **contract change** and follows the handoff protocol (section 7). No agent adds these on its own.

---

## 11. Seed phase outlines

Gemini must produce **at least** these phases per plan and may split any of them further. It must not drop a P0 phase. Phase IDs: `CX-nn`, `CU-nn`, `AG-nn`. P1 and optional phases are marked.

### 11.1 Codex plan (Foundation, Core, AI)

| ID | Phase | Key outputs |
| --- | --- | --- |
| CX-00 | Repo scaffold | Monorepo layout, uv workspace, Python 3.12, Ruff, pytest, `.nvmrc`, `.env.example`, `docs/` and ADR template, progress file |
| CX-01 | Contracts skeleton and reconciliation ADRs | `contracts/common` (error, pagination, job, envelope), validation script, ADRs for R-01 to R-03, R-13 to R-14 |
| CX-02 | `retrace_common` | UUIDv7, error types and handler, logging, pagination, crypto helpers |
| CX-03 | `retrace_auth` | JWT verification, permission classes, service tokens |
| CX-04 | `retrace_tenancy` | Tenant context, DB router, connection cache, registry client |
| CX-05 | `retrace_events` | Envelope, publisher interface, outbox relay, inbox, dead-letter |
| CX-06 | Core skeleton and control DB | Django project, control schema (14 tables), migrations |
| CX-07 | Accounts and sessions | Register, login, logout, refresh rotation, verify email, password reset, lockout, security events |
| CX-08 | OAuth and `/me` | Google and GitHub sign-in, memberships in `/me` |
| CX-09 | Organizations, members, invitations | Roles, last-Admin rule, invite lifecycle |
| CX-10 | Tenant registry and provisioning | Registry, `provision_tenant` idempotent job, Key Vault abstraction with local fake, data keys (Gate G2 with CU-17) |
| CX-11 | Tenant core schema and incidents | `core` schema tables, incidents API, `incident.reported` consumer, description command, jobs |
| CX-12 | Audit log | Hash chain, single writer, `audit.recorded` consumer, verify endpoint |
| CX-13 | Postmortem storage and autosave | Postmortems, versions, `PUT` with ETag and If-Match, idempotency (36 hours), rolling-queue handling per R-07 |
| CX-14 | Review lifecycle | Comments, approvals, state machine endpoints, reopen, author-cannot-approve |
| CX-15 | Action items | CRUD, state rules, verify, stalled computation, internal stalled API, events |
| CX-16 | Exports and job endpoint | PDF and Markdown rendering with citations, Blob storage, signed download |
| CX-17 | Analytics | Summary job, three analytics endpoints |
| CX-18 | AI service skeleton | Django Ninja, model settings, adapter, usage counters, connection test |
| CX-19 | AI pipeline S0 to S3 | Authorization, evidence packet, injection screen, observation map, fake provider, versioned prompts |
| CX-20 | AI pipeline S4 to S6 | Claim planning, claim generation, deterministic validator |
| CX-21 | AI pipeline S7 to S9 | Bounded repair, read-only verifier, policy application, graceful degradation |
| CX-22 | AI pipeline S10 to S13 | Section assembly, final validation, persistence to Core, `draft.requested` and `draft.ready`, clarification output |
| CX-23 | Blameless check | Rule pass, rewrite pass, findings API |
| CX-24 | Inline AI and section regenerate | SSE streaming, suggestions, regenerate as new version |
| CX-25 | Isolation and contract hardening | Full two-tenant suite across Core and AI, contract tests, security review |
| CX-26 | Evaluation package | Labeled incident, model benchmark harness, provisional quotas (feeds R-20) |
| CX-27 | Docs update | Update System Design and Database Design to match decisions (R-23, section 10 outcomes) |

### 11.2 Cursor plan (Ingestion, Notifications, platform)

| ID | Phase | Key outputs |
| --- | --- | --- |
| CU-00 | Compose baseline | `compose.yaml`, override example, Postgres, Redis, local blob and Key Vault substitutes, per-service `.env.example` (parallel with CX-00 on disjoint paths) |
| CU-01 | CI skeleton | Path-aware GitHub Actions, lint, tests, contract validation, lockfile checks, coverage publishing |
| CU-02 | Gateway | Traefik routing (R-11, R-12), JWT verification, CORS, rate limiting, request ids, routing tests (Gate G1) |
| CU-03 | Ingestion skeleton | Django, DRF, Celery, using libs; ingestion schema part 1 |
| CU-04 | Connections and secrets | Integration connections, envelope-encrypted secrets, allowlists |
| CU-05 | PagerDuty | Connector, signed webhook, stale timestamp rejection, sync job, `incident.reported` |
| CU-06 | Slack | OAuth connect, resumable history fetch, Retry-After, own-app and export-upload fallback per ADR |
| CU-07 | Service catalog | Services and links with allowlist rule |
| CU-08 | Evidence normalization | Five timestamp fields (R-04), redaction rules, deduplication |
| CU-09 | Discovery | Search plan, scoring, `discover_evidence` job, evidence APIs, preview and confirm |
| CU-10 | Evidence snapshots | Snapshot resource, include or exclude flow, stale and cancel signals (R-06) |
| CU-11 | Timeline builder | Merge, bursts, key moments, phases, discrepancies, manual events, timeline APIs |
| CU-12 | Ingestion internal API | Timeline and evidence for AI, service-token only (Gate G3) |
| CU-13 | Ingestion hardening | Injection signals, rate-limit tests, isolation tests |
| CU-14 | Notifications skeleton | Schema, in-app notifications API, settings API |
| CU-15 | Reminders | Daily scan, stage logic, `reminder_log` uniqueness, Core internal client |
| CU-16 | Email | Adapter, `email_log`, templates, retention |
| CU-17 | Migration runner | Registry-driven, per-tenant per-service, concurrency, version recording, failure reporting |
| CU-18 | Event consumers | Notifications consumers and outbox relays for Ingestion and Notifications |
| CU-19 | GitHub connector (stretch, optional) | Deployments, merged pull requests, workflow runs, behind a flag |
| CU-20 | Image build and staging deploy | Image scanning, automatic staging, manual production approval |
| CU-21 | Azure infrastructure | IaC per ADR, Container Apps, Static Web Apps, Key Vault, private networking (Gate G6) |
| CU-22 | Observability | OpenTelemetry, Application Insights, health checks, dashboards |
| CU-23 | Backups and pooling | Per-tenant logical backups, PgBouncer arrangement |
| CU-24 | Demo data | Kaggle seed plus generated messages and deployments, demo tenant flag |
| CU-25 | Integration test environment | Core-loop E2E in CI after G4, cross-service isolation tests |
| CU-26 | Release hardening | Failure injection, rollback notes, runbook docs for each service README |

### 11.3 Antigravity plan (Frontend, hallmark skill)

| ID | Phase | Modules and screens |
| --- | --- | --- |
| AG-00 | Preflight | Confirm hallmark skill, scaffold `web/` (Vite, TypeScript, pnpm, Tailwind, shadcn/ui), lint and test configs |
| AG-01 | Design system tokens | Frontend section 2.1 to 2.5, fonts, theme variables |
| AG-02 | Shared components | Primitives and domain components (2.7), including TimestampLabel and badges |
| AG-03 | Shell and routing | AppShell, sidebar, top bar, router, providers, guards, capability map |
| AG-04 | API layer and mocks | Fetch wrapper (auth, ETag, idempotency, errors), query keys, `pnpm generate:api`, MSW from OpenAPI |
| AG-05 | M01 Auth | S-01 to S-07 |
| AG-06 | M02 Organizations | S-08, S-42 to S-44, SettingUpScreen, switcher |
| AG-07 | M03 Dashboard | S-09 with per-card states, onboarding checklist |
| AG-08 | M04 Incidents | S-10 to S-12, next-step banner |
| AG-09 | M05 Integrations | S-37 to S-39 |
| AG-10 | M06 Services | S-40, S-41 |
| AG-11 | M21 and M07 | JobProgress, `useJob`, evidence discovery and preview S-13, S-14 |
| AG-12 | M08 Timeline | S-15, S-16 |
| AG-13 | M09 and M20 | Generation progress, clarification cards, AI settings S-18, S-45 |
| AG-14 | M10 editor core | TipTap, autosave, ETag, stale dialog, SaveStatus |
| AG-15 | Citations and claim kinds | Citation node, CitationPanel, claim-kind styling, section nav |
| AG-16 | Inline AI and comments | SSE client, SuggestionDiff, comment marks and threads |
| AG-17 | M11 Blameless | S-22 |
| AG-18 | M12 and M13 | Review, approval, history, versions, compare |
| AG-19 | M17 Exports | S-50, S-51 |
| AG-20 | M14 Action items | S-29 to S-32 |
| AG-21 | M19 and M15 | Notifications, analytics S-33 to S-36, S-46, S-47 |
| AG-22 | M18 Audit log | S-48, S-49 |
| AG-23 | Cutover after G2 to G5 | Switch modules from MSW to gateway, raise handoffs for drift |
| AG-24 | Accessibility and states audit | Axe checks, four mandatory states on every data view |
| AG-25 | E2E | Playwright WF-2 against the Compose stack |
| AG-26 | P1 extras (optional) | Command palette (navigation only), other P1 items if schedule allows |

---

## 12. Schedule reality check

The PRD plans about eight weeks, one person. These plans total about 80 phases, run by three agents with Praveen as reviewer and merger. Praveen's review time per PR is the real bottleneck, so:

- Keep PRs small and reviewable. A phase that takes more than about 30 minutes to review should be split.
- Gemini should mark each phase with a rough effort tag (S, M, L).
- Cut order if time runs out (from the PRD): email delivery, analytics, GitHub, extra export formats. Never cut tenant isolation tests, stale-version handling, citation resolution, human-accept for AI, or draft validation.

---

## 13. Review checklist for the generated plans (for Praveen)

Before handing a plan to an agent, confirm:

- [ ] 20 or more phases, each using the template in 4.1 with no field missing.
- [ ] Every phase names exact document sections and requirement IDs in READ FIRST.
- [ ] ALLOWED PATHS match the ownership map in section 2.
- [ ] Dependencies are phase IDs and gates only.
- [ ] Every phase has real verification commands and test cases.
- [ ] Every R-item in section 10 maps to a phase task or ADR.
- [ ] The anti-hallucination rules (section 5) and git protocol (section 8) appear at the top of the plan.
- [ ] Antigravity phases each start with the hallmark skill check.
- [ ] No phase builds Realtime, repeat-incident detection, audit-ready reports, Manager or Viewer roles, 2FA, or other "Later" items.
- [ ] No phase invents a route, event, column or number that is not in the documents or section 10.

---

## 14. Prompt to give Gemini

Paste this together with the attached files.

```
You are a senior technical program planner. I am attaching a master build guide
and the nine Retrace project documents. Read all of them completely before writing.

Task: generate three implementation plans as three separate Markdown files:
PLAN_CODEX.md, PLAN_CURSOR.md, PLAN_ANTIGRAVITY.md.

Requirements:
1. Follow the Retrace Master Build Guide exactly. It overrides anything you assume.
2. Each plan must start with: the agent's role, the ownership map for that agent,
   the anti-hallucination rules (guide section 5), the git protocol (guide section 8),
   the handoff protocol (guide section 7), and the gate table (guide section 3).
3. Each plan must contain at least 20 phases. Use the seed phases in guide section 11
   as a minimum. You may split phases but must not drop any P0 phase.
4. Every phase must use the mandatory template in guide section 4.1, with every field
   filled in. READ FIRST must cite exact document sections and requirement IDs.
5. Convert every item in the reconciliation backlog (guide section 10) into a task or
   ADR in the owning agent's plan, and show where each one lands. Mark the items that
   need my decision as "NEEDS PRAVEEN" and do not decide them yourself.
6. Do not invent any API route, event, table, column, field name or numeric limit that
   is not in the documents. When something is missing, create a QUESTION entry
   using: QUESTION, WHY IT BLOCKS, OPTIONS, DEFAULT I WOULD USE.
7. For Antigravity, every phase must begin with the hallmark skill check.
8. Add an effort tag (S, M, L) and an estimated review time to each phase.
9. After the three plans, produce a single INTEGRATION_TIMELINE.md that sequences all
   phases from the three plans against gates G0 to G7 and shows which phases can run
   in parallel.
10. Write in plain English with no em-dashes. Do not write application code. Plans
    describe what to build and how to verify it, not the implementation.

Before writing, list any contradictions you found between the documents and how the
guide resolves them. If something is unresolvable, ask me instead of guessing.
```

---

## 15. Questions Praveen still needs to answer before or during planning

1. Your exact git name and the GitHub-linked email for commits (agents will stop and ask if not set).
2. Does the GitHub repository exist yet, and what is its URL and visibility?
3. Items marked **Needs Praveen** in section 10: R-05, R-07, R-08, R-15, R-16, R-17, R-18, R-21.
4. Are the Slack, PagerDuty and GitHub test accounts ready for manual verification phases?
5. Is the Azure subscription ready, or should Azure phases wait until the end and keep Docker Compose as the demo fallback (System Design section 26)?

End of document.
