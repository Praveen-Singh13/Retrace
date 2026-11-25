# Implementation Plan: Cursor (Backend Integrations, Notifications, and Platform)

## Agent Role and Scope

Cursor owns backend integrations, notifications, API gateway, local Docker Compose environment, CI/CD pipelines, migration runner, Azure infrastructure, and system observability for Retrace.

Owner: Cursor
Services owned:
- `services/ingestion/` (Integration connections, encrypted secrets, allowlists, service catalog, discovery job, evidence normalization with five timestamp fields, timeline builder, PagerDuty webhooks, internal evidence API)
- `services/notifications/` (In-app notifications, preferences, reminders daily scan job, email delivery adapter, templates, delivery logs, event consumers)
Platform and infrastructure owned:
- `gateway/` (Traefik routing, TLS termination, JWT validation, CORS, rate limiting, request IDs)
- `infra/` (Docker Compose assets, migration runner container, Azure infrastructure IaC, PgBouncer, backup scripts)
- `.github/workflows/` (Path-aware GitHub Actions pipelines, quality gates, image builds, deployments)
- `compose.yaml`, `compose.override.yaml.example`
- Contract directories: `contracts/ingestion/`, `contracts/notifications/`, `contracts/events/ingestion/`, `contracts/events/notifications/`
- Progress tracking: `docs/progress/cursor.md`

---

## Anti-Hallucination Rules

These rules are strictly binding on Cursor throughout execution:

1. Documents win over memory. If an endpoint, field, column, event, provider parameter, or infrastructure value is not in the source documents or repo, Cursor does not invent it. It records an open question and asks Praveen.
2. Search before creating. Before adding any route, table, event, schema, helper, or infrastructure resource, search the repository and `contracts/` for an existing definition.
3. Cite sources in the PR. The PR description lists the exact document sections and requirement IDs implemented.
4. Read installed versions and official docs. Check Slack, PagerDuty, and GitHub APIs against current official documentation before implementing connectors. Use lockfile-pinned library versions.
5. No fabricated results. Only report tests or commands as passing if actually run in the session with verified real output. If a test cannot run, say so explicitly.
6. Unresolved items stay unresolved. Open items in API Contracts section 13 and Guide section 10 are resolved only through explicit ADRs and Praveen decisions. Never silently invent an infrastructure provider or configuration default.
7. Fixtures over imagination. External provider interactions use recorded fixtures and mock servers in automated tests. Live calls happen only in marked manual verification steps with Praveen's test accounts.
8. Small steps, full stops. After each phase, stop, summarize, and wait for Praveen to review and merge before continuing.
9. No scope creep. P2 and Later items (such as full GitHub bidirectional sync, repeat-incident detection, audit-ready PDF reports) are out of scope for v1.
10. No secrets. Never write real secrets, provider tokens, private keys, or personal data into code, fixtures, logs, commit messages, or PR text.
11. Ask in a structured way. Questions use the format: QUESTION, WHY IT BLOCKS, OPTIONS, DEFAULT I WOULD USE.
12. Do not weaken security to make tests pass. Tenant isolation, service database role separation, and signature verifications are never bypassed.

---

## Git and GitHub Protocol

1. Author identity: Every commit is authored and committed as Praveen. Before the first commit, verify `git config user.name` and `git config user.email`. If not set to Praveen's verified identity, stop and ask. Praveen's GitHub username is `Praveen-Singh13`.
2. Attribution removal: Remove all agent attribution: no `Co-authored-by` trailers, no "Generated with" lines, and no agent signatures in commit messages or PR text. Verify with `git log -1 --format='%an <%ae>%n%cn <%ce>%n%b'`.
3. Branching: Work exclusively on feature branches named `cu/<NN>-<slug>` (for example `cu/02-gateway`). Never commit directly to `main`.
4. Commits: Use Conventional Commits (`type(scope): imperative summary`). Scopes for Cursor: `ingestion`, `notifications`, `gateway`, `infra`, `ci`, `contracts`, `docs`.
5. Pull requests: Rebase on latest `main` before opening PR. PR body includes problem summary, requirement IDs, affected services/contracts, test evidence, rollback notes, and linked ADRs.

---

## Cross-Agent Handoff Protocol

1. Contracts first: Cursor merges OpenAPI fragments and event schemas into `contracts/ingestion/` and `contracts/notifications/` with example fixtures before writing full implementations.
2. Handoff requests: When requesting changes in paths owned by Codex (`services/core/`, `services/ai/`, `libs/`) or Antigravity (`web/`), Cursor writes `docs/handoffs/cursor-to-<target>-<NN>.md` and stops.
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

## Reconciliation Backlog Assignments for Cursor

| Item | Topic | Phase / Output | Status |
| --- | --- | --- | --- |
| R-04 | Five evidence timestamp fields vs single occurred_at | CU-08 | Migration in ingestion schema |
| R-06 | Evidence snapshot resource, hash, stale/cancel statuses | CU-10 | Joint design with Codex |
| R-11 | Gateway routing for shared /postmortems/{id}/... paths | CU-02 | Traefik path priority matching |
| R-12 | Webhook public path /api/v1/webhooks/pagerduty/{token} | CU-02, CU-05 | Gateway routing rule |
| R-19 | Page sizes, rate limits, timeouts config | CU-03, CU-14 | Provisional configuration module |
| R-21 | IaC tool, email provider, custom domain, Kaggle dataset, PgBouncer | CU-00, CU-16, CU-21, CU-23, CU-24 | NEEDS PRAVEEN (ADRs) |

---

## Cursor Implementation Phases (CU-00 to CU-26)

### PHASE: CU-00 Docker Compose Baseline Environment
EFFORT: M (Est. review time: 25 mins)
GOAL: Establish the local multi-container development environment in `compose.yaml` with PostgreSQL, Redis, local blob storage substitute, and Key Vault substitute.
OWNER AGENT: Cursor
BRANCH: cu/00-compose-baseline
DEPENDS ON: none (parallel with CX-00 on disjoint paths)
READ FIRST: Repository Conventions sections 11.1, 12; System Design sections 3, 7.
ALLOWED PATHS:
- `compose.yaml`
- `compose.override.yaml.example`
- `infra/local/**`
- `services/*/.env.example`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: `pyproject.toml`, `uv.lock`, `.nvmrc`, `services/`, `libs/`, `web/`
CONTRACTS TOUCHED: none
TASKS:
1. Author root `compose.yaml` defining services: `postgres` (PostgreSQL 16), `redis` (Redis 7), `azurite` (local Azure Blob Storage emulator), and `local-vault` (local mock secret service).
2. Author `compose.override.yaml.example` documenting local developer configuration overrides.
3. Configure PostgreSQL container initialization scripts creating the central `control` database and migrator superuser.
4. Create per-service `.env.example` templates referencing standard Compose service connection strings.
5. Create `docs/progress/cursor.md` tracking Cursor phase progression.
NON-GOALS: Do not run application microservices containers until code skeletons exist.
TESTS REQUIRED: Docker Compose configuration validation test: `docker compose config`.
VERIFICATION:
```bash
docker compose config
docker compose up -d postgres redis azurite
docker compose ps
docker compose down
```
Output: Services start cleanly and report healthy status; ports 5432 and 6379 accessible locally.
ACCEPTANCE CRITERIA:
- [ ] `compose.yaml` validates with no syntax errors.
- [ ] PostgreSQL and Redis start with persistent named volumes.
- [ ] No files in Codex or Antigravity owned paths are touched.
STOP AND ASK IF: Port collisions occur on local developer machine (5432, 6379).
HANDOFF OUTPUT: Local backing infrastructure ready for Gate G0.
COMMIT AND PR: `feat(infra): create root docker compose development baseline`
PROGRESS ENTRY: `CU-00 | Merged | Docker Compose baseline, PostgreSQL, Redis, Azurite | None | Open`

---

### PHASE: CU-01 GitHub Actions CI Skeleton
EFFORT: M (Est. review time: 30 mins)
GOAL: Establish path-aware GitHub Actions workflows running Ruff, pytest, ESLint, Prettier, contract validation, and coverage collection.
OWNER AGENT: Cursor
BRANCH: cu/01-ci-skeleton
DEPENDS ON: CU-00, CX-00 (Gate G0)
READ FIRST: Repository Conventions sections 8, 9.2, 13.1; Master Build Guide section 9.
ALLOWED PATHS:
- `.github/workflows/**`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: Application code, contracts, libs, web.
CONTRACTS TOUCHED: none
TASKS:
1. Create `.github/workflows/ci.yaml` with path-filtering rules for changed services, libraries, contracts, and frontend.
2. Add backend lint and format check job (`uv run ruff check .` and `uv run ruff format --check .`).
3. Add backend test job executing pytest across shared libraries and services.
4. Add contract schema validation job executing `scripts/validate_contracts.py`.
5. Add lockfile freshness check jobs verifying `uv.lock` and `pnpm-lock.yaml` are clean.
6. Configure coverage reporting output to artifact storage (gradual enforcement per Repository Conventions section 8).
NON-GOALS: Do not add automated deployment jobs yet (handled in CU-20).
TESTS REQUIRED: CI workflow execution test on pull request; matrix path evaluation test.
VERIFICATION:
```bash
# Locally test the validation scripts referenced by CI
uv run ruff check .
uv run python scripts/validate_contracts.py
```
Output: All CI check commands succeed locally.
ACCEPTANCE CRITERIA:
- [ ] Workflows trigger selectively based on path changes.
- [ ] Required status checks defined for pull requests.
- [ ] Coverage reports collected without blocking builds.
STOP AND ASK IF: GitHub Actions runner OS requires Windows or Linux specific adjustments.
HANDOFF OUTPUT: CI pipeline ready to guard all incoming PRs.
COMMIT AND PR: `ci: establish path-aware github actions quality pipeline`
PROGRESS ENTRY: `CU-01 | Merged | Path-aware CI workflow, lint, test, contract validation | None | Open`

---

### PHASE: CU-02 Traefik API Gateway and Routing
EFFORT: L (Est. review time: 35 mins)
GOAL: Configure Traefik gateway with TLS, path-based routing, JWT signature verification plugin, CORS headers, rate limiting, and request ID generation (Gate G1).
OWNER AGENT: Cursor
BRANCH: cu/02-gateway-routing
DEPENDS ON: CU-01, CX-05 (Gate G1)
READ FIRST: System Design sections 3, 7, 13.3; API Contracts sections 2.1, 3.1, 3.7; Master Build Guide section 10 (R-11, R-12).
ALLOWED PATHS:
- `gateway/**`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All backend services, libs, web.
CONTRACTS TOUCHED: none
TASKS:
1. Scaffold `gateway/` configuration with Traefik 3.x dynamic and static configuration files.
2. Configure path routing per API Contracts:
   - `/api/v1/auth/**`, `/api/v1/orgs`, `/api/v1/me` -> Core service.
   - `/api/v1/orgs/{org_id}/incidents/**` -> Core service.
   - `/api/v1/orgs/{org_id}/integrations/**`, `/api/v1/orgs/{org_id}/services/**`, `/api/v1/orgs/{org_id}/timeline-events/**` -> Ingestion service.
   - Routing for `/postmortems/{id}/...` (R-11): routes matching `/ai/edit`, `/sections/{key}/regenerate`, `/blameless-*` route to AI service; all other postmortem paths route to Core.
   - PagerDuty webhook path `/api/v1/webhooks/pagerduty/{token}` -> Ingestion service (R-12).
3. Configure JWT verification middleware checking Core's published public key for protected routes.
4. Configure CORS middleware allowing requests from the web application domain with credentials.
5. Configure rate limiting middleware with scoped limits and `Retry-After` headers.
6. Configure request ID injection middleware generating UUIDv7 `X-Request-ID` and propagating trace contexts.
NON-GOALS: Gateway does not access application databases or inspect business payloads.
TESTS REQUIRED: Gateway routing integration tests verifying route matching, priority routing for postmortem subpaths, CORS preflight responses, and JWT rejection.
VERIFICATION:
```bash
# Execute gateway route verification script with mock upstream containers
docker compose -f gateway/tests/compose.test.yaml up --abort-on-container-exit
```
Output: All gateway routing tests pass; request IDs propagated; CORS headers returned.
ACCEPTANCE CRITERIA:
- [ ] Route priority correctly separates Core and AI postmortem paths (R-11).
- [ ] PagerDuty webhook route routes to Ingestion (R-12).
- [ ] Protected endpoints reject unauthenticated requests at gateway layer.
STOP AND ASK IF: Domain routing structure differs between local and production.
HANDOFF OUTPUT: Gateway operational (Gate G1 complete).
COMMIT AND PR: `feat(gateway): implement traefik routing jwt validation and rate limiting`
PROGRESS ENTRY: `CU-02 | Merged | Traefik gateway routing, path priority, CORS, rate limits | None | Open`

---

### PHASE: CU-03 Ingestion Service Skeleton and Schema
EFFORT: M (Est. review time: 30 mins)
GOAL: Scaffold `services/ingestion` Django project, integrate shared libraries (`retrace_common`, `retrace_auth`, `retrace_tenancy`, `retrace_events`), and implement ingestion schema models.
OWNER AGENT: Cursor
BRANCH: cu/03-ingestion-skeleton
DEPENDS ON: CU-02, CX-10 (Gate G2)
READ FIRST: System Design section 15; Database Design section 6; Repository Conventions section 4.1.
ALLOWED PATHS:
- `services/ingestion/**`
- `contracts/ingestion/openapi.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ingestion/openapi.json`
TASKS:
1. Scaffold `services/ingestion` Django 5 / DRF project with Celery worker configuration.
2. Integrate `libs/retrace_common`, `retrace_auth`, `retrace_tenancy`, `retrace_events` packages.
3. Implement `ingestion` schema models:
   - `integration_connections`, `integration_secrets`, `allowlist_entries`
   - `services`, `service_links`, `discovery_runs`
   - Common tables: `jobs`, `outbox`, `inbox`
4. Configure database router and dynamic tenant connection cache for `ingestion_{org_id}` database role.
5. Create initial migration files for `ingestion` schema.
6. Configure drf-spectacular OpenAPI schema publication for Ingestion.
NON-GOALS: Do not implement connector integrations or evidence discovery logic yet.
TESTS REQUIRED: Model migration tests, tenant database router tests for ingestion schema, service role permission isolation tests.
VERIFICATION:
```bash
uv run python services/ingestion/manage.py makemigrations --check
uv run pytest services/ingestion/tests/test_models.py
```
Output: Ingestion models migrate cleanly; tenant context router functions.
ACCEPTANCE CRITERIA:
- [ ] Ingestion schema models adhere strictly to Database Design section 6.
- [ ] Missing tenant context prevents database queries.
- [ ] OpenAPI publication configured in `contracts/ingestion/`.
STOP AND ASK IF: Database migration runner role requires specific grants.
HANDOFF OUTPUT: Ingestion service foundation ready for connectors and catalog.
COMMIT AND PR: `feat(ingestion): scaffold ingestion service and schema baseline`
PROGRESS ENTRY: `CU-03 | Merged | Ingestion service scaffold, models, tenant routing | contracts/ingestion/openapi.json | Open`

---

### PHASE: CU-04 Integration Connections and Encrypted Secrets
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement integration connections management, envelope-encrypted secret storage via tenant data key, and admin allowlist management API.
OWNER AGENT: Cursor
BRANCH: cu/04-connections-secrets
DEPENDS ON: CU-03
READ FIRST: PRD 8.3 INT-4, INT-5; System Design sections 8, 15; Database Design section 6 (`integration_connections`, `integration_secrets`, `allowlist_entries`).
ALLOWED PATHS:
- `services/ingestion/apps/integrations/**`
- `contracts/ingestion/openapi.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ingestion/openapi.json`
TASKS:
1. Implement `integration_secrets` model storing ciphertext, nonce, and `key_version`.
2. Implement encryption helper unwrapping tenant data key and encrypting integration tokens with AES-256-GCM before database write.
3. Implement `GET /api/v1/orgs/{org_id}/integrations` listing connected providers and health status.
4. Implement `DELETE /api/v1/orgs/{org_id}/integrations/{id}` disconnecting integration and purging stored secret ciphertext.
5. Implement `GET` and `PUT /api/v1/orgs/{org_id}/integrations/{id}/allowlist` managing allowed Slack channels, GitHub repos, and PagerDuty services.
6. Ensure API responses never return raw secret values, only a masked hint where applicable.
NON-GOALS: Do not perform external API requests to providers yet.
TESTS REQUIRED: Secret encryption at rest test; API secret masking verification test; allowlist validation tests.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_secrets_allowlist.py
```
Output: Secrets encrypted at rest; API returns masked hints; allowlist entries validated.
ACCEPTANCE CRITERIA:
- [ ] Secret values are strictly write-only in API contracts.
- [ ] Disconnecting an integration permanently deletes encrypted secret keys.
- [ ] Allowlists restrict accessible provider resources.
STOP AND ASK IF: Key Vault unwrap failure occurs during local development.
HANDOFF OUTPUT: Integration connections and allowlists unblock Frontend M05 (AG-09).
COMMIT AND PR: `feat(ingestion): implement integration secrets encryption and allowlist api`
PROGRESS ENTRY: `CU-04 | Merged | Integration connections, AES-GCM secrets, allowlists API | contracts/ingestion/openapi.json | Open`

---

### PHASE: CU-05 PagerDuty Connector and Webhook Handler
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement PagerDuty connector, signed webhook verification endpoint rejecting stale timestamps, incident synchronization job, and `incident.reported` event publishing.
OWNER AGENT: Cursor
BRANCH: cu/05-pagerduty-connector
DEPENDS ON: CU-04
READ FIRST: PRD 8.3 INT-3; System Design sections 8, 15, 20.1; API Contracts sections 4.2, 7.4 (R-12); Database Design section 6.
ALLOWED PATHS:
- `services/ingestion/apps/connectors/pagerduty/**`
- `services/ingestion/apps/webhooks/**`
- `contracts/ingestion/openapi.json`
- `contracts/events/ingestion/incident.reported.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ingestion/openapi.json`, `contracts/events/ingestion/incident.reported.json`
TASKS:
1. Implement PagerDuty API client with rate-limiting backoff and recorded response fixtures.
2. Implement `POST /api/v1/webhooks/pagerduty/{token}`:
   - Validate PagerDuty webhook signature header using connection secret.
   - Reject stale timestamps older than configured threshold (default 5 minutes).
   - Resolve organization tenant ID from webhook token hash.
   - Publish `incident.reported` event via transactional outbox.
3. Implement `sync_pagerduty_incidents` Celery task for periodic polling of resolved incidents.
4. Extract incident metadata: external ID, title, status, severity, timestamps (`started_at`, `detected_at`, `resolved_at`), responders, and linked service.
NON-GOALS: Live external calls during automated CI (always use recorded responses and mock server).
TESTS REQUIRED: Webhook signature verification test; stale timestamp rejection test; idempotent replay test; incident payload mapping test.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_pagerduty_webhook.py
```
Output: Webhook validates signatures, rejects replayed or stale payloads, and emits event.
ACCEPTANCE CRITERIA:
- [ ] Valid signed webhook emits `incident.reported` event with standard envelope.
- [ ] Invalid signature or expired timestamp returns 401/400.
- [ ] Webhook processing is idempotent.
STOP AND ASK IF: PagerDuty v3 webhook payload format differences are identified.
HANDOFF OUTPUT: PagerDuty incident ingestion ready; feeds Core incident creation (CX-11).
COMMIT AND PR: `feat(ingestion): implement pagerduty connector and signed webhook handler`
PROGRESS ENTRY: `CU-05 | Merged | PagerDuty signed webhook, sync job, incident.reported event | contracts/events/ingestion/incident.reported.json | Open`

---

### PHASE: CU-06 Slack Connector and Resumable History Fetcher
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement Slack OAuth connection, resumable history fetcher respecting Slack rate limits (Retry-After), channel allowlist enforcement, and export upload fallback per ADR.
OWNER AGENT: Cursor
BRANCH: cu/06-slack-connector
DEPENDS ON: CU-05
READ FIRST: PRD 8.3 INT-1; System Design section 15; Master Build Guide section 6.2.
ALLOWED PATHS:
- `services/ingestion/apps/connectors/slack/**`
- `contracts/ingestion/openapi.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ingestion/openapi.json`
TASKS:
1. Check Slack official Web API documentation for conversations.history rate limits.
2. Implement Slack OAuth connection flow storing tokens encrypted with tenant data key.
3. Implement resumable history fetcher:
   - Read messages and thread replies within time window for allowlisted channels only.
   - Respect Slack `Retry-After` headers and rate-limit backoff.
   - Implement pagination with resumption state saved to allow safe continuation.
4. Support organization-owned Slack app credentials to bypass distribution tier rate limits.
5. Implement fallback parser accepting manual Slack JSON export upload.
NON-GOALS: Do not read private channels or direct messages unless explicitly allowlisted by Admin.
TESTS REQUIRED: Mocked Slack API tests with simulated 429 rate limit and `Retry-After`; channel allowlist enforcement test; thread reply parsing test.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_slack_connector.py
```
Output: Slack history fetches with resumption; rate limits handled cleanly; allowlists respected.
ACCEPTANCE CRITERIA:
- [ ] Connector strictly obeys `Retry-After` header without failing job.
- [ ] Messages from non-allowlisted channels are ignored.
- [ ] Resumable state persists across rate-limit pauses.
STOP AND ASK IF: Slack API scope requirements have changed for bot vs user tokens.
HANDOFF OUTPUT: Slack evidence fetcher ready for discovery pipeline.
COMMIT AND PR: `feat(ingestion): implement slack connector with resumable history fetcher`
PROGRESS ENTRY: `CU-06 | Merged | Slack OAuth, rate-limited history fetcher, export fallback | contracts/ingestion/openapi.json | Open`

---

### PHASE: CU-07 Service Catalog and Link Hints
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement service catalog CRUD API, service links to Slack channels, repositories, and PagerDuty services, enforcing allowlist validation rules.
OWNER AGENT: Cursor
BRANCH: cu/07-service-catalog
DEPENDS ON: CU-06
READ FIRST: PRD 8.4 SVC-1..SVC-3; System Design sections 14, 15; Database Design section 6 (`services`, `service_links`).
ALLOWED PATHS:
- `services/ingestion/apps/catalog/**`
- `contracts/ingestion/openapi.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ingestion/openapi.json`
TASKS:
1. Implement `services` and `service_links` models.
2. Implement `GET /api/v1/orgs/{org_id}/services` with page pagination and filtering.
3. Implement `POST`, `PATCH`, `DELETE /api/v1/orgs/{org_id}/services` (Admin only).
4. Implement `PUT /api/v1/orgs/{org_id}/services/{id}/links` linking service to Slack channels, GitHub repos, and PagerDuty services.
5. Validate that linked Slack channels and GitHub repositories exist in `allowlist_entries` before allowing link creation.
6. Provide discovery hints endpoint summarizing linked sources for an incident.
NON-GOALS: Do not build automated link suggestion in v1 (P1).
TESTS REQUIRED: Catalog CRUD tests; role permission tests (Admin write, Member read); allowlist link validation tests.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_service_catalog.py
```
Output: Service catalog CRUD functions; un-allowlisted links rejected.
ACCEPTANCE CRITERIA:
- [ ] Members can read catalog; only Admins can create or modify services.
- [ ] Service links enforce that the linked resource exists in allowlist.
- [ ] Archived services remain in database for history but excluded from active queries.
STOP AND ASK IF: Archiving vs soft-delete convention for services needs clarification.
HANDOFF OUTPUT: Service catalog APIs unblock Frontend M06 (AG-10).
COMMIT AND PR: `feat(ingestion): implement service catalog and allowlist link validation`
PROGRESS ENTRY: `CU-07 | Merged | Service catalog CRUD, service links, allowlist enforcement | contracts/ingestion/openapi.json | Open`

---

### PHASE: CU-08 Evidence Normalization and Five Timestamp Fields
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement evidence normalization pipeline enforcing redaction rules, deduplication, and the five timestamp fields per R-04 (`occurred_at`, `occurred_at_raw`, `observed_at`, `timestamp_precision`, `timezone_known`).
OWNER AGENT: Cursor
BRANCH: cu/08-evidence-normalization
DEPENDS ON: CU-07
READ FIRST: PRD 8.3 INT-8; API Contracts sections 9.1, 9.2, 10; Database Design section 6 (`evidence_items`); Master Build Guide section 10 (R-04).
ALLOWED PATHS:
- `services/ingestion/apps/evidence/**`
- `contracts/ingestion/openapi.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ingestion/openapi.json`
TASKS:
1. Update `evidence_items` model via migration to include: `occurred_at_raw`, `observed_at`, `timestamp_precision`, `timezone_known`, making `occurred_at` nullable for date-only/uncertain events (R-04).
2. Implement redaction pipeline stripping email addresses, bearer tokens, API keys, and sensitive environment variables before saving to `text_redacted`.
3. Implement candidate deduplication by `(incident_id, source, source_ref)`.
4. Ensure `occurred_at` in UTC is never populated with fabricated precision or assumed timezone certainty.
5. Implement manual evidence creation endpoint `POST /incidents/{id}/evidence`: link-based fetch for allowlisted hosts or store as text note without outbound fetching.
NON-GOALS: Never store raw unredacted provider payloads in evidence tables.
TESTS REQUIRED: Redaction rule tests for tokens and emails; five timestamp fields mapping tests; deduplication collision tests; unknown timezone preservation tests.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_evidence_normalization.py
```
Output: Redaction removes secrets; timestamps preserve source precision without inventing certainty.
ACCEPTANCE CRITERIA:
- [ ] All five timestamp fields populated accurately from source data.
- [ ] Sensitive tokens and emails are redacted before database storage.
- [ ] Deduplication prevents duplicate evidence rows.
STOP AND ASK IF: Custom regex redaction patterns are required per organization.
HANDOFF OUTPUT: Normalized evidence structure ready for discovery and scoring.
COMMIT AND PR: `feat(ingestion): implement evidence normalization five timestamp fields and redaction`
PROGRESS ENTRY: `CU-08 | Merged | Evidence normalization, five timestamp fields, redaction engine | contracts/ingestion/openapi.json | Open`

---

### PHASE: CU-09 Evidence Discovery and Scoring Job
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement `discover_evidence` Celery job, candidate scoring algorithm (0 to 1), evidence preview API, and candidate include/exclude confirmation flow.
OWNER AGENT: Cursor
BRANCH: cu/09-discovery-scoring
DEPENDS ON: CU-08
READ FIRST: PRD 8.6 EVD-1..EVD-5; System Design sections 15, 20.1; API Contracts section 4.2; Database Design section 6 (`discovery_runs`, `evidence_items`).
ALLOWED PATHS:
- `services/ingestion/apps/discovery/**`
- `services/ingestion/tasks/**`
- `contracts/ingestion/openapi.json`
- `contracts/events/ingestion/evidence.ready.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ingestion/openapi.json`, `contracts/events/ingestion/evidence.ready.json`
TASKS:
1. Implement `discover_evidence` Celery task:
   - Calculate time window: 60 minutes before first alert to 30 minutes after resolution.
   - Formulate search plan based on affected services, incident type, and allowlists.
   - Fetch candidates from PagerDuty, linked Slack channels, and search keywords.
   - Score candidates 0.0 to 1.0 based on time closeness, service link, responder authorship, and keyword overlap.
   - Mark candidates above threshold as `included=true`, others as `included=false`.
   - Publish `evidence.ready` event via outbox.
2. Implement `GET /api/v1/orgs/{org_id}/incidents/{id}/evidence` returning paged evidence with scores and reasons.
3. Implement `PATCH /api/v1/orgs/{org_id}/evidence/{id}` toggling inclusion state.
4. Implement `POST /api/v1/orgs/{org_id}/incidents/{id}/evidence/confirm` confirming candidate set and triggering timeline generation.
NON-GOALS: Do not run AI postmortem generation yet (handled in AI service).
TESTS REQUIRED: Scoring algorithm unit tests; discovery window calculation tests; include/exclude toggle tests; `evidence.ready` event delivery test.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_discovery_job.py
```
Output: Discovery searches allowed sources, scores candidates, and emits event.
ACCEPTANCE CRITERIA:
- [ ] Candidates above threshold included by default; score reasons recorded.
- [ ] Author can include or exclude items with one click.
- [ ] Outbound search never queries non-allowlisted sources.
STOP AND ASK IF: Scoring weight adjustments are needed for specific incident types.
HANDOFF OUTPUT: Discovery and preview ready for Frontend M07 (AG-11).
COMMIT AND PR: `feat(ingestion): implement evidence discovery scoring and confirmation workflow`
PROGRESS ENTRY: `CU-09 | Merged | Evidence discovery job, candidate scoring, preview API | contracts/events/ingestion/evidence.ready.json | Open`

---

### PHASE: CU-10 Evidence Snapshots and AI Invalidation Signals
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement `evidence_snapshots` table, snapshot hashing, immutable snapshot versioning, and cancellation/stale signals for in-flight AI jobs on evidence changes (R-06).
OWNER AGENT: Cursor
BRANCH: cu/10-evidence-snapshots
DEPENDS ON: CU-09
READ FIRST: API Contracts sections 9.3, 10; AI Pipeline Spec section 5; Master Build Guide section 10 (R-06).
ALLOWED PATHS:
- `services/ingestion/apps/snapshots/**`
- `contracts/ingestion/openapi.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ingestion/openapi.json`
TASKS:
1. Implement `evidence_snapshots` model with: `id`, `incident_id`, `snapshot_hash`, `event_ids`, `included_count`, `created_at`, `status` (`active`, `stale`, `cancelled`).
2. When evidence is included, excluded, or edited after confirmation, create a new immutable `evidence_snapshots` row.
3. Mark prior active snapshot as `stale`.
4. Send cancellation/stale signal for any running AI generation job referencing the previous snapshot.
5. Provide internal API endpoint for AI service to retrieve authorized snapshot event registry.
NON-GOALS: Never rewrite historical postmortem versions when an evidence snapshot changes.
TESTS REQUIRED: Snapshot hash immutability test; stale status transition test on evidence toggle; prior version snapshot reference preservation test.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_evidence_snapshots.py
```
Output: Snapshots generated with SHA-256 content hashes; evidence edits transition prior snapshots to stale.
ACCEPTANCE CRITERIA:
- [ ] Every evidence modification creates a new snapshot ID.
- [ ] In-flight jobs against older snapshots receive stale/cancelled signal.
- [ ] Historical postmortem snapshot references remain untouched.
STOP AND ASK IF: Redis pub/sub vs Celery revoke for job cancellation signals.
HANDOFF OUTPUT: Snapshot mechanics ready for AI pipeline S0 (CX-19).
COMMIT AND PR: `feat(ingestion): implement evidence snapshots and invalidation mechanics`
PROGRESS ENTRY: `CU-10 | Merged | Evidence snapshots table, hash verification, stale signals | contracts/ingestion/openapi.json | Open`

---

### PHASE: CU-11 Timeline Builder and Discrepancy Detection
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement `build_timeline` job, chat burst merging, key moment detection, phase classification, discrepancy flags, manual event support, and timeline APIs.
OWNER AGENT: Cursor
BRANCH: cu/11-timeline-builder
DEPENDS ON: CU-10
READ FIRST: PRD 8.6 EVD-4..EVD-9; System Design section 20.2; API Contracts sections 4.2, 9.2; Database Design section 6 (`timeline_events`, `timeline_event_evidence`).
ALLOWED PATHS:
- `services/ingestion/apps/timeline/**`
- `contracts/ingestion/openapi.json`
- `contracts/events/ingestion/timeline.ready.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ingestion/openapi.json`, `contracts/events/ingestion/timeline.ready.json`
TASKS:
1. Implement `timeline_events` and `timeline_event_evidence` models.
2. Implement `build_timeline` Celery task:
   - Sort included evidence chronologically with source priority tie-breakers.
   - Merge chat bursts: messages in same thread within 2 minutes merge into single event.
   - Detect key moments: first symptom, detection, escalation, mitigation, resolution.
   - Partition into phases: detection, diagnosis, mitigation, recovery.
   - Detect timestamp discrepancies: flag events where sources disagree on time by more than configured threshold without hiding conflict.
   - Rebuilding timeline preserves manual events and manual edits (`is_manual=true`).
   - Publish `timeline.ready` event via outbox.
3. Implement `GET /api/v1/orgs/{org_id}/incidents/{id}/timeline` with cursor pagination.
4. Implement `POST`, `PATCH`, `DELETE /api/v1/orgs/{org_id}/timeline-events/{id}` for manual events.
NON-GOALS: Do not hide or force resolution of timestamp discrepancies.
TESTS REQUIRED: Chat burst merge test; key moment rule detection test; discrepancy flag test; manual event preservation test across rebuilds; cursor pagination stability test.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_timeline_builder.py
```
Output: Timeline orders events stably, merges bursts, flags discrepancies, and emits event.
ACCEPTANCE CRITERIA:
- [ ] Timeline events cite underlying evidence items via junction table.
- [ ] Sources with conflicting times display discrepancy flags.
- [ ] Manual events survive automated timeline rebuilds.
STOP AND ASK IF: Chat burst merge time window parameter requires adjustment (default 2 mins confirmed).
HANDOFF OUTPUT: Timeline builder unblocks Frontend timeline (AG-12).
COMMIT AND PR: `feat(ingestion): implement timeline builder discrepancy detection and manual events`
PROGRESS ENTRY: `CU-11 | Merged | Timeline builder, burst merging, discrepancy flags, cursor API | contracts/events/ingestion/timeline.ready.json | Open`

---

### PHASE: CU-12 Ingestion Internal API for AI Service
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement internal service-token authenticated API exposing authorized timeline events and evidence snapshots for the AI service (Gate G3).
OWNER AGENT: Cursor
BRANCH: cu/12-ingestion-internal-api
DEPENDS ON: CU-11
READ FIRST: System Design sections 14, 15; API Contracts sections 4.5, 9.1; AI Pipeline Spec section 5.
ALLOWED PATHS:
- `services/ingestion/apps/internal/**`
- `contracts/ingestion/internal.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ingestion/internal.json`
TASKS:
1. Implement internal endpoint `GET /api/v1/internal/incidents/{incident_id}/timeline`:
   - Require valid service token (`retrace_auth` service identity verification).
   - Return normalized timeline events with stable IDs, kinds, redacted text, and five timestamp fields.
2. Implement internal endpoint `GET /api/v1/internal/snapshots/{snapshot_id}/events` returning exact snapshot event registry.
3. Verify that non-internal traffic or user access tokens cannot call internal endpoints.
4. Document internal contract schema in `contracts/ingestion/internal.json`.
NON-GOALS: Public gateway never routes internal endpoints to external clients.
TESTS REQUIRED: Service token authentication test; user token rejection test; snapshot event payload serialization test.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_internal_api.py
```
Output: Internal endpoints accept service tokens, reject user tokens, and serialize timeline accurately.
ACCEPTANCE CRITERIA:
- [ ] Accessible only with valid internal service token.
- [ ] Returns redacted, authorized evidence only.
- [ ] Gateway blocks external routing to internal endpoints.
STOP AND ASK IF: Service token audience claim format needs reconciliation (R-13).
HANDOFF OUTPUT: Ingestion internal API ready (Gate G3 complete). Unblocks AI pipeline integration.
COMMIT AND PR: `feat(ingestion): implement internal timeline and snapshot api for ai service`
PROGRESS ENTRY: `CU-12 | Merged | Ingestion internal timeline and evidence snapshot API | contracts/ingestion/internal.json | Open`

---

### PHASE: CU-13 Ingestion Hardening and Connector Isolation
EFFORT: M (Est. review time: 30 mins)
GOAL: Harden Ingestion connectors with adversarial payload testing, prompt injection screening signals, rate-limit backoff verification, and two-tenant isolation suites.
OWNER AGENT: Cursor
BRANCH: cu/13-ingestion-hardening
DEPENDS ON: CU-12
READ FIRST: AI Pipeline Spec section 11; Master Build Guide section 9.1; Database Design section 3.2.
ALLOWED PATHS:
- `services/ingestion/tests/**`
- `services/ingestion/apps/**`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: none
TASKS:
1. Implement test suite injecting adversarial prompts ("ignore previous instructions") into simulated Slack messages and commit messages to verify evidence ingestion handles them safely as untrusted data.
2. Write two-tenant isolation tests verifying that tenant A cannot access tenant B's integration connections, evidence, or timeline events.
3. Test connector behavior under simulated network disconnects and continuous 429 rate limiting.
4. Verify database role `ingestion_{org_id}` permissions: ensure role cannot access `core` or `ai` schemas.
NON-GOALS: Do not relax security checks for convenience.
TESTS REQUIRED: Adversarial evidence ingestion test; two-tenant cross-read rejection test; direct database role privilege test.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_isolation_hardening.py
```
Output: Zero cross-tenant data leaks; adversarial text ingested safely without escaping; role privileges enforced.
ACCEPTANCE CRITERIA:
- [ ] Connectors treat all incoming provider text as untrusted data.
- [ ] Database role boundary verified by direct SQL privilege tests.
- [ ] Rate-limit backoff handles prolonged 429 responses cleanly.
STOP AND ASK IF: Any provider test reveals unhandled exception during parsing.
HANDOFF OUTPUT: Ingestion service hardened and production-ready.
COMMIT AND PR: `test(ingestion): harden connectors with isolation and security suites`
PROGRESS ENTRY: `CU-13 | Merged | Ingestion isolation hardening, injection tests, role checks | None | Open`

---

### PHASE: CU-14 Notifications Service Skeleton and In-App Notifications
EFFORT: M (Est. review time: 30 mins)
GOAL: Scaffold `services/notifications` Django project, implement `notifications` schema models, in-app notifications API, and notification settings preferences.
OWNER AGENT: Cursor
BRANCH: cu/14-notifications-skeleton
DEPENDS ON: CU-13, CX-10 (Gate G2)
READ FIRST: PRD 8.11 ACT-5; System Design section 17; API Contracts section 4.4; Database Design section 8 (`notifications`, `notification_settings`).
ALLOWED PATHS:
- `services/notifications/**`
- `contracts/notifications/openapi.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/notifications/openapi.json`
TASKS:
1. Scaffold `services/notifications` Django 5 / DRF project targeting Python 3.12.
2. Implement `notifications` schema models: `reminder_log`, `notifications`, `notification_settings`, `email_log`, and common tables.
3. Implement `GET /api/v1/orgs/{org_id}/notifications` listing in-app notifications with read status.
4. Implement `PATCH /api/v1/orgs/{org_id}/notifications/{id}` marking notification as read.
5. Implement `GET` and `PATCH /api/v1/orgs/{org_id}/notification-settings` managing user email and in-app preferences.
6. Configure drf-spectacular OpenAPI schema publication for Notifications.
NON-GOALS: Do not send live emails yet (handled in CU-16).
TESTS REQUIRED: Model migration tests; in-app notification mark-as-read test; user preferences update test; two-tenant isolation tests.
VERIFICATION:
```bash
uv run python services/notifications/manage.py makemigrations --check
uv run pytest services/notifications/tests/test_notifications_api.py
```
Output: Notifications models migrate cleanly; in-app endpoints function; isolation verified.
ACCEPTANCE CRITERIA:
- [ ] In-app notifications support read tracking.
- [ ] Preferences allow muting specific notification types.
- [ ] Tenant context boundary enforced on all notification reads.
STOP AND ASK IF: Route placement for notification settings requires confirmation (R-22, under `account/` confirmed).
HANDOFF OUTPUT: In-app notifications APIs unblock Frontend M19 (AG-21).
COMMIT AND PR: `feat(notifications): scaffold notifications service and in-app notifications api`
PROGRESS ENTRY: `CU-14 | Merged | Notifications service scaffold, in-app notifications, preferences | contracts/notifications/openapi.json | Open`

---

### PHASE: CU-15 Reminders Daily Scan Job and Escalation Logic
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement `scan_stalled_items` daily Celery beat job, stage escalation logic (pre_due, stalled, escalated), `reminder_log` deduplication, and Core internal client integration.
OWNER AGENT: Cursor
BRANCH: cu/15-reminders-scan-job
DEPENDS ON: CU-14, CX-15
READ FIRST: PRD 8.11 ACT-5; System Design section 17, 20.5; Database Design section 8 (`reminder_log`).
ALLOWED PATHS:
- `services/notifications/tasks/**`
- `services/notifications/apps/reminders/**`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: none
TASKS:
1. Implement internal HTTP client calling Core's `GET /api/v1/internal/action-items/stalled` with service token.
2. Implement `scan_stalled_items` Celery beat task executing daily:
   - Stage 0 (`pre_due`): 2 days before due date, notify owner.
   - Stage 1 (`stalled`): on first day stalled, notify owner.
   - Stage 2 (`escalated`): stalled longer than escalation setting (default 3 days), notify Admins.
3. Enforce composite unique constraint on `reminder_log (action_item_id, stage, recipient_user_id, channel)`: never send duplicate reminder for same stage.
4. Create in-app notification row for each reminder stage.
NON-GOALS: Notifications service never stores its own copy of action item data (always queries Core).
TESTS REQUIRED: Reminder stage progression tests; `reminder_log` duplicate suppression test; escalation timing tests.
VERIFICATION:
```bash
uv run pytest services/notifications/tests/test_reminders_scan.py
```
Output: Scan job queries Core, calculates stages, writes to reminder log, and suppresses duplicates.
ACCEPTANCE CRITERIA:
- [ ] No duplicate reminder is created for the same item and stage.
- [ ] Escalation stage notifies Admins when stall duration exceeds threshold.
- [ ] Recipient preferences respected before reminder generation.
STOP AND ASK IF: Timezone handling for daily schedule trigger time requires configuration.
HANDOFF OUTPUT: Reminder scan operational.
COMMIT AND PR: `feat(notifications): implement reminders daily scan job and escalation logic`
PROGRESS ENTRY: `CU-15 | Merged | Stalled items daily scan, stage escalation, reminder log | None | Open`

---

### PHASE: CU-16 Email Delivery Adapter and Templates
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement provider-agnostic email adapter (supporting SMTP and Azure Communication Services), email templates, `email_log` tracking, and retention rules (R-21).
OWNER AGENT: Cursor
BRANCH: cu/16-email-delivery
DEPENDS ON: CU-15
READ FIRST: PRD section 10; System Design section 17; Database Design sections 8 (`email_log`), 10.
ALLOWED PATHS:
- `services/notifications/apps/email/**`
- `services/notifications/templates/**`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: none
TASKS:
1. Implement `EmailProvider` interface and mock email provider for local development and automated testing.
2. Implement Azure Communication Services Email and SMTP provider implementations (R-21, NEEDS PRAVEEN).
3. Implement responsive HTML and plain text email templates: invitations, password reset, review requested, action due, action stalled, action escalated.
4. Implement `send_email` background task with exponential backoff retries and status recording in `email_log`.
5. Implement 90-day retention purge job for `email_log` containing personal email addresses.
NON-GOALS: Do not send live emails in automated test runs (always mock provider).
TESTS REQUIRED: Email template rendering tests; email adapter retry backoff test; mock email delivery test; log retention purge test.
VERIFICATION:
```bash
uv run pytest services/notifications/tests/test_email_delivery.py
```
Output: Templates render with correct variables; mock email adapter logs delivery; purge deletes old logs.
ACCEPTANCE CRITERIA:
- [ ] Email provider is swappable via configuration without code changes.
- [ ] `email_log` tracks delivery status, attempts, and provider message ID.
- [ ] Purge task deletes email logs older than 90 days.
STOP AND ASK IF: Praveen has decided between Azure Communication Services Email vs SMTP (R-21).
HANDOFF OUTPUT: Email delivery ready for all system notifications and auth flows.
COMMIT AND PR: `feat(notifications): implement email delivery adapter templates and logging`
PROGRESS ENTRY: `CU-16 | Merged | Email delivery adapter, HTML templates, email_log retention | None | Open`

---

### PHASE: CU-17 Migration Runner Container Job
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement the independent migration runner job in `infra/` reading tenant registry, executing migrations per tenant and service with service roles, recording versions, and reporting failures (Gate G2 with CX-10).
OWNER AGENT: Cursor
BRANCH: cu/17-migration-runner
DEPENDS ON: CU-03, CX-10 (Gate G2)
READ FIRST: Repository Conventions section 13.2; System Design sections 4.6, 23.3; Database Design section 3.2 (`migrator` role).
ALLOWED PATHS:
- `infra/migrator/**`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: Application code in services.
CONTRACTS TOUCHED: none
TASKS:
1. Create `infra/migrator/` container definition and entrypoint script.
2. Implement migration runner logic:
   - Connect to control database using `migrator` role credentials.
   - Query all active tenants from `tenant_registry`.
   - For each active tenant and each service (`core`, `ingestion`, `ai`, `notifications`), execute pending migrations in bounded parallel batches.
   - Execute migrations using that service's specific role for the tenant.
   - Record applied migration version per service in `tenant_registry.schema_versions`.
   - If a tenant migration fails, log error, record `last_error` in registry, and continue safely with remaining tenants.
3. Add dry-run check command for CI pre-deployment validation.
NON-GOALS: Developer workstations never execute migrations directly against production databases.
TESTS REQUIRED: Runner execution test across multiple simulated tenants; failure containment test (one failing tenant does not halt others); version recording verification test.
VERIFICATION:
```bash
# Execute migrator script against local test environment
python infra/migrator/run_migrations.py --dry-run
```
Output: Migrator connects, inspects registry, runs migrations, and updates version records.
ACCEPTANCE CRITERIA:
- [ ] Migrations run using dedicated schema roles without cross-schema access.
- [ ] Tenant failure is contained and recorded in registry without aborting rollout.
- [ ] Applied versions match expected service migration states.
STOP AND ASK IF: Concurrency limits for parallel tenant migrations require tuning (default 5 concurrent).
HANDOFF OUTPUT: Migration runner ready for Gate G2 and CI/CD pipelines.
COMMIT AND PR: `feat(infra): implement tenant registry driven migration runner`
PROGRESS ENTRY: `CU-17 | Merged | Independent migration runner, per-tenant recording, fault tolerance | None | Open`

---

### PHASE: CU-18 Cross-Service Event Consumers and Relays
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement outbox relays and consumer workers for Ingestion and Notifications services handling cross-service domain events (`draft.ready`, `postmortem.submitted`, `postmortem.approved`, `incident.description_submitted`).
OWNER AGENT: Cursor
BRANCH: cu/18-event-consumers-relays
DEPENDS ON: CU-15, CX-14
READ FIRST: System Design section 6.2, 6.4; API Contracts section 7; Database Design section 3.3 (`outbox`, `inbox`).
ALLOWED PATHS:
- `services/ingestion/events/**`
- `services/notifications/events/**`
- `contracts/events/**`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: Consumes Core and AI event schemas.
TASKS:
1. Implement outbox relay Celery tasks for Ingestion and Notifications services polling unpublished outbox records and publishing to Redis Streams.
2. Implement Ingestion consumer for `incident.description_submitted` initiating evidence discovery job.
3. Implement Notifications consumers for:
   - `draft.ready`: notify incident author that draft postmortem is ready for review.
   - `postmortem.submitted`: notify organization reviewers and Admins.
   - `postmortem.approved`: notify author and team of approval.
4. Implement consumer inbox deduplication and aggregate version checking using `retrace_events`.
5. Implement dead-letter stream error handling.
NON-GOALS: Consumers never perform database mutations on other services' schemas directly.
TESTS REQUIRED: Event publication test; outbox relay retry test; consumer deduplication test; dead-letter routing on repeated failure test.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_event_consumers.py
uv run pytest services/notifications/tests/test_event_consumers.py
```
Output: Events relay to Redis Streams; consumers process events idempotently.
ACCEPTANCE CRITERIA:
- [ ] At-least-once delivery handled with complete inbox deduplication.
- [ ] Notifications generated accurately for submitted, approved, and ready drafts.
- [ ] Failed events move to dead-letter stream after configured retries.
STOP AND ASK IF: Redis consumer group naming convention requires standardization.
HANDOFF OUTPUT: Event-driven notification loop operational (Gate G5 ready).
COMMIT AND PR: `feat(events): implement cross-service event relays and consumers`
PROGRESS ENTRY: `CU-18 | Merged | Ingestion and notifications event relays, consumer handlers | None | Open`

---

### PHASE: CU-19 GitHub Connector (Stretch, Optional)
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement GitHub App connector reading deployments, merged pull requests, and workflow runs for allowlisted repositories, placed behind a feature flag.
OWNER AGENT: Cursor
BRANCH: cu/19-github-connector
DEPENDS ON: CU-08
READ FIRST: PRD 8.3 INT-2; System Design section 15; Repository Conventions section 3.
ALLOWED PATHS:
- `services/ingestion/apps/connectors/github/**`
- `contracts/ingestion/openapi.json`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: All other services and libraries.
CONTRACTS TOUCHED: `contracts/ingestion/openapi.json`
TASKS:
1. Place GitHub integration code behind feature flag `FEATURE_GITHUB_CONNECTOR=false`.
2. Implement GitHub App OAuth installation flow and private key authentication.
3. Implement candidate fetcher retrieving:
   - Merged pull requests within incident window.
   - Commit history on default branch.
   - Deployment events and workflow runs.
4. Normalize fetched items into evidence candidates with five timestamp fields.
5. Support rate-limit backoff on GitHub REST API.
NON-GOALS: Do not build GitHub issue creation in v1 (P1).
TESTS REQUIRED: Mocked GitHub API response tests; feature flag toggle test; repository allowlist enforcement test.
VERIFICATION:
```bash
uv run pytest services/ingestion/tests/test_github_connector.py
```
Output: GitHub connector parses PRs, deployments, and commits when enabled by feature flag.
ACCEPTANCE CRITERIA:
- [ ] Connector is disabled by default behind feature flag.
- [ ] When enabled, reads only allowlisted repositories within incident window.
- [ ] Normalizes GitHub deployments and PRs into standard evidence candidates.
STOP AND ASK IF: Praveen decides to defer GitHub connector entirely.
HANDOFF OUTPUT: GitHub evidence integration available as stretch capability.
COMMIT AND PR: `feat(ingestion): implement optional github connector behind feature flag`
PROGRESS ENTRY: `CU-19 | Merged | GitHub App connector, deployments, PRs, feature flag | contracts/ingestion/openapi.json | Open`

---

### PHASE: CU-20 Container Image Builds and Staging Deployment
EFFORT: L (Est. review time: 35 mins)
GOAL: Create production multi-stage Dockerfiles for all services, image vulnerability scanning in CI, automatic staging deployment, and manual production approval gate.
OWNER AGENT: Cursor
BRANCH: cu/20-docker-staging-deploy
DEPENDS ON: CU-18
READ FIRST: Repository Conventions sections 7, 13.1; System Design section 7.
ALLOWED PATHS:
- `services/*/Dockerfile`
- `gateway/Dockerfile`
- `.github/workflows/deploy.yaml`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: Application business code.
CONTRACTS TOUCHED: none
TASKS:
1. Create optimized, non-root multi-stage Dockerfiles for Core, Ingestion, AI, Notifications, and Gateway targeting Python 3.12 slim base images.
2. Integrate image vulnerability scanning in CI (Trivy or GitHub container scanning).
3. Implement `.github/workflows/deploy.yaml`:
   - Build and tag container images with commit SHA and semantic version.
   - Push to container registry.
   - Automatically deploy to staging environment upon successful merge to `main`.
   - Require explicit manual approval gate before promoting to production environment.
NON-GOALS: Production deployment is never fully automatic without human approval.
TESTS REQUIRED: Docker image build tests; image vulnerability scan tests; deployment pipeline syntax validation.
VERIFICATION:
```bash
docker build -f services/core/Dockerfile -t retrace-core:test .
docker build -f services/ai/Dockerfile -t retrace-ai:test .
docker build -f services/ingestion/Dockerfile -t retrace-ingestion:test .
docker build -f services/notifications/Dockerfile -t retrace-notifications:test .
docker build -f gateway/Dockerfile -t retrace-gateway:test .
```
Output: All container images build cleanly with minimal layer sizes and zero critical CVEs.
ACCEPTANCE CRITERIA:
- [ ] Images run as unprivileged non-root users.
- [ ] Staging deploys automatically upon merge.
- [ ] Production requires manual approval gate.
STOP AND ASK IF: Container registry credentials and Azure environment targets are provisioned.
HANDOFF OUTPUT: Production container images ready for Azure infrastructure deployment.
COMMIT AND PR: `ci: implement multi-stage dockerfiles image scanning and deployment gates`
PROGRESS ENTRY: `CU-20 | Merged | Production Dockerfiles, Trivy scans, staging CD workflow | None | Open`

---

### PHASE: CU-21 Azure Infrastructure as Code
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement Azure Infrastructure as Code (Bicep/Terraform per ADR) defining Container Apps environment, Key Vault, PostgreSQL, Redis, private endpoints, and Static Web Apps (Gate G6).
OWNER AGENT: Cursor
BRANCH: cu/21-azure-infrastructure
DEPENDS ON: CU-20
READ FIRST: System Design sections 7, 23.4, 26; Master Build Guide section 10 (R-21).
ALLOWED PATHS:
- `infra/azure/**`
- `docs/decisions/`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: Application code, gateway, web.
CONTRACTS TOUCHED: none
TASKS:
1. Author ADR resolving IaC tool choice (Bicep recommended for Azure native integration) per R-21 (NEEDS PRAVEEN).
2. Implement IaC modules for:
   - Resource Group and Virtual Network with private subnets.
   - Azure Container Apps Environment with internal ingress for services and external ingress for Gateway.
   - Azure Database for PostgreSQL Flexible Server with private endpoint.
   - Azure Cache for Redis with private endpoint.
   - Azure Key Vault with access policies / Azure RBAC for managed identities.
   - Azure Blob Storage account with private endpoints for exports and snapshots.
   - Azure Static Web Apps instance for frontend hosting.
3. Configure Managed Identities for each service granting least-privilege Key Vault and storage permissions.
NON-GOALS: Never commit real Azure subscription IDs, secrets, or keys into repository.
TESTS REQUIRED: IaC template syntax and lint validation (`az bicep build` or `terraform validate`).
VERIFICATION:
```bash
az bicep build --file infra/azure/main.bicep
```
Output: Bicep templates compile cleanly to ARM templates with zero syntax or lint errors.
ACCEPTANCE CRITERIA:
- [ ] Data stores reside in private network zone without public IP addresses.
- [ ] Each service uses its own Managed Identity with minimum necessary permissions.
- [ ] Single registrable domain configuration supports app and api subdomains.
STOP AND ASK IF: Praveen has confirmed Azure subscription readiness and IaC tool choice (R-21).
HANDOFF OUTPUT: Azure infrastructure deployable (Gate G6).
COMMIT AND PR: `feat(infra): implement azure infrastructure as code bicep templates`
PROGRESS ENTRY: `CU-21 | Merged | Azure Container Apps, Key Vault, private networking Bicep IaC | None | Open`

---

### PHASE: CU-22 Observability, Tracing, and Dashboards
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement OpenTelemetry distributed tracing across services, Azure Application Insights integration, structured health checks, and operational dashboards.
OWNER AGENT: Cursor
BRANCH: cu/22-observability-dashboards
DEPENDS ON: CU-21
READ FIRST: System Design sections 11, 24; Repository Conventions section 11.1.
ALLOWED PATHS:
- `infra/observability/**`
- `services/*/apps/health/**`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: Application business code.
CONTRACTS TOUCHED: none
TASKS:
1. Configure OpenTelemetry SDK in all services propagating `trace_id` from gateway `X-Request-ID`.
2. Configure Application Insights export for traces, metrics, and error exceptions.
3. Implement standardized health check endpoints `GET /health/live` and `GET /health/ready` in all services checking database connectivity and Redis availability.
4. Configure structured JSON logging ensuring logs carry `tenant_id`, `request_id`, and `job_id` while scrubbing evidence text and secrets.
5. Create dashboard definitions for service latency, error rates, queue depth, and model failure rates.
NON-GOALS: Traces and logs must never record evidence text, prompts, or provider credentials.
TESTS REQUIRED: Health check endpoint tests; log secret scrubbing tests; trace propagation integration tests.
VERIFICATION:
```bash
uv run pytest services/core/tests/test_health.py
uv run pytest services/ingestion/tests/test_health.py
uv run pytest services/ai/tests/test_health.py
uv run pytest services/notifications/tests/test_health.py
```
Output: Health endpoints return 200 with readiness details; logs scrub sensitive parameters.
ACCEPTANCE CRITERIA:
- [ ] Distributed trace IDs correlate requests across Gateway, Core, and Ingestion.
- [ ] Health check distinguishes liveness from readiness.
- [ ] Zero unredacted evidence or credentials emitted to logs.
STOP AND ASK IF: Application Insights sampling rate requires configuration.
HANDOFF OUTPUT: Observability suite active across all backend services.
COMMIT AND PR: `feat(infra): implement opentelemetry tracing health checks and monitoring`
PROGRESS ENTRY: `CU-22 | Merged | OpenTelemetry tracing, health checks, AppInsights dashboards | None | Open`

---

### PHASE: CU-23 Database Backups and Connection Pooling
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement per-tenant logical backups to Azure Blob Storage, retention cleanup, and PgBouncer connection pooling configuration (R-21).
OWNER AGENT: Cursor
BRANCH: cu/23-backups-pgbouncer
DEPENDS ON: CU-22
READ FIRST: System Design sections 4.4, 4.7, 26; Database Design section 10; Master Build Guide section 10 (R-21).
ALLOWED PATHS:
- `infra/backups/**`
- `infra/pgbouncer/**`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: Application business code.
CONTRACTS TOUCHED: none
TASKS:
1. Implement PgBouncer configuration and deployment container:
   - Configure transaction-level connection pooling.
   - Support dynamic per-tenant role authentication.
   - Configure connection limits and query timeouts preventing noisy-neighbor exhaustion.
2. Implement nightly logical backup script:
   - Read active tenants from `tenant_registry`.
   - Execute `pg_dump` per tenant database.
   - Encrypt backup archive with tenant data key.
   - Upload backup archive to Azure Blob Storage.
3. Implement backup retention lifecycle policy deleting backup files older than retention limit.
NON-GOALS: Do not bypass PostgreSQL database role checks in connection pooler.
TESTS REQUIRED: PgBouncer connection concurrency test; backup script execution test; backup restore verification test.
VERIFICATION:
```bash
# Verify PgBouncer configuration syntax
docker run --rm -v $(pwd)/infra/pgbouncer:/etc/pgbouncer edoburu/pgbouncer:latest pgbouncer -V
```
Output: PgBouncer config parses cleanly; backup script exports tenant schema.
ACCEPTANCE CRITERIA:
- [ ] PgBouncer pools connections without exhausting PostgreSQL server limits.
- [ ] Logical backups execute per tenant and upload encrypted archives to Blob storage.
- [ ] Backups older than retention period are pruned automatically.
STOP AND ASK IF: PgBouncer auth_file generation approach for dynamic roles (R-21).
HANDOFF OUTPUT: Database connection pooling and backup automation ready.
COMMIT AND PR: `feat(infra): implement pgbouncer pooling and per-tenant logical backups`
PROGRESS ENTRY: `CU-23 | Merged | PgBouncer pooling, nightly logical backups to blob storage | None | Open`

---

### PHASE: CU-24 Demo Seed Dataset and Kaggle Integration
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement demo data generator loading Kaggle incident records paired with synthetic Slack messages, commits, and deployments into a tenant marked `is_demo=true`.
OWNER AGENT: Cursor
BRANCH: cu/24-demo-seed-dataset
DEPENDS ON: CU-23
READ FIRST: PRD sections 13, 16; System Design section 24; Database Design section 2.
ALLOWED PATHS:
- `infra/demo_data/**`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: Application business code.
CONTRACTS TOUCHED: none
TASKS:
1. Author seed data generator loading incident tickets from public incident dataset.
2. Generate synthetic Slack incident channels, messages, alerts, and pull request deployments matching incident time windows to populate realistic timelines.
3. Mark generated organization with `is_demo=true` in `control.organizations`.
4. Ensure demo data never mixes with real tenant data and cannot be selected by non-demo organizations.
5. Create one-command demo tenant reset script `infra/demo_data/seed_demo.py`.
NON-GOALS: Demo data must not contain real customer tokens, credentials, or proprietary incident logs.
TESTS REQUIRED: Demo seed script execution test; `is_demo` flag validation test; cross-tenant query isolation test.
VERIFICATION:
```bash
uv run python infra/demo_data/seed_demo.py --tenant=demo-org
```
Output: Demo organization seeded with incidents, evidence items, and timeline events.
ACCEPTANCE CRITERIA:
- [ ] Demo tenant populated with realistic incident volume and timelines.
- [ ] All demo records tagged and isolated within demo tenant database.
- [ ] Seed script executes idempotently.
STOP AND ASK IF: Praveen has specified preferred Kaggle incident dataset (R-21).
HANDOFF OUTPUT: Demo environment ready for end-to-end evaluation and capstone presentation.
COMMIT AND PR: `feat(infra): implement kaggle demo dataset generator and seeding scripts`
PROGRESS ENTRY: `CU-24 | Merged | Demo dataset loader, synthetic messages, is_demo tenant flag | None | Open`

---

### PHASE: CU-25 End-to-End Integration Test Suite
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement end-to-end integration test suite in CI executing the complete core loop (describe, discover, confirm, draft, review, approve, export) against the full Docker Compose stack.
OWNER AGENT: Cursor
BRANCH: cu/25-integration-tests
DEPENDS ON: CU-24, CX-22 (Gate G4)
READ FIRST: Master Build Guide sections 9.4; PRD section 7; System Design section 24.
ALLOWED PATHS:
- `tests/e2e/**`
- `.github/workflows/e2e.yaml`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: Application business code.
CONTRACTS TOUCHED: none
TASKS:
1. Author E2E test harness spinning up Docker Compose stack with all active services in CI.
2. Implement automated end-to-end test flow:
   - Register user, create organization, wait for tenant provisioning.
   - Create incident from PagerDuty webhook.
   - Submit incident description; wait for evidence discovery.
   - Confirm evidence candidates; wait for timeline generation.
   - Request AI draft generation; verify postmortem version creation in Core.
   - Execute blameless check; accept finding.
   - Submit postmortem for review; approve postmortem as Admin.
   - Request PDF export and verify signed download URL.
3. Run two-tenant isolation checks during the live test run.
NON-GOALS: Do not mock internal service APIs during E2E integration test (test real service boundaries).
TESTS REQUIRED: Full loop E2E automated test against Compose stack.
VERIFICATION:
```bash
# Execute integration test runner in test container
pytest tests/e2e/test_core_loop.py
```
Output: Complete core loop passes from incident webhook to approved postmortem export.
ACCEPTANCE CRITERIA:
- [ ] End-to-end loop executes without manual intervention.
- [ ] All cross-service events and internal REST calls succeed.
- [ ] Zero cross-tenant data leaks during multi-tenant test run.
STOP AND ASK IF: Integration test execution time exceeds CI timeout limits.
HANDOFF OUTPUT: Integration environment validated (Gate G7 readiness).
COMMIT AND PR: `test(e2e): implement cross-service core loop integration test suite`
PROGRESS ENTRY: `CU-25 | Merged | Core-loop E2E integration test suite against compose stack | None | Open`

---

### PHASE: CU-26 Release Hardening, Rollback Runbooks, and Documentation
EFFORT: S (Est. review time: 25 mins)
GOAL: Execute failure injection tests (database outage, Redis crash, provider timeout), document service runbooks, and compile operational rollback documentation.
OWNER AGENT: Cursor
BRANCH: cu/26-release-hardening
DEPENDS ON: CU-25
READ FIRST: Master Build Guide section 11.2; Repository Conventions section 15; System Design section 26.
ALLOWED PATHS:
- `docs/**`
- `services/ingestion/README.md`
- `services/notifications/README.md`
- `gateway/README.md`
- `infra/README.md`
- `docs/progress/cursor.md`
FORBIDDEN PATHS: Application business code.
CONTRACTS TOUCHED: none
TASKS:
1. Conduct failure injection tests: simulate Redis crash (outbox holds unsent events and resumes on restart), simulate database disconnect (services fail safely with standard 500 error without exposing stack traces).
2. Author service READMEs for Ingestion, Notifications, Gateway, and Infrastructure detailing environment variables, health checks, operational commands, and contract ownership.
3. Author operational rollback runbook covering schema migration rollbacks, secret rotation procedures, and tenant recovery.
4. Finalize `docs/progress/cursor.md`.
NON-GOALS: Do not edit Codex or Antigravity owned documentation files.
TESTS REQUIRED: Failure recovery verification tests; documentation link checks.
VERIFICATION:
```bash
# Verify documentation references and links
uv run python -m doctest infra/README.md
```
Output: Runbooks and recovery procedures verified.
ACCEPTANCE CRITERIA:
- [ ] Failure recovery verified for broker and database outages.
- [ ] Service READMEs complete with local runbooks.
- [ ] All Cursor phases marked complete in progress file.
STOP AND ASK IF: Any production runbook procedure requires security review.
HANDOFF OUTPUT: Platform and integration services fully verified for release candidate (Gate G7).
COMMIT AND PR: `docs(platform): compile operational runbooks and failure recovery guides`
PROGRESS ENTRY: `CU-26 | Merged | Operational runbooks, failure injection testing, final sign-off | None | Done`
