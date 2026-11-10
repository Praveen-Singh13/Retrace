# Implementation Plan: Codex (Backend Foundation and Brains)

## Agent Role and Scope

Codex owns the backend foundation, shared libraries, contracts skeleton, Core service, and AI service for Retrace.

Owner: Codex
Services owned:
- `services/core/` (Identity, control plane, tenancy registry, incidents, postmortems, comments, approvals, action items, analytics, exports, audit log, job status)
- `services/ai/` (Model settings adapter, structured drafting stages S0 to S13, deterministic validation, read-only verifier, blameless checks, inline AI suggestions, usage limits)
Shared components owned:
- Root workspace configs: `pyproject.toml`, `uv.lock`, `.nvmrc`, `.env.example`, root lint configs
- Shared libraries: `libs/retrace_common`, `libs/retrace_auth`, `libs/retrace_tenancy`, `libs/retrace_events`
- Contract directories: `contracts/common/`, `contracts/core/`, `contracts/ai/`, `contracts/events/core/`, `contracts/events/ai/`
- Progress tracking: `docs/progress/codex.md`

---

## Anti-Hallucination Rules

These rules are strictly binding on Codex throughout execution:

1. Documents win over memory. If a name, field, route, column, event, library API, or number is not in the source documents or already in the repository, Codex does not invent it. It records an open item and asks Praveen.
2. Search before creating. Before adding any route, table, event, schema, helper, or component, search the repository and `contracts/` for an existing one.
3. Cite sources in the PR. The PR description lists the exact document sections and requirement IDs implemented.
4. Read installed versions, not training memory. For Django, DRF, Django Ninja, Celery, and other pinned packages, check the version pinned in `uv.lock` and read the installed package documentation or source.
5. No fabricated results. Only report tests or commands as passing if actually run in the session with verified output. Paste real output.
6. Unresolved items stay unresolved. Open items in API Contracts section 13 and Guide section 10 are resolved only through explicit ADRs and Praveen decisions. Never silently pick an unapproved value.
7. Fixtures over imagination. Cross-service work uses shared fixtures committed under `contracts/`. Build against fixtures, not assumptions.
8. Small steps, full stops. After each phase, stop, summarize, and wait for Praveen to review and merge. Do not start the next phase automatically.
9. No scope creep. P2 and Later features (such as Realtime, repeat-incident detection, audit-ready reports, Manager/Viewer roles, 2FA) are forbidden in v1.
10. No secrets. Never write real secrets, tokens, or personal data into code, fixtures, logs, prompts, commit messages, or PR text.
11. Ask in a structured way. Questions use the format: QUESTION, WHY IT BLOCKS, OPTIONS, DEFAULT I WOULD USE.
12. Do not weaken security to make tests pass. Tenant isolation, database role checks, redaction, and audit rules are never relaxed.

---

## Git and GitHub Protocol

1. Author identity: Every commit is authored and committed as Praveen. Before the first commit, verify `git config user.name` and `git config user.email`. If not set to Praveen's verified identity, stop and ask. Praveen's GitHub username is `Praveen-Singh13`.
2. Attribution removal: No `Co-authored-by` trailers, no "Generated with" lines, and no agent signatures in commit messages or PR text. Check `git log -1 --format='%an <%ae>%n%cn <%ce>%n%b'` after every commit.
3. Branching: Work exclusively on feature branches named `cx/<NN>-<slug>` (for example `cx/05-events-lib`). Never commit directly to `main`.
4. Commits: Use Conventional Commits (`type(scope): imperative summary`). Scopes for Codex: `core`, `ai`, `contracts`, `libs`, `ci`, `docs`.
5. Pull requests: Rebase on latest `main` before opening PR. PR body includes problem summary, requirement IDs, affected services/contracts, test output, rollback notes, and linked ADRs.

---

## Cross-Agent Handoff Protocol

1. Contracts first: Codex publishes OpenAPI fragments and event schemas to `contracts/` with example fixtures before writing full implementations.
2. Handoff requests: When requesting changes in paths owned by Cursor (`gateway/`, `infra/`, `services/ingestion/`) or Antigravity (`web/`), Codex writes `docs/handoffs/codex-to-<target>-<NN>.md` and stops. It never edits those paths directly.
3. Breaking changes: Any change to frozen contracts after Gate G1 requires a breaking-change PR and explicit Praveen approval.

---

## Integration Gates Summary

| Gate | Name | Must be merged first | Unblocks |
| --- | --- | --- | --- |
| G0 | Repo exists | CX-00, CU-00 | Everything |
| G1 | Shared libs and contracts skeleton frozen | CX-01 to CX-05, CU-01, CU-02 | All service work, frontend API client |
| G2 | Identity and tenancy | CX-06 to CX-10, CU-17 | Ingestion tenant schema, frontend auth |
| G3 | Incident and evidence contracts published | CX-11, CU-08 to CU-12 | AI pipeline integration, frontend timeline |
| G4 | Draft loop | CX-18 to CX-23, CU-11, CU-12 | Frontend generation, editor, blameless |
| G5 | Close the loop | CX-14 to CX-17, CU-14 to CU-16 | Frontend action items, analytics |
| G6 | Deployable | CU-20 to CU-23, CX-25 | Demo hardening |
| G7 | Release candidate | CX-25, CX-26, CU-25, AG-25 | Demo |

---

## Reconciliation Backlog Assignments for Codex

| Item | Topic | Phase / Output | Status |
| --- | --- | --- | --- |
| R-01 | Public Job resource vs service-specific jobs tables | CX-01 (ADR-0001), CX-16 | Core proxies/records job stubs |
| R-02 | Outbox and inbox envelope fields | CX-01 (ADR-0002), CX-05, CX-06 | 11-field standard envelope |
| R-03 | Aggregate-version source per aggregate | CX-01 (ADR-0003), CX-05, CX-11, CX-13 | Version counter on aggregate row |
| R-05 | Soft delete vs DB hard-delete statement | CX-01 (ADR-0004), CX-06, CX-11 | NEEDS PRAVEEN (confirm tables) |
| R-07 | Rolling 15-version queue vs foreign keys from approvals | CX-01 (ADR-0005), CX-13 | NEEDS PRAVEEN (archive table vs flag) |
| R-08 | Explicit save and restore commands | CX-01 (ADR-0006), CX-13 | NEEDS PRAVEEN (new routes) |
| R-09 | Persistence for AI claims, verifier findings, stage artifacts | CX-01 (ADR-0007), CX-18, CX-20 | `draft_run_stages` and output schemas |
| R-10 | Recipient email lookup for Notifications | CX-14, CX-15 | Internal endpoint user email lookup |
| R-13 | Service-token claims and internal route schemas | CX-01 (ADR-0008), CX-03 | Internal JWT claims in `contracts/common` |
| R-14 | SSE endpoint paths, reconnect, payloads | CX-01 (ADR-0009), CX-24 | AI OpenAPI SSE definitions |
| R-15 | Clarification question delivery and answer endpoint | CX-01 (ADR-0010), CX-22 | NEEDS PRAVEEN (new route) |
| R-16 | Postmortem list endpoint for library | CX-01 (ADR-0011), CX-13 | NEEDS PRAVEEN (`GET /postmortems`) |
| R-17 | Missing admin/lifecycle routes (delete incident, org deletion, retry provisioning, sign out all devices) | CX-01 (ADR-0012), CX-07, CX-09, CX-11 | NEEDS PRAVEEN (new routes) |
| R-18 | Org switch token call | CX-01 (ADR-0013), CX-07, CX-08 | NEEDS PRAVEEN (`POST /auth/switch-org`) |
| R-19 | Page sizes, rate limits, timeouts config | CX-02, CX-18 | Provisional configuration module |
| R-20 | Default Azure model, quota, verifier model | CX-18, CX-26 | Feeds Praveen decision |
| R-23 | System Design version label update | CX-27 | Update docs to v0.4 |

---

## Codex Implementation Phases (CX-00 to CX-27)

### PHASE: CX-00 Repo Scaffold
EFFORT: S (Est. review time: 20 mins)
GOAL: Establish the monorepo root structure, Python 3.12 workspace with uv, lint/test tooling, environment templates, and progress tracking file.
OWNER AGENT: Codex
BRANCH: cx/00-repo-scaffold
DEPENDS ON: none (parallel with CU-00 on disjoint paths)
READ FIRST: Repository Conventions sections 2, 4, 5, 10; Master Build Guide sections 2, 8.
ALLOWED PATHS:
- `pyproject.toml`
- `uv.lock`
- `.nvmrc`
- `.env.example`
- `ruff.toml`
- `pytest.ini`
- `docs/progress/codex.md`
- `docs/decisions/`
- `libs/`
- `services/core/`
- `services/ai/`
- `contracts/`
FORBIDDEN PATHS: `gateway/`, `infra/`, `compose.yaml`, `web/`, `services/ingestion/`, `services/notifications/`, `services/realtime/`
CONTRACTS TOUCHED: none
TASKS:
1. Initialize Python 3.12 root workspace configuration in `pyproject.toml` with `uv` workspace members (`libs/*`, `services/core`, `services/ai`).
2. Pin root Ruff linting and formatting configuration enforcing language-standard conventions.
3. Pin pytest and pytest-django root configuration.
4. Create `.nvmrc` with current Node.js LTS version.
5. Create initial root `.env.example` containing non-secret template variable definitions.
6. Create `docs/progress/codex.md` with phase tracking table and initial status.
7. Create ADR template in `docs/decisions/0000-adr-template.md`.
NON-GOALS: Do not create Docker Compose files or CI workflows (owned by Cursor in CU-00 and CU-01). Do not create frontend directories.
TESTS REQUIRED: Tooling tests: `uv run ruff check .`, `uv run pytest --version`.
VERIFICATION:
```bash
uv run ruff check .
uv run pytest
```
Output: Ruff checks pass with zero errors; pytest recognizes configuration.
ACCEPTANCE CRITERIA:
- [ ] Root `pyproject.toml` defines valid `uv` workspace for Python 3.12.
- [ ] Ruff formats and lints with no errors.
- [ ] `docs/progress/codex.md` is present.
- [ ] No files in Cursor or Antigravity owned paths are touched.
STOP AND ASK IF: Praveen has not confirmed git identity (`user.name`, `user.email`).
HANDOFF OUTPUT: Root workspace baseline ready for libraries and Cursor CI integration.
COMMIT AND PR: `chore(repo): scaffold monorepo workspace and python tooling`
PROGRESS ENTRY: `CX-00 | Merged | Repo scaffold, uv workspace, ruff, pytest configs | None | Open`

---

### PHASE: CX-01 Contracts Skeleton and Reconciliation ADRs
EFFORT: M (Est. review time: 30 mins)
GOAL: Establish the shared contracts directory structure, common schemas (errors, pagination, envelope, jobs), schema validation script, and author baseline ADRs for backlog items.
OWNER AGENT: Codex
BRANCH: cx/01-contracts-and-adrs
DEPENDS ON: CX-00, CU-00 (Gate G0)
READ FIRST: API Contracts sections 2.2, 3.3, 3.4, 3.5, 7.2; Master Build Guide section 10 (R-01, R-02, R-03, R-05, R-07, R-08, R-13, R-14, R-15, R-16, R-17, R-18).
ALLOWED PATHS:
- `contracts/common/**`
- `contracts/core/**`
- `contracts/ai/**`
- `contracts/events/core/**`
- `contracts/events/ai/**`
- `scripts/validate_contracts.py`
- `docs/decisions/**`
- `docs/progress/codex.md`
FORBIDDEN PATHS: `contracts/ingestion/`, `contracts/notifications/`, `contracts/events/ingestion/`, `contracts/events/notifications/`, `gateway/`, `web/`
CONTRACTS TOUCHED: `contracts/common/errors.json`, `contracts/common/pagination.json`, `contracts/common/envelope.json`, `contracts/common/job.json`
TASKS:
1. Create directory skeletons for `contracts/common/`, `contracts/core/`, `contracts/ai/`, and event folders.
2. Define `contracts/common/errors.json` matching API Contracts 3.4 standard error shape (`code`, `message`, `details`, `correlation_id`).
3. Define `contracts/common/pagination.json` for cursor and page pagination shapes.
4. Define `contracts/common/envelope.json` for standard 11-field event envelope (API Contracts 7.2).
5. Define `contracts/common/job.json` defining standard 202 response and job state schema.
6. Write python script `scripts/validate_contracts.py` using jsonschema to validate all contract schemas.
7. Draft architectural decision records in `docs/decisions/`:
   - ADR-0001 (R-01): Public job proxying via Core.
   - ADR-0002 (R-02): Shared outbox/inbox schema migration template.
   - ADR-0003 (R-03): Aggregate version counter source.
   - ADR-0004 (R-05): Soft delete scope (NEEDS PRAVEEN).
   - ADR-0005 (R-07): Rolling 15-version retention policy (NEEDS PRAVEEN).
   - ADR-0006 (R-08): Explicit save and restore routes (NEEDS PRAVEEN).
   - ADR-0007 (R-09): AI persistence mapping.
   - ADR-0008 (R-13): Internal service token claims.
   - ADR-0009 (R-14): SSE streaming paths and payloads.
   - ADR-0010 (R-15): Clarification question routes (NEEDS PRAVEEN).
   - ADR-0011 (R-16): Postmortem list endpoint (NEEDS PRAVEEN).
   - ADR-0012 (R-17): Admin deletion and retry routes (NEEDS PRAVEEN).
   - ADR-0013 (R-18): Org switch token endpoint (NEEDS PRAVEEN).
NON-GOALS: Do not implement application endpoints or database models yet.
TESTS REQUIRED: Contract validation tests verifying valid and invalid examples against common schemas.
VERIFICATION:
```bash
uv run python scripts/validate_contracts.py
```
Output: All common contract schemas valid; test fixtures pass schema checks.
ACCEPTANCE CRITERIA:
- [ ] `contracts/common/` contains JSON schemas for error, pagination, envelope, and jobs.
- [ ] `scripts/validate_contracts.py` runs cleanly in CI.
- [ ] ADRs drafted for R-01 through R-18 with NEEDS PRAVEEN items clearly labeled.
STOP AND ASK IF: Praveen has not resolved decisions for R-05, R-07, R-08, R-15, R-16, R-17, R-18.
HANDOFF OUTPUT: Shared contract schemas unblock Cursor (gateway and ingestion) and Antigravity (API client).
COMMIT AND PR: `feat(contracts): establish common schemas and reconciliation adrs`
PROGRESS ENTRY: `CX-01 | Merged | Common contract schemas, validation script, baseline ADRs | contracts/common/* | Open`

---

### PHASE: CX-02 Retrace Common Library (`retrace_common`)
EFFORT: M (Est. review time: 25 mins)
GOAL: Implement `libs/retrace_common` with UUIDv7 generators, standard error classes and handlers, structured logging helpers, pagination utilities, and crypto helpers.
OWNER AGENT: Codex
BRANCH: cx/02-retrace-common
DEPENDS ON: CX-01
READ FIRST: System Design sections 1, 12, 13; Database Design section 2; Repository Conventions section 3.
ALLOWED PATHS:
- `libs/retrace_common/**`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other libraries and services.
CONTRACTS TOUCHED: Consumes `contracts/common/errors.json`, `contracts/common/pagination.json`.
TASKS:
1. Scaffold package `libs/retrace_common` with `pyproject.toml`.
2. Implement UUIDv7 generation utility using standard Python 3.12 / standard library time components.
3. Implement standard exception hierarchy (`RetraceError`, `NotFoundError`, `ConflictError`, `PreconditionFailedError`, `RateLimitError`) serializing to standard error format.
4. Implement DRF and Django Ninja exception handlers converting exceptions to standard error responses with `correlation_id`.
5. Implement structured logging helper attaching `tenant_id`, `request_id`, `correlation_id`, and sanitizing secrets.
6. Implement cursor and page pagination utility classes.
7. Implement cryptographic helper interface for AES-GCM envelope encryption and secure random nonces.
NON-GOALS: Do not implement tenant database routing (owned by `retrace_tenancy`).
TESTS REQUIRED: Unit tests for UUIDv7 uniqueness and monotonic ordering, exception serialization, logging sanitization, crypto encryption/decryption round trips.
VERIFICATION:
```bash
uv run pytest libs/retrace_common/tests
```
Output: 100% unit tests pass covering error serialization, UUIDv7 generation, and encryption helpers.
ACCEPTANCE CRITERIA:
- [ ] `libs/retrace_common` is installable via uv workspace.
- [ ] Exception handlers match `contracts/common/errors.json`.
- [ ] Logging helper strips authorization headers and tokens.
STOP AND ASK IF: Discrepancy found in crypto encryption standard (AES-256-GCM confirmed).
HANDOFF OUTPUT: `retrace_common` library ready for consumption by all services.
COMMIT AND PR: `feat(libs): implement retrace_common package`
PROGRESS ENTRY: `CX-02 | Merged | retrace_common utilities, errors, UUIDv7, crypto | None | Open`

---

### PHASE: CX-03 Retrace Auth Library (`retrace_auth`)
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement `libs/retrace_auth` providing asymmetric JWT verification, JWKS public key rotation support, DRF/Ninja permission classes, and service-token verification.
OWNER AGENT: Codex
BRANCH: cx/03-retrace-auth
DEPENDS ON: CX-02
READ FIRST: System Design section 5; API Contracts section 5.1, 5.2; Database Design section 4 (`jwt_signing_keys`).
ALLOWED PATHS:
- `libs/retrace_auth/**`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other libraries and services.
CONTRACTS TOUCHED: Consumes `contracts/common/errors.json`.
TASKS:
1. Scaffold `libs/retrace_auth` package.
2. Implement asymmetric JWT decoder verifying RS256/EdDSA signatures using published public keys.
3. Support local JWKS caching and graceful key rotation via `kid`.
4. Implement DRF authentication backend `RetraceJWTAuthentication` extracting `user_id`, `org_id`, `role`, and `correlation_id`.
5. Implement Django Ninja security dependency performing identical token extraction.
6. Implement `HasOrgRole` permission class enforcing Admin and Member roles per endpoint.
7. Implement internal service token generator and verifier using mutual service identities and audience claims (R-13).
NON-GOALS: Do not implement user login or token generation endpoints (owned by Core service in CX-07).
TESTS REQUIRED: Unit tests for valid token decoding, expired token rejection, tampered token rejection, unknown `kid` handling, role enforcement, and service-token verification.
VERIFICATION:
```bash
uv run pytest libs/retrace_auth/tests
```
Output: All auth tests pass, verifying token extraction and rejection of unauthorized claims.
ACCEPTANCE CRITERIA:
- [ ] Decodes user access tokens and populates request user and active organization.
- [ ] Rejects cross-tenant tokens or mismatched audience claims.
- [ ] DRF and Ninja permission classes enforce role boundaries.
STOP AND ASK IF: Signing algorithm needs change from RS256.
HANDOFF OUTPUT: `retrace_auth` library unblocks Core, Ingestion, and AI service authentication.
COMMIT AND PR: `feat(libs): implement retrace_auth jwt verification and permissions`
PROGRESS ENTRY: `CX-03 | Merged | retrace_auth JWT and service token validation | None | Open`

---

### PHASE: CX-04 Retrace Tenancy Library (`retrace_tenancy`)
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement `libs/retrace_tenancy` providing thread-safe tenant context, dynamic Django database router, connection caching, and tenant registry lookup client.
OWNER AGENT: Codex
BRANCH: cx/04-retrace-tenancy
DEPENDS ON: CX-03
READ FIRST: System Design sections 4, 23.1; Database Design sections 3.1, 3.2; Repository Conventions section 3.
ALLOWED PATHS:
- `libs/retrace_tenancy/**`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other libraries and services.
CONTRACTS TOUCHED: none
TASKS:
1. Scaffold `libs/retrace_tenancy` package.
2. Implement `tenant_context` using `contextvars` storing active `tenant_id`.
3. Implement `TenantDatabaseRouter` selecting tenant database connection dynamically based on `tenant_context`.
4. Ensure attempts to read or write tenant models without an active tenant context raise explicit `TenantContextMissingError`.
5. Implement connection manager configuring per-tenant connection aliases on demand using cached credentials.
6. Implement tenant registry client interface with local in-memory/Redis caching.
7. Implement middleware setting tenant context from verified request token and ensuring teardown on request completion.
NON-GOALS: Do not implement the provisioning worker job (owned by Core in CX-10).
TESTS REQUIRED: Two-tenant isolation tests verifying queries with tenant A context never access tenant B database; tests verifying missing context raises loud errors.
VERIFICATION:
```bash
uv run pytest libs/retrace_tenancy/tests
```
Output: Multi-tenant database routing tests pass; context violations fail loudly.
ACCEPTANCE CRITERIA:
- [ ] `tenant_context` maintains isolated state per async task/thread.
- [ ] Router routes to tenant database alias accurately.
- [ ] Missing tenant context blocks database access unconditionally.
STOP AND ASK IF: Django version compatibility issues with dynamic database configuration.
HANDOFF OUTPUT: `retrace_tenancy` library unblocks Core and Ingestion multi-tenancy.
COMMIT AND PR: `feat(libs): implement retrace_tenancy router and context isolation`
PROGRESS ENTRY: `CX-04 | Merged | retrace_tenancy router, context manager, isolation guards | None | Open`

---

### PHASE: CX-05 Retrace Events Library (`retrace_events`)
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement `libs/retrace_events` providing the standard 11-field event envelope, event publisher interface with Redis Streams backend, transactional outbox relay, idempotent inbox handler, and dead-letter queue.
OWNER AGENT: Codex
BRANCH: cx/05-retrace-events
DEPENDS ON: CX-04
READ FIRST: API Contracts section 7; System Design section 6.2, 6.4; Database Design section 3.3.
ALLOWED PATHS:
- `libs/retrace_events/**`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other libraries and services.
CONTRACTS TOUCHED: Consumes `contracts/common/envelope.json`.
TASKS:
1. Scaffold `libs/retrace_events` package.
2. Implement Pydantic event envelope class strictly enforcing the 11 fields: `event_id`, `event_type`, `event_version`, `occurred_at`, `tenant_id`, `aggregate_type`, `aggregate_id`, `aggregate_version`, `producer`, `correlation_id`, `payload`.
3. Implement `EventPublisher` abstract base class and `RedisStreamsEventPublisher`.
4. Implement outbox writer helper recording event within current database transaction.
5. Implement outbox relay worker polling unpublished outbox records and publishing to Redis Streams with retry and error tracking.
6. Implement inbox consumer helper recording `(event_id, consumer)` deduplication record, rejecting duplicates, and checking `aggregate_version`.
7. Implement dead-letter stream publisher for unrecoverable consumer failures.
NON-GOALS: Do not implement service-specific event handlers (implemented within each service).
TESTS REQUIRED: Unit and integration tests for envelope validation, outbox transactional atomic commit, outbox relay publishing, duplicate event suppression, out-of-order aggregate version rejection, and dead-letter routing.
VERIFICATION:
```bash
uv run pytest libs/retrace_events/tests
```
Output: Outbox, inbox deduplication, and envelope tests pass with zero failures.
ACCEPTANCE CRITERIA:
- [ ] Envelope strictly validates all 11 fields.
- [ ] Duplicate event delivery causes zero duplicate processing.
- [ ] Stale aggregate versions are detected and safely ignored.
STOP AND ASK IF: Redis connection pooling parameters require tuning.
HANDOFF OUTPUT: Shared libraries frozen (Gate G1 readiness for Codex).
COMMIT AND PR: `feat(libs): implement retrace_events envelope outbox and inbox`
PROGRESS ENTRY: `CX-05 | Merged | retrace_events outbox relay, envelope validation, inbox deduplication | contracts/common/envelope.json | Open`

---

### PHASE: CX-06 Core Service Skeleton and Control Database
EFFORT: M (Est. review time: 30 mins)
GOAL: Scaffold `services/core` Django application, configure control database connection, and implement migrations for all 14 control plane tables.
OWNER AGENT: Codex
BRANCH: cx/06-core-skeleton-control-db
DEPENDS ON: CX-05, CU-02 (Gate G1)
READ FIRST: System Design sections 4.1, 14; Database Design section 4; Repository Conventions section 4.1.
ALLOWED PATHS:
- `services/core/**`
- `contracts/core/**`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/core/openapi.json`
TASKS:
1. Scaffold `services/core` Django 5 / DRF project targeting Python 3.12.
2. Configure settings for dual database access: default control database and tenant database router.
3. Implement Django models for control database:
   - `users`, `oauth_accounts`, `email_tokens`, `refresh_tokens`
   - `organizations`, `memberships`, `invitations`
   - `db_servers`, `tenant_registry`, `tenant_service_roles`, `tenant_keys`
   - `provisioning_runs`, `jwt_signing_keys`, `security_events`
4. Apply standard conventions: UUIDv7 primary keys, UTC timestamptz, snake_case, check constraints for enums.
5. Generate and test initial control migrations.
6. Configure `drf-spectacular` for OpenAPI 3.x schema publication in `contracts/core/`.
NON-GOALS: Do not implement tenant schema tables yet (handled in CX-11).
TESTS REQUIRED: Model integrity tests, unique constraint validation, foreign key cascades, migration idempotency tests.
VERIFICATION:
```bash
uv run python services/core/manage.py makemigrations --check
uv run python services/core/manage.py migrate --database=default
uv run pytest services/core/tests/test_control_models.py
```
Output: All 14 control tables migrated successfully; model constraint tests pass.
ACCEPTANCE CRITERIA:
- [ ] Control database schema contains all 14 tables specified in Database Design section 4.
- [ ] Migrations run cleanly on fresh PostgreSQL control database.
- [ ] `security_events` table is append-only.
STOP AND ASK IF: Praveen decides on table-specific soft delete flags vs deactivation on control tables (R-05).
HANDOFF OUTPUT: Control database ready for authentication and tenancy endpoints.
COMMIT AND PR: `feat(core): scaffold core service and control database schema`
PROGRESS ENTRY: `CX-06 | Merged | Core service scaffold and 14 control database models | contracts/core/openapi.json | Open`

---

### PHASE: CX-07 Accounts, Sessions, and Security Events
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement email/password registration, login, rotating refresh tokens with family revocation, logout, email verification, password reset, lockout throttling, and security audit events.
OWNER AGENT: Codex
BRANCH: cx/07-accounts-and-sessions
DEPENDS ON: CX-06
READ FIRST: PRD 8.1 AUTH-1..AUTH-4, AUTH-6; System Design section 5; API Contracts sections 3.1, 4.1, 5.1; Database Design section 4.
ALLOWED PATHS:
- `services/core/apps/accounts/**`
- `contracts/core/openapi.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/core/openapi.json` (Auth routes)
TASKS:
1. Implement `POST /api/v1/auth/register` with input validation, password hashing, and email token generation.
2. Implement `POST /api/v1/auth/login` validating credentials, checking lockout (`failed_login_count`, `locked_until`), issuing JWT access token, and setting HttpOnly rotating refresh token cookie.
3. Implement `POST /api/v1/auth/refresh` rotating refresh token, revoking whole token family on detected token reuse, and re-issuing access token.
4. Implement `POST /api/v1/auth/logout` revoking active refresh token family.
5. Implement `POST /api/v1/auth/verify-email` and `POST /api/v1/auth/password-reset` request/confirm endpoints (R-17).
6. Implement rate limiting and lockout logic on failed attempts, recording events into `security_events`.
7. Update Core OpenAPI fragment with request/response schemas.
NON-GOALS: Do not build 2FA (P1/Later item).
TESTS REQUIRED: Unit and API tests: successful registration/login, invalid credentials, token refresh rotation, reuse attack detection revoking family, account lockout after repeated failures, password reset flow without user disclosure.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_auth_api.py
```
Output: 100% pass on authentication, rotation, reuse detection, and lockout tests.
ACCEPTANCE CRITERIA:
- [ ] Refresh token cookie is HttpOnly, Secure, SameSite.
- [ ] Token reuse revokes all tokens in the family immediately.
- [ ] Security events recorded for login success/failure and lockout.
STOP AND ASK IF: Praveen wants specific lockout threshold parameters (default 5 attempts, 15 min lock).
HANDOFF OUTPUT: Working auth APIs unblock frontend authentication (AG-05).
COMMIT AND PR: `feat(core): implement accounts authentication session rotation and lockout`
PROGRESS ENTRY: `CX-07 | Merged | User registration, login, rotating refresh tokens, lockout | contracts/core/openapi.json | Open`

---

### PHASE: CX-08 OAuth and User Profile (`/me`)
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement Google and GitHub OAuth sign-in flows and `GET /api/v1/me` returning current user profile, active organization, and tenant memberships.
OWNER AGENT: Codex
BRANCH: cx/08-oauth-and-me
DEPENDS ON: CX-07
READ FIRST: PRD 8.1 AUTH-2; System Design section 5; API Contracts section 4.1; Database Design section 4 (`oauth_accounts`).
ALLOWED PATHS:
- `services/core/apps/accounts/**`
- `contracts/core/openapi.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/core/openapi.json`
TASKS:
1. Implement `GET /api/v1/auth/oauth/{provider}/start` redirecting to GitHub or Google OAuth authorization URL with signed state.
2. Implement `GET /api/v1/auth/oauth/{provider}/callback` exchanging code for provider token, creating or linking `oauth_accounts` row, and issuing session tokens.
3. Implement `GET /api/v1/me` returning user identity, email verification status, active organization, and all memberships with roles.
4. Implement `POST /api/v1/auth/switch-org` issuing a new access token bound to the requested organization ID (R-18, NEEDS PRAVEEN).
5. Update Core OpenAPI contract.
NON-GOALS: Do not connect integration OAuth for Slack/PagerDuty (owned by Ingestion in CU-05, CU-06).
TESTS REQUIRED: Mocked OAuth provider tests for GitHub/Google success and failure; `/me` endpoint returns all memberships; `/switch-org` issues token with updated active org claim.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_oauth_me.py
```
Output: OAuth callback exchanges and `/me` serialization tests pass.
ACCEPTANCE CRITERIA:
- [ ] OAuth accounts link cleanly to existing or new user records.
- [ ] `/me` returns active org and complete membership list.
- [ ] `/switch-org` validates membership before issuing new token.
STOP AND ASK IF: Praveen has provided test OAuth client credentials.
HANDOFF OUTPUT: Complete auth surface published in OpenAPI for Antigravity AG-05 and AG-06.
COMMIT AND PR: `feat(core): implement oauth sign-in and user profile me endpoint`
PROGRESS ENTRY: `CX-08 | Merged | Google/GitHub OAuth callback and /me user profile endpoint | contracts/core/openapi.json | Open`

---

### PHASE: CX-09 Organizations, Members, and Invitations
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement organization creation, organization settings, role management (Admin, Member), last-Admin protection, invitation lifecycle, and invitation acceptance.
OWNER AGENT: Codex
BRANCH: cx/09-orgs-members-invitations
DEPENDS ON: CX-08
READ FIRST: PRD 8.2 ORG-1..ORG-5; System Design section 5; API Contracts section 4.1; Database Design section 4 (`organizations`, `memberships`, `invitations`).
ALLOWED PATHS:
- `services/core/apps/tenants/**`
- `contracts/core/openapi.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/core/openapi.json`
TASKS:
1. Implement `POST /api/v1/orgs` creating organization row with status `provisioning`, assigning creator as Admin membership, and queueing tenant provisioning.
2. Implement `GET` and `PATCH /api/v1/orgs/{org_id}` and settings endpoints.
3. Implement `GET /api/v1/orgs/{org_id}/members` listing members with snapshot names and roles.
4. Implement `PATCH` and `DELETE /api/v1/orgs/{org_id}/members/{id}` enforcing the mandatory rule: an organization must always retain at least one active Admin (ORG-5).
5. Implement `POST /api/v1/orgs/{org_id}/invitations` generating signed expiring invitation token hash and recording invitation row.
6. Implement `POST /api/v1/invitations/accept` validating token, adding user membership, and updating invitation status.
7. Implement invitation revocation and expiration checks.
NON-GOALS: Do not implement Teams or optional Manager/Viewer roles (Later items).
TESTS REQUIRED: Multi-org membership tests; last-Admin removal rejection; invitation expiry and single-use acceptance tests.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_orgs_members_api.py
```
Output: All membership, last-Admin guard, and invitation lifecycle tests pass.
ACCEPTANCE CRITERIA:
- [ ] Organization creation binds creator as Admin.
- [ ] Cannot remove or demote the last active Admin.
- [ ] Invitations expire and cannot be reused once accepted.
STOP AND ASK IF: Invitation email template parameters are finalized.
HANDOFF OUTPUT: Unblocks organization and membership UI (AG-06).
COMMIT AND PR: `feat(core): implement organizations members and invitations lifecycle`
PROGRESS ENTRY: `CX-09 | Merged | Orgs, member roles, last-Admin protection, invitation accept | contracts/core/openapi.json | Open`

---

### PHASE: CX-10 Tenant Registry and Provisioning Job
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement `tenant_registry`, Azure Key Vault abstraction with local fake, per-tenant data key generation, and the idempotent `provision_tenant` Celery job (Gate G2 with CU-17).
OWNER AGENT: Codex
BRANCH: cx/10-tenant-registry-provisioning
DEPENDS ON: CX-09
READ FIRST: System Design sections 4.2, 4.5, 23.2, 23.4; Database Design sections 3.2, 4 (`tenant_registry`, `tenant_keys`, `tenant_service_roles`).
ALLOWED PATHS:
- `services/core/apps/tenants/**`
- `services/core/tasks/**`
- `contracts/events/core/tenant.provisioned.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/events/core/tenant.provisioned.json`
TASKS:
1. Implement Key Vault client wrapper supporting local environment fake and Azure Key Vault in production.
2. Implement tenant data key generation, master key wrapping, and storage in `tenant_keys`.
3. Implement `provision_tenant(tenant_id)` Celery task:
   - Check if database already exists; create `tenant_{id}` if absent.
   - Create schemas: `core`, `ingestion`, `ai`, `notifications`.
   - Create per-service roles with secure random passwords, storing passwords in Key Vault.
   - Run initial migrations for each service against its schema.
   - Mark `tenant_registry` status as `active`.
   - Publish `tenant.provisioned` event via transactional outbox.
4. Make every provisioning step idempotent and safe to retry on failure.
5. Implement internal tenant resolution API used by other services with Redis caching.
NON-GOALS: Do not run migration runner container directly (Cursor owns migration runner in CU-17).
TESTS REQUIRED: Unit and integration tests for provisioning idempotency, Key Vault encryption round trips, and retry resumption after simulated failure.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_provisioning_job.py
```
Output: Provisioning task executes idempotently, creates database/schemas, and publishes event.
ACCEPTANCE CRITERIA:
- [ ] Provisioning creates separate schemas and roles per service.
- [ ] Failure in provisioning leaves status as failed and can be retried without duplicate errors.
- [ ] `tenant.provisioned` event matches standard envelope.
STOP AND ASK IF: Database superuser credentials for local database creation are configured.
HANDOFF OUTPUT: Identity and tenancy ready (Gate G2). Unblocks Ingestion tenant schema and frontend live testing.
COMMIT AND PR: `feat(core): implement tenant registry and idempotent provisioning job`
PROGRESS ENTRY: `CX-10 | Merged | Tenant provisioning job, Key Vault data keys, registry resolution | contracts/events/core/tenant.provisioned.json | Open`

---

### PHASE: CX-11 Tenant Core Schema and Incidents API
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement `core` tenant schema models, incidents CRUD API, author short description endpoint, `incident.reported` event consumer, and `incident.description_submitted` event publisher.
OWNER AGENT: Codex
BRANCH: cx/11-tenant-core-incidents
DEPENDS ON: CX-10
READ FIRST: PRD 8.5 INC-1..INC-4; System Design section 14, 20.1; API Contracts sections 4.1, 7.4; Database Design section 5 (`incidents`, `incident_services`, `incident_responders`).
ALLOWED PATHS:
- `services/core/apps/incidents/**`
- `contracts/core/openapi.json`
- `contracts/events/core/incident.description_submitted.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/core/openapi.json`, `contracts/events/core/incident.description_submitted.json`
TASKS:
1. Implement `core` schema models: `org_settings`, `incidents`, `incident_services`, `incident_responders`, and common tables (`jobs`, `outbox`, `inbox`).
2. Implement `GET /api/v1/orgs/{org_id}/incidents` with page pagination, sorting, and declared filters (`status`, `severity`, `incident_type`).
3. Implement `POST /api/v1/orgs/{org_id}/incidents` creating manual incident.
4. Implement `GET` and `PATCH /api/v1/orgs/{org_id}/incidents/{id}` with `If-Match` ETag concurrency check and validation (`resolved_at >= started_at`).
5. Implement `POST /api/v1/orgs/{org_id}/incidents/{id}/description` taking author short description and publishing `incident.description_submitted` outbox event.
6. Implement `incident.reported` event consumer creating or updating incident reported by PagerDuty.
7. Implement `incident.deleted` cascade handler and outbox publisher (R-17, NEEDS PRAVEEN).
NON-GOALS: Do not implement evidence discovery (owned by Ingestion in CU-09).
TESTS REQUIRED: Two-tenant isolation tests for incidents; ETag optimistic concurrency tests; event consumer idempotency tests; description submission event publishing tests.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_incidents_api.py
```
Output: Incidents CRUD passes; two-tenant isolation verified; description submission outbox event verified.
ACCEPTANCE CRITERIA:
- [ ] Description is the only required author input to trigger discovery.
- [ ] Cross-tenant incident access returns 404.
- [ ] `incident.description_submitted` published to outbox atomically.
STOP AND ASK IF: Deletion cascade requirements on incidents need Praveen clarification.
HANDOFF OUTPUT: Incidents API published (Gate G3 readiness for Codex).
COMMIT AND PR: `feat(core): implement tenant core schema and incidents management api`
PROGRESS ENTRY: `CX-11 | Merged | Core tenant schema, incidents CRUD, description event | contracts/core/openapi.json | Open`

---

### PHASE: CX-12 Audit Log and Hash Chain Verification
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement append-only tamper-evident `audit_log` with SHA-256 hash chaining, per-tenant advisory locking, single-writer consumer for `audit.recorded`, and verification endpoint.
OWNER AGENT: Codex
BRANCH: cx/12-audit-log-hash-chain
DEPENDS ON: CX-11
READ FIRST: PRD 8.14 ADM-1, ADM-2; System Design sections 8, 14; Database Design section 5 (`audit_log`).
ALLOWED PATHS:
- `services/core/apps/audit/**`
- `contracts/core/openapi.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/core/openapi.json`
TASKS:
1. Implement `audit_log` model with fields: `seq`, `occurred_at`, `actor_type`, `actor_user_id`, `actor_name`, `actor_role`, `source_service`, `action`, `entity_type`, `entity_id`, `summary`, `details`, `request_id`, `prev_hash`, `entry_hash`.
2. Configure database permissions on `core.audit_log`: allow INSERT and SELECT only; add PostgreSQL trigger rejecting UPDATE or DELETE.
3. Implement thread-safe audit writer taking per-tenant advisory lock, retrieving previous `entry_hash`, calculating SHA-256 over canonical entry, and inserting row.
4. Implement consumer for `audit.recorded` events from all services, appending records via the single writer.
5. Implement `GET /api/v1/orgs/{org_id}/audit-log` with cursor pagination.
6. Implement `GET /api/v1/orgs/{org_id}/audit-log/verify` recomputing hash chain from genesis and reporting integrity status.
NON-GOALS: Do not build PDF audit-ready export bundle in v1 (Later item).
TESTS REQUIRED: Hash chain integrity verification test; tamper detection test (modifying a row breaks verification); advisory lock concurrency test.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_audit_log.py
```
Output: Chain appends sequentially; verification passes; tampered record detected immediately.
ACCEPTANCE CRITERIA:
- [ ] Database trigger blocks any UPDATE or DELETE on audit log.
- [ ] Verification detects any payload or sequence modification.
- [ ] Cross-service `audit.recorded` events write to chain reliably.
STOP AND ASK IF: First genesis entry hash definition needs adjustment (32 zero bytes confirmed).
HANDOFF OUTPUT: Audit log ready for all services to emit audit events.
COMMIT AND PR: `feat(core): implement tamper-evident hash chained audit log`
PROGRESS ENTRY: `CX-12 | Merged | Hash-chained audit log, verification endpoint, single writer | contracts/core/openapi.json | Open`

---

### PHASE: CX-13 Postmortem Storage, Autosave, and Version Management
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement postmortem working draft storage, `PUT /postmortems/{id}` autosave with ETag/If-Match, 36-hour Idempotency-Key support, 15-version rolling queue, and version archiving per R-07.
OWNER AGENT: Codex
BRANCH: cx/13-postmortem-storage-versions
DEPENDS ON: CX-12
READ FIRST: PRD 8.9 REV-1, REV-4; System Design section 14, 22; API Contracts sections 3.6, 6.4, 10.2; Database Design section 5 (`postmortems`, `postmortem_versions`).
ALLOWED PATHS:
- `services/core/apps/postmortems/**`
- `contracts/core/openapi.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/core/openapi.json`
TASKS:
1. Implement `postmortems` and `postmortem_versions` models.
2. Implement `GET /api/v1/orgs/{org_id}/incidents/{id}/postmortem` returning working draft ProseMirror JSON with `ETag`.
3. Implement `PUT /api/v1/orgs/{org_id}/postmortems/{id}` accepting ProseMirror JSON, requiring `If-Match` header, updating revision counter and returning new `ETag` (returns 412 on mismatch).
4. Implement 36-hour idempotency key cache for postmortem mutations.
5. Implement immutable named version creation on generation, submit, approve, publish, and restore triggers.
6. Enforce 15-version rolling queue retention rule: never purge versions referenced by `approvals` or `approved_version_id` (R-07, NEEDS PRAVEEN).
7. Implement `GET /api/v1/orgs/{org_id}/postmortems/{id}/versions` listing version metadata and snapshots.
8. Implement `POST /api/v1/orgs/{org_id}/postmortems/{id}/versions` for explicit saves (R-08, NEEDS PRAVEEN).
9. Implement `GET /api/v1/orgs/{org_id}/postmortems` library endpoint (R-16, NEEDS PRAVEEN).
NON-GOALS: Do not build Yjs real-time co-editing in v1.
TESTS REQUIRED: ETag optimistic concurrency test (412 on stale revision); 36-hour idempotency cache hit test; rolling 15-version queue test verifying approved versions are protected.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_postmortem_storage.py
```
Output: Autosave updates revision and ETag; 412 returned on stale write; version retention respects approvals.
ACCEPTANCE CRITERIA:
- [ ] Autosave updates working draft without creating unnecessary versions.
- [ ] Failed `If-Match` returns 412 with `stale_version` error code.
- [ ] Approved versions are never pruned by rolling queue.
STOP AND ASK IF: Praveen has answered R-07 on version archive table vs flag.
HANDOFF OUTPUT: Postmortem storage unblocks Frontend editor core (AG-14).
COMMIT AND PR: `feat(core): implement postmortem storage autosave and version queue`
PROGRESS ENTRY: `CX-13 | Merged | Postmortem working draft, autosave ETag, version retention | contracts/core/openapi.json | Open`

---

### PHASE: CX-14 Review Lifecycle, Comments, and Approvals
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement postmortem review state machine (`submit`, `approve`, `request-changes`, `publish`, `reopen`), comment threads, author-cannot-approve guard, and user email lookup for notifications (R-10).
OWNER AGENT: Codex
BRANCH: cx/14-review-lifecycle-approvals
DEPENDS ON: CX-13
READ FIRST: PRD 8.9 REV-2..REV-7; System Design section 14, 21; API Contracts section 4.1, 10.1; Database Design section 5 (`comment_threads`, `comments`, `approvals`).
ALLOWED PATHS:
- `services/core/apps/postmortems/**`
- `contracts/core/openapi.json`
- `contracts/events/core/postmortem.submitted.json`
- `contracts/events/core/postmortem.approved.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/core/openapi.json`, `contracts/events/core/postmortem.submitted.json`, `contracts/events/core/postmortem.approved.json`
TASKS:
1. Implement `comment_threads` and `comments` models and CRUD API.
2. Implement state machine actions:
   - `POST /postmortems/{id}/submit`: guards require blameless check on latest version. Emits `postmortem.submitted`.
   - `POST /postmortems/{id}/request-changes`: requires Admin role and non-empty note.
   - `POST /postmortems/{id}/approve`: requires Admin role, reviewed version must be latest, author cannot approve own postmortem (REV-6). Emits `postmortem.approved`.
   - `POST /postmortems/{id}/publish`: requires prior approval. Sets `is_locked=true`.
   - `POST /postmortems/{id}/reopen`: takes snapshot, returns to `in_review`, unlocks document.
3. Implement internal endpoint for user email lookup by user IDs for Notifications service (R-10).
NON-GOALS: Do not implement automated reviewer assignment in v1 (P1).
TESTS REQUIRED: State machine transition guard tests; author-cannot-approve rejection test; lock enforcement on approved postmortem; comment thread anchor preservation tests.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_review_lifecycle.py
```
Output: All state transitions adhere to guards; author approval is blocked; lock prevents edits.
ACCEPTANCE CRITERIA:
- [ ] Author cannot approve their own postmortem (enforced in service and DB trigger).
- [ ] Approved and published documents are strictly read-only until reopened.
- [ ] `postmortem.submitted` and `postmortem.approved` events emitted via outbox.
STOP AND ASK IF: Manager role is enabled (v1 confirmed Admin and Member only).
HANDOFF OUTPUT: Review workflow endpoints ready for Antigravity AG-18.
COMMIT AND PR: `feat(core): implement postmortem review lifecycle comments and approvals`
PROGRESS ENTRY: `CX-14 | Merged | Review state machine, approvals, author guard, comments API | contracts/core/openapi.json | Open`

---

### PHASE: CX-15 Action Items Management and Stalled Logic
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement action items CRUD, confirmation flow, verification requirements, stalled status calculation, and internal stalled items query API.
OWNER AGENT: Codex
BRANCH: cx/15-action-items-stalled
DEPENDS ON: CX-14
READ FIRST: PRD 8.11 ACT-1..ACT-6; System Design sections 14, 20.5; API Contracts section 4.1; Database Design section 5 (`action_items`, `action_item_events`).
ALLOWED PATHS:
- `services/core/apps/actions/**`
- `contracts/core/openapi.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/core/openapi.json`
TASKS:
1. Implement `action_items` and `action_item_events` models.
2. Implement `GET /api/v1/orgs/{org_id}/action-items` with page pagination and filters (`status`, `priority`, `owner_user_id`, `stalled`).
3. Implement `POST /api/v1/orgs/{org_id}/action-items` creating manual or confirming AI-suggested action items.
4. Implement `PATCH /api/v1/orgs/{org_id}/action-items/{id}` with state transitions (`open`, `in_progress`, `blocked`, `done`, `dropped`).
5. Implement `POST /api/v1/orgs/{org_id}/action-items/{id}/verify` recording verification note/URL.
6. Implement stalled status calculation logic: overdue or no update within `stall_days` (default 7 days).
7. Implement internal API endpoint `GET /api/v1/internal/action-items/stalled` consumed by Notifications scan job (System Design 20.5).
NON-GOALS: Do not build GitHub issue sync in v1 (P1).
TESTS REQUIRED: Stalled calculation tests across timezone boundaries; confirmation guard tests; state history recording tests.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_action_items_api.py
```
Output: Action items CRUD, verification, and stalled calculations pass all tests.
ACCEPTANCE CRITERIA:
- [ ] AI-suggested items cannot be tracked until confirmed with owner and due date.
- [ ] Dropped items require explicit reason.
- [ ] Internal stalled endpoint returns correct stalled items per tenant settings.
STOP AND ASK IF: Action item priority values need modification (`low`, `medium`, `high`, `critical` confirmed).
HANDOFF OUTPUT: Action items API unblocks Frontend action board (AG-20) and Notifications reminders (CU-15).
COMMIT AND PR: `feat(core): implement action items lifecycle and stalled items calculation`
PROGRESS ENTRY: `CX-15 | Merged | Action items CRUD, confirmation, stalled calculation, internal API | contracts/core/openapi.json | Open`

---

### PHASE: CX-16 Exports Engine and Public Jobs Endpoint
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement PDF and Markdown export rendering with preserved citations, Azure Blob Storage upload with signed download links, and public `GET /jobs/{job_id}` endpoint (R-01).
OWNER AGENT: Codex
BRANCH: cx/16-exports-jobs-endpoint
DEPENDS ON: CX-15
READ FIRST: PRD 8.10 EXP-1, EXP-2; System Design section 14, 218; API Contracts sections 3.1, 4.1, 8.1; Database Design section 5 (`exports`).
ALLOWED PATHS:
- `services/core/apps/exports/**`
- `services/core/apps/jobs/**`
- `contracts/core/openapi.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/core/openapi.json`
TASKS:
1. Implement `render_export` Celery background task generating Markdown and PDF (using WeasyPrint or ReportLab) preserving citation chips linked to timeline events.
2. Store rendered files in Azure Blob Storage (with local filesystem fake for dev) with short-lived expiration.
3. Implement `POST /api/v1/orgs/{org_id}/postmortems/{id}/export` returning 202 Accepted and job ID.
4. Implement `GET /api/v1/orgs/{org_id}/exports/{id}/download` generating short-lived signed download URL.
5. Implement public `GET /api/v1/orgs/{org_id}/jobs/{job_id}` reporting job status, progress percentage, and safe error message across Core and external services via ADR-0001 (R-01).
NON-GOALS: Do not build audit-ready composite PDF in v1 (Later item).
TESTS REQUIRED: Markdown export citation format test; PDF rendering test; signed URL expiry test; public job polling test.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_exports_jobs.py
```
Output: PDF and Markdown generated cleanly with citations; job status endpoint returns accurate progress.
ACCEPTANCE CRITERIA:
- [ ] Export contains timeline events with complete source references.
- [ ] Signed download URL expires after configured lifetime.
- [ ] Public job endpoint safely reports job states without disclosing cross-tenant data.
STOP AND ASK IF: PDF rendering engine choice requires system package dependencies in container.
HANDOFF OUTPUT: Export and job polling ready for Frontend M17 (AG-19) and M21 (AG-11).
COMMIT AND PR: `feat(core): implement postmortem exports and public jobs endpoint`
PROGRESS ENTRY: `CX-16 | Merged | PDF/Markdown export rendering, blob storage, public job status | contracts/core/openapi.json | Open`

---

### PHASE: CX-17 Recovery-Time and Incident Volume Analytics
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement `refresh_analytics_summaries` precomputation job and the three public analytics endpoints (`recovery-times`, `incident-volume`, `action-health`).
OWNER AGENT: Codex
BRANCH: cx/17-analytics-engine
DEPENDS ON: CX-16
READ FIRST: PRD 8.12 ANL-1, ANL-2, ANL-5; System Design section 14; Database Design section 5 (`analytics_summaries`).
ALLOWED PATHS:
- `services/core/apps/analytics/**`
- `contracts/core/openapi.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/core/openapi.json`
TASKS:
1. Implement `analytics_summaries` model and unique composite constraints.
2. Implement `refresh_analytics_summaries` job computing MTTA, MTTD, MTTM, MTTR, incident volume, and action item health by week/month and severity/service.
3. Implement `GET /api/v1/orgs/{org_id}/analytics/recovery-times` returning duration metrics and trends.
4. Implement `GET /api/v1/orgs/{org_id}/analytics/incident-volume` returning counts grouped by service, severity, type, and period.
5. Implement `GET /api/v1/orgs/{org_id}/analytics/action-health` returning completion rates, average close times, and stalled counts.
NON-GOALS: Do not build repeat-incident detection in v1 (Later item).
TESTS REQUIRED: Analytics calculation unit tests against fixed test incidents; empty period handling tests; two-tenant isolation tests.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_analytics.py
```
Output: Precomputed summaries match raw calculations; analytics endpoints return correct schema.
ACCEPTANCE CRITERIA:
- [ ] Computes detect, acknowledge, mitigate, and resolve averages accurately.
- [ ] Action health reflects stalled action items per organization settings.
- [ ] Endpoints respond within 2 seconds for typical data size.
STOP AND ASK IF: Missing incident timestamp data handling policy requires adjustment.
HANDOFF OUTPUT: Analytics APIs published (Gate G5 readiness for Codex). Unblocks Frontend analytics (AG-21).
COMMIT AND PR: `feat(core): implement analytics precomputation and reporting endpoints`
PROGRESS ENTRY: `CX-17 | Merged | Analytics summaries job, recovery times, volume, action health | contracts/core/openapi.json | Open`

---

### PHASE: CX-18 AI Service Skeleton, Model Settings, and Adapter
EFFORT: L (Est. review time: 35 mins)
GOAL: Scaffold `services/ai` with Django Ninja, implement `ai` schema models, provider-agnostic model adapter with fake scripted provider, model settings API, and connection test.
OWNER AGENT: Codex
BRANCH: cx/18-ai-skeleton-adapter
DEPENDS ON: CX-10 (Gate G2)
READ FIRST: PRD 8.7 AI-3, section 10; System Design section 16; AI Pipeline Spec sections 14, 19.2; Database Design section 7 (`model_settings`, `usage_counters`).
ALLOWED PATHS:
- `services/ai/**`
- `contracts/ai/openapi.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ai/openapi.json`
TASKS:
1. Scaffold `services/ai` using Django 5, Django Ninja async routers, and Pydantic v2.
2. Implement `ai` schema models: `model_settings`, `usage_counters`, `draft_runs`, `draft_section_runs`, `blameless_findings`, `inline_edit_events`, and common tables.
3. Implement `LLMProvider` protocol and `FakeScriptedProvider` capable of returning scripted valid and invalid structured responses.
4. Implement Azure OpenAI and OpenAI provider implementations behind adapter.
5. Implement `GET` and `PUT /api/v1/orgs/{org_id}/ai-model` managing model settings (storing API keys encrypted via tenant data key, returning masked hint).
6. Implement `POST /api/v1/orgs/{org_id}/ai-model/test` executing test call through adapter.
7. Implement daily usage counter tracking and limit enforcement for default model.
NON-GOALS: Do not depend on a real live LLM endpoint for test execution (always test with fake scripted provider).
TESTS REQUIRED: Adapter protocol conformance tests; encryption of model API keys; daily usage limit enforcement; fake provider test calls.
VERIFICATION:
```bash
uv run python services/ai/manage.py makemigrations --check
uv run pytest services/ai/tests/test_adapter.py
```
Output: AI models migrated; adapter tests pass; keys encrypted at rest.
ACCEPTANCE CRITERIA:
- [ ] Adapter interface supports structured output generation and timeouts.
- [ ] Stored API keys are encrypted at rest with tenant data key; API returns only masked hint.
- [ ] Usage counters enforce default model daily quota.
STOP AND ASK IF: Praveen has benchmarked candidate Azure default models (R-20).
HANDOFF OUTPUT: AI service ready for pipeline stage implementation.
COMMIT AND PR: `feat(ai): scaffold ai service model adapter and settings api`
PROGRESS ENTRY: `CX-18 | Merged | AI service scaffold, Ninja routers, LLM adapter, model settings | contracts/ai/openapi.json | Open`

---

### PHASE: CX-19 AI Pipeline Stages S0 to S3 (Preparation and Screening)
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement Pipeline stages S0 (Resolve and Authorize), S1 (Evidence Prepare), S2 (Prompt Injection Screen), and S3 (Observation Map) with versioned prompts and fake provider.
OWNER AGENT: Codex
BRANCH: cx/19-ai-pipeline-s0-s3
DEPENDS ON: CX-18, CU-12 (Gate G3)
READ FIRST: AI Pipeline Spec sections 4, 5, 9.1, 9.2, 11, stages table S0..S3.
ALLOWED PATHS:
- `services/ai/pipeline/**`
- `services/ai/prompts/**`
- `contracts/ai/**`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ai/schemas/observation_map.json`
TASKS:
1. Store global system prompt (9.1) and observation extraction prompt (9.2) in versioned files (`services/ai/prompts/v1/`).
2. Implement S0: validate tenant/incident authorization, model configuration, and fetch evidence snapshot reference.
3. Implement S1: fetch authorized timeline events from Ingestion internal API, validate stable event IDs, format redacted evidence packet, and record limitations.
4. Implement S2: screening pass for instruction-like injection patterns; tag risk annotations while treating all evidence as untrusted data.
5. Implement S3: invoke LLM adapter with observation prompt, parse response into `observation-map.v1` Pydantic model, ensuring all observations link to valid event IDs.
6. Implement stage input hashing and immutable stage artifact storage in `draft_run_stages` (R-09).
NON-GOALS: Do not combine observations into causal stories or draft sections yet.
TESTS REQUIRED: Unit tests for S0 scope rejection; S1 evidence packet formatting; S2 injection screening detection; S3 observation parsing with fake provider; stage caching hash test.
VERIFICATION:
```bash
uv run pytest services/ai/tests/test_pipeline_s0_s3.py
```
Output: Stages S0 through S3 execute sequentially; observations map to event IDs; injection patterns flagged.
ACCEPTANCE CRITERIA:
- [ ] Evidence content is treated strictly as untrusted data in prompts.
- [ ] Observation map records stable event IDs for every observation.
- [ ] Stage input hash detects any change to evidence or prompts.
STOP AND ASK IF: Prompt template variables require additional metadata fields.
HANDOFF OUTPUT: S0-S3 stage pipeline ready for claim generation.
COMMIT AND PR: `feat(ai): implement ai pipeline stages s0 through s3`
PROGRESS ENTRY: `CX-19 | Merged | Pipeline stages S0-S3, evidence packet, injection screen, observation map | None | Open`

---

### PHASE: CX-20 AI Pipeline Stages S4 to S6 (Claim Planning and Validation)
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement S4 (Claim Planning), S5 (Claim Generation), and S6 (Deterministic Validation) enforcing claim kinds, event existence, citation relevance, and timestamp accuracy.
OWNER AGENT: Codex
BRANCH: cx/20-ai-pipeline-s4-s6
DEPENDS ON: CX-19
READ FIRST: AI Pipeline Spec sections 6, 7, 8.1, 9.3, 9.4, stages table S4..S6.
ALLOWED PATHS:
- `services/ai/pipeline/**`
- `services/ai/prompts/**`
- `contracts/ai/**`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ai/schemas/claims.json`
TASKS:
1. Store claim planning prompt (9.3) and claim generation prompt (9.4) in versioned prompt files.
2. Implement S4: generate claim plan mapping required sections to evidence availability, identifying gaps and questions.
3. Implement S5: generate atomic candidate claims enforcing taxonomy (`observed_fact`, `causal_claim`, `hypothesis`, `open_question`, `author_context`, `process_recommendation`).
4. Implement S6 Deterministic Validator:
   - Validate Pydantic schema structure.
   - Verify all cited event IDs exist in the active evidence snapshot.
   - Verify every `observed_fact` and `causal_claim` has at least one valid citation.
   - Check that event timestamps in prose match source event timestamps.
   - Verify root cause is not marked as confirmed by the model.
   - Verify action items are suggestions without fabricated assignments.
NON-GOALS: Do not run semantic LLM verifier yet (handled in CX-21).
TESTS REQUIRED: Deterministic validation test matrix: missing citation rejection, unknown event ID rejection, timestamp mismatch rejection, root-cause auto-confirmation rejection.
VERIFICATION:
```bash
uv run pytest services/ai/tests/test_deterministic_validator.py
```
Output: Deterministic validator catches all schema, provenance, and citation defects.
ACCEPTANCE CRITERIA:
- [ ] Factual claims without citations fail validation unconditionally.
- [ ] Citations referencing non-existent event IDs are rejected.
- [ ] Root cause confirmation is blocked from model output.
STOP AND ASK IF: Claim kind taxonomy requires additional domain-specific kinds.
HANDOFF OUTPUT: Validated claims ready for repair and semantic verification.
COMMIT AND PR: `feat(ai): implement ai pipeline stages s4 through s6 and deterministic validator`
PROGRESS ENTRY: `CX-20 | Merged | Claim planning, claim generation, deterministic validation suite | contracts/ai/schemas/claims.json | Open`

---

### PHASE: CX-21 AI Pipeline Stages S7 to S9 (Repair, Verifier, Policy)
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement S7 (Bounded Repair), S8 (Read-Only Semantic Verifier), S9 (Policy Application), and graceful degradation when verifier is unavailable.
OWNER AGENT: Codex
BRANCH: cx/21-ai-pipeline-s7-s9
DEPENDS ON: CX-20
READ FIRST: AI Pipeline Spec sections 8.2, 8.3, 9.5, 9.7, 13, stages table S7..S9.
ALLOWED PATHS:
- `services/ai/pipeline/**`
- `services/ai/prompts/**`
- `contracts/ai/**`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ai/schemas/verifier_report.json`
TASKS:
1. Store causal analysis prompt (9.5) and read-only semantic verifier prompt (9.7) in versioned files.
2. Implement S7: single bounded repair attempt passing exact validation errors back to model for structural defects.
3. Implement S8: read-only semantic verifier inspecting high-risk and causal claims; verifier output produces findings only and cannot edit content.
4. Implement S9 Policy Application: deterministic mapping of findings to claim disposition:
   - Valid supported fact -> accept.
   - Unsupported causal claim -> downgrade to hypothesis.
   - Unknown fact -> convert to targeted open question.
   - Misleading claim -> omit.
5. Implement graceful degradation: if verifier times out or fails, proceed only if deterministic checks passed, marking `verification_status="unavailable"` plainly.
NON-GOALS: Never allow semantic verifier to rewrite text or modify draft content.
TESTS REQUIRED: Bounded repair single-attempt test; read-only verifier immutability test; verifier timeout graceful degradation test; claim disposition policy tests.
VERIFICATION:
```bash
uv run pytest services/ai/tests/test_verifier_and_policy.py
```
Output: Repair executes exactly once; verifier outputs findings only; graceful degradation activates on timeout.
ACCEPTANCE CRITERIA:
- [ ] Verifier has no code path to edit draft text or citations.
- [ ] When verifier is unavailable, status is visibly marked "unavailable", never "passed".
- [ ] Unsupported claims are downgraded or converted to questions per policy.
STOP AND ASK IF: Candidate verifier model identity requires configuration (R-20).
HANDOFF OUTPUT: Verified and policy-processed claims ready for assembly.
COMMIT AND PR: `feat(ai): implement bounded repair semantic verifier and policy application`
PROGRESS ENTRY: `CX-21 | Merged | Bounded repair, read-only verifier, claim policy, degradation handling | contracts/ai/schemas/verifier_report.json | Open`

---

### PHASE: CX-22 AI Pipeline Stages S10 to S13 and Core Draft Integration
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement S10 (Section Assembly), S11 (Final Validation), S12 (Blameless Review), S13 (Persist and Return to Core), draft background job, and clarification question generation (Gate G4).
OWNER AGENT: Codex
BRANCH: cx/22-pipeline-assembly-persistence
DEPENDS ON: CX-21, CX-13
READ FIRST: AI Pipeline Spec sections 6.3, 9.6, 10, stages table S10..S13; API Contracts sections 6.4, 7.4; System Design section 9.4.
ALLOWED PATHS:
- `services/ai/pipeline/**`
- `services/ai/tasks/**`
- `services/ai/prompts/**`
- `contracts/events/ai/draft.ready.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/events/ai/draft.ready.json`
TASKS:
1. Store section assembly prompt (9.6) in versioned files.
2. Implement S10: assemble required 11 postmortem sections using only accepted claims; map every sentence to claim IDs.
3. Implement S11: final validation verifying no uncatalogued factual claims were introduced during assembly.
4. Implement S12: invoke blameless review scan on assembled draft.
5. Implement S13: persist stage artifacts, call Core internal API to store new postmortem version with model metadata and prompt version, and publish `draft.ready` event.
6. Implement `generate_draft` Celery background task with progress reporting.
7. Implement clarification question output structure when critical ambiguity pauses a stage (R-15, NEEDS PRAVEEN).
NON-GOALS: Never overwrite an existing human-edited version; always append as a new draft version.
TESTS REQUIRED: End-to-end pipeline test from authorized snapshot to Core version persistence; sentence-to-claim mapping verification; `draft.ready` event publishing test.
VERIFICATION:
```bash
uv run pytest services/ai/tests/test_full_draft_pipeline.py
```
Output: Pipeline runs S0 through S13 end-to-end; Core creates version snapshot; event emitted.
ACCEPTANCE CRITERIA:
- [ ] Assembled postmortem contains all 11 required sections.
- [ ] Every factual claim preserves its citation chips.
- [ ] Persisted to Core as new version; human edits preserved.
STOP AND ASK IF: Clarification question endpoint design needs Praveen decision (R-15).
HANDOFF OUTPUT: Draft generation loop complete (Gate G4). Unblocks Frontend generation and editor (AG-13, AG-14).
COMMIT AND PR: `feat(ai): implement section assembly final validation and draft persistence`
PROGRESS ENTRY: `CX-22 | Merged | S10-S13 section assembly, draft background task, Core persistence | contracts/events/ai/draft.ready.json | Open`

---

### PHASE: CX-23 Blameless Language Checker
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement rule-based blameless checker, optional targeted LLM rewrite pass, findings persistence in `blameless_findings`, and public blameless API endpoints.
OWNER AGENT: Codex
BRANCH: cx/23-blameless-checker
DEPENDS ON: CX-22
READ FIRST: PRD 8.8 BL-1..BL-4; System Design section 20.4; AI Pipeline Spec sections 9.8, 12; Database Design section 7 (`blameless_findings`).
ALLOWED PATHS:
- `services/ai/apps/blameless/**`
- `services/ai/prompts/**`
- `contracts/ai/openapi.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ai/openapi.json`
TASKS:
1. Store blameless review prompt (9.8) in versioned files.
2. Implement rule-based pattern scanner for attribution, personal judgment, counterfactual blame ("should have"), and absolute language ("always/never").
3. Ensure rule-based pass executes completely without any LLM requirement.
4. Implement targeted rewrite pass requesting LLM rewrite for flagged sentences only, keeping all factual statements.
5. Implement `POST /api/v1/orgs/{org_id}/postmortems/{id}/blameless-check` executing scan on current document revision.
6. Implement `GET /api/v1/orgs/{org_id}/postmortems/{id}/blameless-suggestions` listing open findings.
7. Implement `PATCH /api/v1/orgs/{org_id}/blameless-suggestions/{id}` accepting, editing, or dismissing finding.
NON-GOALS: Blameless check never automatically rewrites text without author approval.
TESTS REQUIRED: Unit tests for rule regex patterns; LLM-unavailable fallback test; API tests for accept/edit/dismiss status updates.
VERIFICATION:
```bash
uv run pytest services/ai/tests/test_blameless.py
```
Output: Rule scanner detects blame phrases; LLM failure preserves rule findings; API updates statuses.
ACCEPTANCE CRITERIA:
- [ ] Rule scanner works 100% offline without LLM availability.
- [ ] Author must explicitly accept or dismiss each finding.
- [ ] Core submit guard checks that blameless check has run on latest revision.
STOP AND ASK IF: Additional organization-specific blame keywords are requested.
HANDOFF OUTPUT: Blameless API unblocks Frontend blameless panel (AG-17).
COMMIT AND PR: `feat(ai): implement rule-based blameless checker and rewrite suggestions`
PROGRESS ENTRY: `CX-23 | Merged | Blameless rule scanner, rewrite generator, suggestions API | contracts/ai/openapi.json | Open`

---

### PHASE: CX-24 Inline AI Suggestions and Section Regeneration
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement Server-Sent Events (SSE) streaming endpoint `POST /postmortems/{id}/ai/edit` for inline text actions and `POST /postmortems/{id}/sections/{key}/regenerate` creating suggested revisions.
OWNER AGENT: Codex
BRANCH: cx/24-inline-ai-streaming
DEPENDS ON: CX-23
READ FIRST: PRD 8.9a ED-2, ED-3; System Design sections 10, 16; API Contracts sections 3.1, 4.3, 6.5 (R-14); Database Design section 7 (`inline_edit_events`).
ALLOWED PATHS:
- `services/ai/apps/inline/**`
- `contracts/ai/openapi.json`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ai/openapi.json`
TASKS:
1. Implement Django Ninja async SSE endpoint `POST /api/v1/orgs/{org_id}/postmortems/{id}/ai/edit` taking selection, surrounding context, and action (`blameless`, `clearer`, `shorter`, `expand_with_evidence`, `custom`).
2. Stream SSE named events: `progress`, `result`, `error`, `complete` with correlation ID.
3. Record action metadata in append-only `inline_edit_events` (selection length, tokens, outcome).
4. Implement `POST /api/v1/orgs/{org_id}/postmortems/{id}/sections/{key}/regenerate` executing section pipeline and returning new version as suggestion in Core without overwriting manual text.
5. Enforce citation rules on inline suggestions adding new factual claims.
NON-GOALS: Streamed edits are not saved to the document until explicitly accepted by author.
TESTS REQUIRED: SSE stream connection and chunk delivery test; error event delivery test; section regenerate suggestion test.
VERIFICATION:
```bash
uv run pytest services/ai/tests/test_inline_ai_streaming.py
```
Output: SSE stream emits valid event stream; section regenerate creates non-destructive suggestion.
ACCEPTANCE CRITERIA:
- [ ] SSE endpoint emits `text/event-stream` with standard event names.
- [ ] Suggestions are never saved to document automatically.
- [ ] Inline facts cite timeline events.
STOP AND ASK IF: SSE reconnect policy parameters require adjustment (R-14).
HANDOFF OUTPUT: Inline AI and section regeneration unblocks Frontend editor AI (AG-16).
COMMIT AND PR: `feat(ai): implement inline ai sse streaming and section regeneration`
PROGRESS ENTRY: `CX-24 | Merged | Inline AI SSE streaming, section regenerate, suggestion diff | contracts/ai/openapi.json | Open`

---

### PHASE: CX-25 Isolation and Contract Hardening
EFFORT: L (Est. review time: 40 mins)
GOAL: Execute comprehensive security, two-tenant isolation, contract schema verification, and concurrency test suites across Core and AI services (Gate G6/G7 readiness).
OWNER AGENT: Codex
BRANCH: cx/25-isolation-contract-hardening
DEPENDS ON: CX-17, CX-24
READ FIRST: PRD section 11; Master Build Guide section 9.1; API Contracts section 11.3; Database Design section 3.2.
ALLOWED PATHS:
- `services/core/tests/**`
- `services/ai/tests/**`
- `contracts/**`
- `docs/progress/codex.md`
FORBIDDEN PATHS: `services/ingestion/`, `services/notifications/`, `gateway/`, `web/`
CONTRACTS TOUCHED: Contract validation updates.
TASKS:
1. Write exhaustive two-tenant cross-boundary test suite:
   - Route tests: tenant A token accessing tenant B resources returns 404.
   - Cache tests: tenant B cache keys cannot be read by tenant A.
   - Job tests: Celery tasks running with tenant A context cannot query tenant B database.
   - Event tests: tenant A event consumers ignore tenant B payloads.
   - Database role tests: direct connection with `core_{org_a}` cannot select `tenant_{org_b}`.
2. Run full OpenAPI contract validation comparing drf-spectacular and Ninja outputs to `contracts/`.
3. Verify 36-hour idempotency key replay behavior with identical and mismatched payloads.
4. Verify ETag optimistic concurrency behavior under concurrent saves.
NON-GOALS: Do not weaken any security check to make a test pass.
TESTS REQUIRED: Two-tenant isolation suite; contract diff suite; concurrent ETag collision suite; audit chain integrity suite.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_tenant_isolation.py
uv run pytest services/ai/tests/test_tenant_isolation.py
uv run python scripts/validate_contracts.py
```
Output: Zero cross-tenant data leaks; all contract schemas match 100%; concurrency guards hold.
ACCEPTANCE CRITERIA:
- [ ] Zero cross-tenant data disclosures across all routes and jobs.
- [ ] Direct database role privileges strictly enforced.
- [ ] Contract diff produces zero unapproved drift.
STOP AND ASK IF: Any test reveals potential cross-tenant leak.
HANDOFF OUTPUT: Backend foundation and brains hardened for Gate G6/G7.
COMMIT AND PR: `test(security): execute two-tenant isolation and contract hardening suite`
PROGRESS ENTRY: `CX-25 | Merged | Cross-tenant isolation verification, contract tests, security audit | None | Open`

---

### PHASE: CX-26 AI Evaluation Package and Benchmark Harness
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement versioned benchmark evaluation harness using labeled test incidents to measure claim citation coverage, causal accuracy, and token latency across models (feeds R-20).
OWNER AGENT: Codex
BRANCH: cx/26-ai-evaluation-package
DEPENDS ON: CX-25
READ FIRST: PRD sections 14, 17; AI Pipeline Spec section 15; Master Build Guide section 10 (R-20).
ALLOWED PATHS:
- `services/ai/evaluation/**`
- `docs/progress/codex.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: none
TASKS:
1. Create versioned evaluation dataset in `services/ai/evaluation/data/` with at least two labeled incidents containing known key moments, ground-truth root causes, and conflicting evidence.
2. Implement evaluation benchmark runner testing:
   - Claim citation coverage (target >= 90% per PRD).
   - Contradiction preservation rate.
   - Hallucinated timestamp rate (target 0%).
   - Prompt injection resistance on adversarial test cases.
3. Measure per-stage latency, token counts, and estimated cost across candidate models.
4. Record evaluation report output to feed Praveen decision on default model and quotas (R-20).
NON-GOALS: Do not hard-code production Azure model selection before benchmark review.
TESTS REQUIRED: Benchmark execution test verifying evaluation runner calculates metrics cleanly.
VERIFICATION:
```bash
uv run python services/ai/evaluation/run_benchmark.py --provider=fake
```
Output: Benchmark runner calculates precision, recall, citation coverage, and latency metrics.
ACCEPTANCE CRITERIA:
- [ ] Benchmark tests all 11 required evaluation metrics.
- [ ] Adversarial prompt injection cases are tested.
- [ ] Benchmark report generated for Praveen review.
STOP AND ASK IF: Praveen wants specific candidate models included in benchmark run.
HANDOFF OUTPUT: Benchmark results available for default Azure model selection (R-20).
COMMIT AND PR: `feat(ai): implement model evaluation package and benchmark harness`
PROGRESS ENTRY: `CX-26 | Merged | Evaluation harness, labeled incidents benchmark, metrics runner | None | Open`

---

### PHASE: CX-27 Documentation Update and Final Alignment
EFFORT: S (Est. review time: 20 mins)
GOAL: Update system architecture documentation, database design references, and progress records reflecting settled ADRs and version labels (R-23).
OWNER AGENT: Codex
BRANCH: cx/27-docs-final-alignment
DEPENDS ON: CX-26
READ FIRST: Master Build Guide section 10 (R-23); Repository Conventions section 15; API Contracts section 1.3.
ALLOWED PATHS:
- `docs/**`
- `README.md`
- `services/core/README.md`
- `services/ai/README.md`
- `docs/progress/codex.md`
FORBIDDEN PATHS: Application code, contracts, infra, gateway, web.
CONTRACTS TOUCHED: none
TASKS:
1. Update System Design references to v0.4 in documentation (R-23).
2. Document service READMEs for Core and AI detailing setup commands, local environment variables, health endpoints, and migration ownership.
3. Reconcile Database Design table counts and new columns from ADRs in architecture documentation.
4. Finalize `docs/progress/codex.md` with complete phase log.
NON-GOALS: Do not edit Cursor or Antigravity progress files.
TESTS REQUIRED: Markdown linting checks and documentation link verification.
VERIFICATION:
```bash
uv run python -m doctest README.md
```
Output: Documentation links and examples verified.
ACCEPTANCE CRITERIA:
- [ ] System Design version label updated to v0.4 in doc references.
- [ ] Service READMEs complete with local runbooks.
- [ ] All Codex phases in `docs/progress/codex.md` marked complete.
STOP AND ASK IF: Any architectural documentation conflict remains unresolved.
HANDOFF OUTPUT: Codex implementation complete for final release candidate (Gate G7).
COMMIT AND PR: `docs(core,ai): update architecture documentation and service runbooks`
PROGRESS ENTRY: `CX-27 | Merged | Final documentation alignment, service READMEs, progress sign-off | None | Done`
