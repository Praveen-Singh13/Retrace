# Implementation Plan: Antigravity (Frontend and Hallmark UI)

## Agent Role and Scope

Antigravity owns the entire frontend single-page application under `web/`, built with the already installed hallmark skill, React, Vite, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, and TipTap.

Owner: Antigravity
Paths owned:
- `web/` (including all components, features, hooks, styles, tests, and committed generated types in `web/src/generated/`)
- `docs/progress/antigravity.md` (progress tracking)
Forbidden paths:
- `services/**`
- `libs/**`
- `gateway/**`
- `infra/**`
- `contracts/**` (consumed via generated types only; changes requested via handoffs)
- `pyproject.toml`, `compose.yaml`

---

## Anti-Hallucination Rules

These rules are strictly binding on Antigravity throughout execution:

1. Hallmark skill required: Every phase begins with loading and following the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Documents win over memory. The Frontend Design and Workflow specification v1.0 is the visual and interaction contract. Only the endpoint inventory in API Contracts section 4 exists. Anything missing is a GAP.
3. No invented routes or fields: Generated API types under `web/src/generated/` are never hand-edited. If a field or endpoint is missing, use the documented fallback in Frontend section 9 (GAP register) and raise a handoff request.
4. Dark theme only: Use design tokens from Frontend section 2 strictly. Never invent colors or layout values.
5. Four mandatory states: Every data view (list, card, drawer, tab, panel) must implement loading (skeletons), empty, error (with retry and correlation id), and permission-denied.
6. Honest uncertainty: Hypotheses, open questions, timestamp discrepancies, and "verification unavailable" statuses are displayed plainly. Never display "verified" when semantic verification was unavailable.
7. Human decides: AI outputs are suggestions. The UI never applies or saves AI text without an explicit accept action by the user.
8. Traceable citations: Every citation chip must resolve to a timeline event. Never omit event links.
9. Secrets are write-only: Never display saved secrets or tokens in cleartext. Only show masked hints.
10. UI hiding is cosmetic: Role gating uses `can(capability)`. The UI gracefully handles 401, 403, 404, 412, 422, 429, and network errors from backend enforcement.
11. Small steps, full stops: Complete one phase at a time. Stop, summarize, paste real test output, and wait for Praveen to merge.
12. Ask in a structured way: Questions use: QUESTION, WHY IT BLOCKS, OPTIONS, DEFAULT I WOULD USE.

---

## Git and GitHub Protocol

1. Author identity: Every commit is authored and committed as Praveen. Before the first commit, verify `git config user.name` and `git config user.email`. Praveen's GitHub username is `Praveen-Singh13`.
2. Attribution removal: Remove all agent attribution: no `Co-authored-by` trailers, no "Generated with" lines, and no agent signatures in commit messages or PR text. Check `git log -1 --format='%an <%ae>%n%cn <%ce>%n%b'`.
3. Branching: Work exclusively on feature branches named `ag/<NN>-<slug>` (for example `ag/04-api-layer-mocks`). Never commit directly to `main`.
4. Commits: Use Conventional Commits (`type(scope): imperative summary`). Scope for Antigravity: `web`.
5. Pull requests: Rebase on latest `main` before opening PR. PR body includes problem summary, requirement IDs, affected screens/modules, test evidence, screenshots of all four mandatory states, and linked GAPs.

---

## Cross-Agent Handoff Protocol

1. Consumer protocol: Antigravity consumes OpenAPI contracts via `pnpm generate:api` and builds against Mock Service Worker (MSW) handlers until backend gates pass.
2. Handoff requests: If a required contract field, filter, or route is absent, Antigravity logs the GAP, implements the documented fallback, and writes `docs/handoffs/antigravity-to-<backend>-<NN>.md`. Antigravity never edits backend or contract files directly.
3. Cutover phases: After Gates G2, G3, G4, and G5 pass, Antigravity executes cutover phase AG-23, transitioning modules from MSW to the live gateway.

---

## Integration Gates Summary

| Gate | Name | Must be merged first | Unblocks |
| --- | --- | --- | --- |
| G0 | Repo exists | CX-00, CU-00 | Everything |
| G1 | Shared libs and contracts skeleton frozen | CX-01 to CX-05, CU-01, CU-02 | All service work, frontend API client |
| G2 | Identity and tenancy | CX-06 to CX-10, CU-17 | Ingestion tenant schema, frontend auth cutover |
| G3 | Incident and evidence contracts published | CX-11, CU-08 to CU-12 | AI pipeline integration, frontend timeline cutover |
| G4 | Draft loop | CX-18 to CX-23, CU-11, CU-12 | Frontend generation, editor, blameless cutover |
| G5 | Close the loop | CX-14 to CX-17, CU-14 to CU-16 | Frontend action items, analytics cutover |
| G6 | Deployable | CU-20 to CU-23, CX-25 | Demo hardening |
| G7 | Release candidate | CX-25, CX-26, CU-25, AG-25 | Demo |

---

## Antigravity Implementation Phases (AG-00 to AG-26)

### PHASE: AG-00 Preflight and Frontend Workspace Scaffold
EFFORT: S (Est. review time: 20 mins)
GOAL: Confirm hallmark skill availability, scaffold `web/` with Vite, React 18, TypeScript, pnpm, Tailwind CSS, and configure ESLint, Prettier, Vitest, and Playwright.
OWNER AGENT: Antigravity
BRANCH: ag/00-frontend-preflight
DEPENDS ON: CX-00, CU-00 (Gate G0)
READ FIRST: Frontend Spec sections 0, 3.1, 3.2; Repository Conventions sections 2, 6.
ALLOWED PATHS:
- `web/**`
- `pnpm-workspace.yaml`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All backend services, libs, gateway, infra, contracts.
CONTRACTS TOUCHED: none
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Scaffold `web/` application using Vite React TypeScript template with `pnpm`.
3. Configure `pnpm-workspace.yaml` including `web/`.
4. Install and configure Tailwind CSS 3.x and PostCSS.
5. Configure ESLint and Prettier matching repository rules.
6. Configure Vitest with React Testing Library and Playwright for cross-browser testing.
7. Create `docs/progress/antigravity.md` with phase tracking table.
NON-GOALS: Do not build UI components or screens yet.
TESTS REQUIRED: Build and lint tests: `pnpm --filter web build`, `pnpm --filter web lint`.
VERIFICATION:
```bash
pnpm --filter web lint
pnpm --filter web test:run
pnpm --filter web build
```
Output: Vite builds clean production bundle; ESLint passes; Vitest runs with zero errors.
ACCEPTANCE CRITERIA:
- [ ] Hallmark skill verified and confirmed to Praveen.
- [ ] `web/` builds with zero TypeScript or lint errors.
- [ ] Test harness configured for Vitest and Playwright.
STOP AND ASK IF: Hallmark skill is not loaded or active in environment.
HANDOFF OUTPUT: Frontend project scaffold ready for design tokens and components.
COMMIT AND PR: `chore(web): scaffold vite react typescript frontend workspace`
PROGRESS ENTRY: `AG-00 | Merged | Hallmark skill verified, web workspace scaffolded | None | Open`

---

### PHASE: AG-01 Design System Tokens and Theme Variables
EFFORT: S (Est. review time: 20 mins)
GOAL: Implement dark-theme CSS design tokens, typography rules, self-hosted font packages, elevation surfaces, and severity/claim color palettes.
OWNER AGENT: Antigravity
BRANCH: ag/01-design-tokens
DEPENDS ON: AG-00
READ FIRST: Frontend Spec sections 2.1 to 2.5.
ALLOWED PATHS:
- `web/src/styles/**`
- `web/package.json`
- `web/tailwind.config.js`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other directories.
CONTRACTS TOUCHED: none
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Install self-hosted font packages via `@fontsource`: `@fontsource/inter`, `@fontsource/source-serif-4`, `@fontsource/jetbrains-mono`.
3. Implement `web/src/styles/tokens.css` defining dark theme variables:
   - Surfaces: `--bg` (#0B0D10), `--surface-1` (#111418), `--surface-2` (#171B21), `--surface-3` (#1E232B).
   - Borders: `--border` (#232932), `--border-strong` (#2F3744).
   - Text: `--text` (#E6E9EE), `--text-muted` (#9AA3B0), `--text-faint` (#6B7480).
   - Accents and states: `--accent` (#7C8CFF), `--danger` (#F47067), `--warning` (#E3B341), `--success` (#56D364), `--info` (#58A6FF).
   - Incident severity colors: `--sev1` through `--sev4`.
   - AI claim kind colors and tag tokens: `observed_fact`, `causal_claim`, `hypothesis`, `open_question`, `author_context`, `process_recommendation`.
4. Configure `tailwind.config.js` mapping semantic colors, font families, and 4px spacing scale.
5. Set `color-scheme: dark` on `:root`.
NON-GOALS: Do not support light theme in v1 (dark theme only confirmed).
TESTS REQUIRED: Token compilation tests verifying CSS custom properties resolve in Tailwind classes.
VERIFICATION:
```bash
pnpm --filter web test:run
```
Output: CSS builds without errors; tokens mapped to Tailwind utility classes.
ACCEPTANCE CRITERIA:
- [ ] Dark theme variables match Frontend Spec section 2.2 exactly.
- [ ] Typography families (Inter, Source Serif 4, JetBrains Mono) configured without external Google Fonts requests.
- [ ] Contrast ratios meet minimum 4.5:1 for body and 3:1 for large elements.
STOP AND ASK IF: Additional token values are needed beyond specification.
HANDOFF OUTPUT: Design tokens ready for UI component library.
COMMIT AND PR: `feat(web): implement design system tokens and typography`
PROGRESS ENTRY: `AG-01 | Merged | CSS design tokens, dark theme variables, typography setup | None | Open`

---

### PHASE: AG-02 Shared Component Primitives and Domain Components
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement shadcn/ui primitive components and Retrace domain components: `SeverityBadge`, `StatusBadge`, `ClaimKindTag`, `CitationChip`, `TimestampLabel`, and `ConfirmDestructiveDialog`.
OWNER AGENT: Antigravity
BRANCH: ag/02-shared-components
DEPENDS ON: AG-01
READ FIRST: Frontend Spec sections 2.6, 2.7.
ALLOWED PATHS:
- `web/src/components/**`
- `web/src/lib/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: Feature modules, API layers.
CONTRACTS TOUCHED: none
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement shadcn/ui primitives themed with dark tokens: Button, Input, Textarea, Select, Combobox, Checkbox, Switch, Tabs, Tooltip, Popover, DropdownMenu, Dialog, AlertDialog, Sheet, Toast, Skeleton, Badge, Avatar, Kbd.
3. Implement `StatusBadge` mapping status kinds (`incident`, `postmortem`, `action`, `evidence`, `job`) to label, color, and icon in one central lookup.
4. Implement `SeverityBadge` rendering `sev1` to `sev4` with distinct labels and colors.
5. Implement `ClaimKindTag` with distinctive icons and colors (flask for hypothesis, check-circle for fact, link for causal, user for author context).
6. Implement `CitationChip` rendering compact claim event chips with click interaction.
7. Implement `TimestampLabel` consuming five timestamp fields: renders UTC mono when exact, shows precision hint, and displays warning icon when `timezone_known=false`.
8. Implement `ConfirmDestructiveDialog` requiring explicit action name confirmation or resource title typing for destructive operations.
9. Implement `SaveStatus` (Saving, Saved, Offline, Conflict).
NON-GOALS: Do not build full feature screens yet.
TESTS REQUIRED: Unit tests for `TimestampLabel` formatting with uncertain timezones; `StatusBadge` lookup tests; `ConfirmDestructiveDialog` typing confirmation test.
VERIFICATION:
```bash
pnpm --filter web test:run src/components
```
Output: 100% tests pass covering domain component props, accessibility attributes, and formatting.
ACCEPTANCE CRITERIA:
- [ ] `TimestampLabel` never formats date-only or uncertain time as exact UTC instant.
- [ ] `StatusBadge` pairs color with icon/text (never color alone).
- [ ] Primitives trap focus in dialogs and support keyboard navigation.
STOP AND ASK IF: Component accessibility fails axe-core checks.
HANDOFF OUTPUT: Component library ready for shell and application views.
COMMIT AND PR: `feat(web): implement shared primitives and domain components`
PROGRESS ENTRY: `AG-02 | Merged | Component primitives, StatusBadge, TimestampLabel, CitationChip | None | Open`

---

### PHASE: AG-03 App Shell, Routing, and Capability Guard
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement `AppShell`, collapsible 240px/64px sidebar, top bar, React Router routing skeleton, providers, and capability-based authorization map (`can()`).
OWNER AGENT: Antigravity
BRANCH: ag/03-shell-routing
DEPENDS ON: AG-02
READ FIRST: Frontend Spec sections 1.3, 3.3, 3.7, 5.1; System Design section 22.
ALLOWED PATHS:
- `web/src/app/**`
- `web/src/components/shell/**`
- `web/src/lib/permissions.ts`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: Feature implementation code.
CONTRACTS TOUCHED: none
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement React Router 6 configuration mapping all public routes and `/o/:org` tenant routes per Frontend section 3.3.
3. Implement `AppShell` with 240px sidebar collapsible to 64px icon rail, top bar (56px) with breadcrumbs, notification bell, user menu, and max-width 1280px content area.
4. Implement `OrgProvider` and `AuthProvider` contexts managing active tenant slug and session state.
5. Implement capability map in `lib/permissions.ts` and `can(capability)` hook gating UI actions for Admin and Member roles (Frontend 3.7).
6. Implement `RequireAuth`, `RequireOrg`, and `RequireCapability` route guards.
7. Support sidebar collapsed preference stored in `localStorage`.
NON-GOALS: Do not build live backend data calls yet (shell operates with mock state).
TESTS REQUIRED: Route navigation tests; sidebar collapse toggle test; capability map permissions test for Admin vs Member roles.
VERIFICATION:
```bash
pnpm --filter web test:run src/app
```
Output: Router navigates routes; guards redirect unauthenticated access; capability map enforces roles.
ACCEPTANCE CRITERIA:
- [ ] Admin nav items (Integrations, Members, AI settings, Audit log) hidden from Member role.
- [ ] Unknown route or tenant returns NotFound page.
- [ ] Sidebar collapses smoothly and respects `prefers-reduced-motion`.
STOP AND ASK IF: Route slug vs UUID mapping needs adjustments in context.
HANDOFF OUTPUT: App shell and route structure ready for API layer and feature screens.
COMMIT AND PR: `feat(web): implement app shell responsive routing and capability guards`
PROGRESS ENTRY: `AG-03 | Merged | AppShell layout, sidebar collapse, router skeleton, capability map | None | Open`

---

### PHASE: AG-04 API Client Layer, Type Generation, and MSW Mock Server
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement typed fetch wrapper in `api/client.ts` (handling auth headers, ETag, 36h Idempotency-Key, 412, 429, single-flight silent refresh), configure `pnpm generate:api`, and setup MSW mock server (Gate G1).
OWNER AGENT: Antigravity
BRANCH: ag/04-api-layer-mocks
DEPENDS ON: AG-03, CX-01, CU-02 (Gate G1)
READ FIRST: Frontend Spec sections 3.4, 3.4.1; Repository Conventions sections 6, 14.2; Master Build Guide section 9.3.
ALLOWED PATHS:
- `web/src/api/**`
- `web/src/generated/**`
- `web/src/test/**`
- `web/package.json`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: Backend code, contracts.
CONTRACTS TOUCHED: Generates types from `contracts/` into `web/src/generated/`.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Add script `pnpm generate:api` in `web/package.json` using `openapi-typescript` compiling all contract OpenAPI schemas into `web/src/generated/api.d.ts`.
3. Implement `web/src/api/client.ts`:
   - Inject `Authorization: Bearer <token>` from memory.
   - Inject active `org_id` into tenant route prefix `/api/v1/orgs/{org_id}/...`.
   - Single-flight silent refresh: on 401, call `POST /auth/refresh` once, replay concurrent pending calls; redirect to login if refresh fails.
   - Cache `ETag` and send `If-Match` on mutating requests.
   - Generate UUIDv7 `Idempotency-Key` on command intents.
   - Handle 412, 422, 429 (toast countdown with `Retry-After`), and 5xx errors.
4. Implement TanStack Query query keys structure in `api/queryKeys.ts`.
5. Implement Mock Service Worker (MSW) handlers generating mock fixtures matching generated contracts for all endpoints.
NON-GOALS: Do not hand-edit `web/src/generated/` files.
TESTS REQUIRED: API client tests: silent refresh single-flight replay; 412 error triggering; 429 toast handling; MSW mock interceptor tests.
VERIFICATION:
```bash
pnpm --filter web generate:api
git diff --exit-code web/src/generated
pnpm --filter web test:run src/api
```
Output: Type generation creates valid TypeScript definitions without uncommitted drift; client tests pass.
ACCEPTANCE CRITERIA:
- [ ] `pnpm generate:api` leaves no git diff in clean repository.
- [ ] Concurrent 401s trigger exactly one refresh call.
- [ ] MSW handlers provide complete offline mock server for all P0 endpoints.
STOP AND ASK IF: Type generator fails to resolve multi-file OpenAPI references.
HANDOFF OUTPUT: API layer and mock server ready. Unblocks feature development across all modules.
COMMIT AND PR: `feat(web): implement api fetch wrapper type generation and msw mocks`
PROGRESS ENTRY: `AG-04 | Merged | API client, silent refresh, ETag/idempotency, type generation, MSW | web/src/generated/* | Open`

---

### PHASE: AG-05 Module M01 Authentication and Account Screens
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement authentication screens S-01 through S-07: Login, Signup, Email Verification, Forgot Password, Reset Password, OAuth Callback, and User Profile.
OWNER AGENT: Antigravity
BRANCH: ag/05-module-m01-auth
DEPENDS ON: AG-04
READ FIRST: Frontend Spec M01 (screens S-01..S-07), section 5.8; PRD 8.1 AUTH-1..AUTH-4.
ALLOWED PATHS:
- `web/src/features/auth/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Auth OpenAPI contracts via generated types.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-01 Login: email/password form, "Continue with GitHub/Google" buttons, generic error on failure, lockout countdown on 429.
3. Implement S-02 Registration: name, email, password form, password strength hint, redirect to "Check your email" confirmation screen.
4. Implement S-03 Email Verification: read token from query, call verify endpoint, strip token from URL, display verification outcome.
5. Implement S-04 Forgot Password: email input, always show neutral confirmation copy without disclosing account existence.
6. Implement S-05 Reset Password: read token, accept new password with validation, redirect to login.
7. Implement S-06 OAuth Callback: transient progress screen exchanging state, refreshing session, redirecting to destination.
8. Implement S-07 Profile: display user details, memberships, and sign out button.
9. Implement session restore screen: full-screen branded loader during initial token check.
NON-GOALS: Do not build 2FA screens in v1 (P1).
TESTS REQUIRED: Form validation tests with Zod; generic login error test; single-flight session restore test; token stripping from URL test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/auth
```
Output: All authentication screens pass unit and interaction tests.
ACCEPTANCE CRITERIA:
- [ ] Login error never reveals whether email or password was incorrect.
- [ ] Verification tokens are stripped from browser history after read.
- [ ] Password reset confirmation never reveals email existence.
STOP AND ASK IF: OAuth provider start redirect requires specific popup vs window redirect.
HANDOFF OUTPUT: Authentication module complete (matches Gate G2).
COMMIT AND PR: `feat(web): implement m01 authentication and user profile screens`
PROGRESS ENTRY: `AG-05 | Merged | S-01 to S-07 Auth screens, login, signup, verification, profile | None | Open`

---

### PHASE: AG-06 Module M02 Organizations, Workspace, and Members
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement organization creation (S-08), `SettingUpScreen`, `OrgSwitcher`, general settings (S-42), members management (S-43), and invitations lifecycle (S-44).
OWNER AGENT: Antigravity
BRANCH: ag/06-module-m02-orgs
DEPENDS ON: AG-05
READ FIRST: Frontend Spec M02 (screens S-08, S-42..S-44), section 3.6; PRD 8.2 ORG-1..ORG-5.
ALLOWED PATHS:
- `web/src/features/orgs/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Orgs, Members, Invitations OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-08 Create Organization: name and slug inputs with validation, redirect to `SettingUpScreen`.
3. Implement `SettingUpScreen`: poll `GET /orgs/{org_id}` status, show friendly setup progress copy, navigate to dashboard when `status=active`.
4. Implement `OrgSwitcher`: list user memberships, handle org switch via `POST /auth/switch-org` (GAP-11), clear query cache for previous tenant, navigate to `/o/{slug}`.
5. Implement S-42 Organization Settings: edit name, stall days, escalation days, pre-due days, retention days with `If-Match`.
6. Implement S-43 Members Table: list members with snapshot names, role change dropdown (Admin/Member only), remove member with confirmation, enforce last-Admin protection.
7. Implement S-44 Invitations: invite by email with role, display pending invites, revoke invitation, accept invite page.
NON-GOALS: Do not build Teams or optional Manager/Viewer role toggles in v1.
TESTS REQUIRED: SettingUpScreen polling test; OrgSwitcher cache clearing test; last-Admin removal disabled test; invitation accept test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/orgs
```
Output: Organization creation, setup polling, org switching, and member role management pass tests.
ACCEPTANCE CRITERIA:
- [ ] Switching organizations clears previous tenant cache completely.
- [ ] Last active Admin cannot be demoted or removed (control disabled with tooltip).
- [ ] SettingUpScreen exits to dashboard when active.
STOP AND ASK IF: Invitation list route schema differs from GAP-08 fallback.
HANDOFF OUTPUT: Organization and tenancy UI complete.
COMMIT AND PR: `feat(web): implement m02 organizations switcher members and invitations`
PROGRESS ENTRY: `AG-06 | Merged | S-08, S-42 to S-44 Orgs, SettingUpScreen, OrgSwitcher, members | None | Open`

---

### PHASE: AG-07 Module M03 Dashboard
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement home dashboard (S-09) with four independent StatCards, recent incidents table, postmortems awaiting review list, stalled action items, and onboarding checklist.
OWNER AGENT: Antigravity
BRANCH: ag/07-module-m03-dashboard
DEPENDS ON: AG-06
READ FIRST: Frontend Spec M03 (screen S-09); PRD 8.13 DSH-2.
ALLOWED PATHS:
- `web/src/features/dashboard/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Dashboard and Analytics OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement 12-column responsive dashboard grid.
3. Implement Row 1 StatCards: recovery times, incident volume, open action items, stalled count.
4. Implement Row 2: Recent Incidents (8 columns) and Postmortems Awaiting Review (4 columns).
5. Implement Row 3: Stalled Action Items (6 columns) and Open / Overdue Items (6 columns).
6. Implement onboarding checklist for newly provisioned workspaces (connect integrations, add service, create first incident).
7. Ensure each dashboard card loads independently with its own loading skeleton and error boundary.
NON-GOALS: Do not fail entire page if one analytics summary query fails.
TESTS REQUIRED: Dashboard rendering test under 2 seconds; independent card error state test; card click navigation tests.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/dashboard
```
Output: Dashboard renders cards with skeletons; empty states display onboarding checklist.
ACCEPTANCE CRITERIA:
- [ ] Every dashboard card has loading, empty, and error states.
- [ ] Clicking stat cards navigates to corresponding analytics view with preset filters.
- [ ] Renders under 2 seconds with skeletons then data.
STOP AND ASK IF: StatCard metric formula requires adjustment.
HANDOFF OUTPUT: Dashboard operational.
COMMIT AND PR: `feat(web): implement m03 dashboard and headline metric stat cards`
PROGRESS ENTRY: `AG-07 | Merged | S-09 Dashboard grid, StatCards, recent incidents, awaiting review | None | Open`

---

### PHASE: AG-08 Module M04 Incidents List and Detail Shell
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement incident list (S-10), create incident modal with description-only input (S-11), incident detail frame with next-step banner (S-12), and tabs navigation.
OWNER AGENT: Antigravity
BRANCH: ag/08-module-m04-incidents
DEPENDS ON: AG-07
READ FIRST: Frontend Spec M04 (screens S-10..S-12); PRD 8.5 INC-1..INC-4.
ALLOWED PATHS:
- `web/src/features/incidents/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Incidents OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-10 Incident List: table with severity, title, type, status, services, started time, owner; filter bar with URL state; page pagination.
3. Implement S-11 Create Incident Modal: single required text field (short description); optional fields for severity, type, services, and approximate window.
4. Implement S-12 Incident Detail Shell: title header (editable for author), SeverityBadge, StatusBadge, lifecycle timestamps, and tabs: Overview, Evidence, Timeline, Postmortem, Actions, Activity.
5. Implement next-step banner dynamically guiding author based on incident lifecycle state (Frontend 717-728).
6. Enforce validation: `resolved_at` cannot be earlier than `started_at`.
NON-GOALS: Do not build PagerDuty duplicate incident merge in v1 (P1).
TESTS REQUIRED: Description-only incident creation test; filter bar URL persistence test; next-step banner state mapping test; timestamp validation test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/incidents
```
Output: Incident list filters correctly; create incident submits with description only; banner guides loop.
ACCEPTANCE CRITERIA:
- [ ] Author can create incident filling only the short description.
- [ ] Next-step banner reflects incident state accurately.
- [ ] Filter and sort parameters persist in URL query string.
STOP AND ASK IF: Incident delete route status (GAP-09, keep control hidden until documented).
HANDOFF OUTPUT: Incident management UI ready for evidence and timeline tabs.
COMMIT AND PR: `feat(web): implement m04 incidents list create modal and detail shell`
PROGRESS ENTRY: `AG-08 | Merged | S-10 to S-12 Incident list, description-only create, next-step banner | None | Open`

---

### PHASE: AG-09 Module M05 Integrations and Allowlists
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement integrations settings page (S-37), integration detail view (S-38), and channel/repository source allowlists manager (S-39).
OWNER AGENT: Antigravity
BRANCH: ag/09-module-m05-integrations
DEPENDS ON: AG-08
READ FIRST: Frontend Spec M05 (screens S-37..S-39); PRD 8.3 INT-1..INT-5.
ALLOWED PATHS:
- `web/src/features/integrations/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Integrations OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-37 Integrations List: connection cards for Slack, PagerDuty, and GitHub with status badges, last sync time, and "Connect" buttons.
3. Implement S-38 Integration Details: display external account ID, granted scopes, health status, and disconnect button with destructive confirm.
4. Implement S-39 Source Allowlists: table of allowed Slack channels and GitHub repositories, add allowlist entry dialog, toggle private channel with warning modal.
5. Ensure integration tokens and secrets are never displayed or queried by UI.
NON-GOALS: Do not build automated source discovery outside allowlists.
TESTS REQUIRED: Integration connection card rendering test; allowlist add/remove test; private channel warning dialog test; Admin-only capability gating test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/integrations
```
Output: Integrations cards render; allowlist entries update; private channel warning triggers.
ACCEPTANCE CRITERIA:
- [ ] Members cannot access integration settings (PermissionDenied).
- [ ] Adding private channel displays explicit sensitivity warning.
- [ ] Stored credentials never rendered to browser.
STOP AND ASK IF: OAuth callback route parameters for Slack connect require customization.
HANDOFF OUTPUT: Integrations and allowlists UI complete.
COMMIT AND PR: `feat(web): implement m05 integrations and source allowlists management`
PROGRESS ENTRY: `AG-09 | Merged | S-37 to S-39 Integrations list, connection details, allowlists | None | Open`

---

### PHASE: AG-10 Module M06 Service Catalog
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement service catalog page (S-40), add/edit service modal (S-41), and service linking to allowlisted Slack channels, repos, and PagerDuty services.
OWNER AGENT: Antigravity
BRANCH: ag/10-module-m06-catalog
DEPENDS ON: AG-09
READ FIRST: Frontend Spec M06 (screens S-40, S-41); PRD 8.4 SVC-1..SVC-3.
ALLOWED PATHS:
- `web/src/features/services/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Services OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-40 Service Catalog: searchable list of services with owning team, linked channels, repos, and PagerDuty services; visible to all members.
3. Implement S-41 Add/Edit Service Modal: name, description, owning team inputs (Admin only).
4. Implement Service Links Manager: link service to allowlisted Slack channels, repositories, and PagerDuty services.
5. Validate that source selection draws only from active allowlists.
6. Display hint on services with zero links: "Add links to improve automatic evidence discovery."
NON-GOALS: Do not build automated link inference in v1 (P1).
TESTS REQUIRED: Catalog search filtering test; Admin write vs Member read-only capability test; allowlist resource selector validation test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/services
```
Output: Service catalog renders for all members; write controls restricted to Admin role.
ACCEPTANCE CRITERIA:
- [ ] Service catalog is readable by Members and editable only by Admins.
- [ ] Source links restrict selection to allowlist entries.
- [ ] Empty link warning banner displays when service has no linked sources.
STOP AND ASK IF: Service archiving vs deletion UI convention needs clarification.
HANDOFF OUTPUT: Service catalog UI ready to provide hints for evidence discovery.
COMMIT AND PR: `feat(web): implement m06 service catalog and allowlist source links`
PROGRESS ENTRY: `AG-10 | Merged | S-40, S-41 Service catalog, add/edit modal, allowlist links | None | Open`

---

### PHASE: AG-11 Modules M21 and M07 Jobs Progress and Evidence Discovery Preview
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement `JobProgress` and `useJob` hook (M21), evidence discovery tab (S-13), evidence preview with candidate scoring reasons, and include/exclude confirmation (S-14).
OWNER AGENT: Antigravity
BRANCH: ag/11-jobs-evidence-preview
DEPENDS ON: AG-10
READ FIRST: Frontend Spec M07, M21 (screens S-13, S-14); PRD 8.6 EVD-1..EVD-5.
ALLOWED PATHS:
- `web/src/features/evidence/**`
- `web/src/components/workflow/JobProgress.tsx`
- `web/src/hooks/useJob.ts`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Evidence and Jobs OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement `useJob(job_id)` hook polling `GET /jobs/{job_id}` starting at 2 seconds with exponential backoff to 10 seconds.
3. Implement `JobProgress` component showing status (`queued`, `running`, `succeeded`, `failed`), progress bar, user-safe error message, and Retry button.
4. Implement S-13 Evidence Tab: display discovery run status and time window.
5. Implement S-14 Evidence Preview: candidate cards grouped by source (Slack, PagerDuty, manual), showing relevance score (0-1), score reasons, and five timestamp fields via `TimestampLabel`.
6. Implement include/exclude checkbox toggling `PATCH /evidence/{id}` with immediate visual feedback.
7. Implement "Confirm evidence" button calling `POST /incidents/{id}/evidence/confirm` transitioning to Timeline tab.
NON-GOALS: Do not display raw unredacted payloads.
TESTS REQUIRED: `useJob` polling and retry test; candidate include/exclude toggle test; score reason popover test; snapshot warning banner test on toggle.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/evidence
```
Output: `useJob` tracks job states; evidence candidates toggle inclusion; confirmation advances workflow.
ACCEPTANCE CRITERIA:
- [ ] Candidates above threshold checked by default; reasons displayed on hover/expand.
- [ ] Toggling candidate updates inclusion and shows snapshot invalidation notice.
- [ ] `JobProgress` shows user-safe error and retry button on failure.
STOP AND ASK IF: SSE progress fallback vs polling behavior (GAP-03).
HANDOFF OUTPUT: Evidence discovery and preview ready for Timeline.
COMMIT AND PR: `feat(web): implement m21 useJob progress and m07 evidence preview`
PROGRESS ENTRY: `AG-11 | Merged | S-13, S-14 Evidence discovery preview, useJob polling, JobProgress | None | Open`

---

### PHASE: AG-12 Module M08 Incident Timeline
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement ordered incident timeline tab (S-15), event detail side panel (S-16), key moment badges, discrepancy warning flags, and manual event modal.
OWNER AGENT: Antigravity
BRANCH: ag/12-module-m08-timeline
DEPENDS ON: AG-11
READ FIRST: Frontend Spec M08 (screens S-15, S-16); PRD 8.6 EVD-4..EVD-9; System Design section 20.2.
ALLOWED PATHS:
- `web/src/features/timeline/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Timeline OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-15 Timeline View: chronological list of events with cursor pagination using `useInfiniteQuery`.
3. Render source icons (Slack, GitHub, PagerDuty, manual), summary text, and `TimestampLabel` with timezone indicator.
4. Render key moment markers: First symptom, Detection, Escalation, Mitigation, Resolution.
5. Render phase dividers: Detection, Diagnosis, Mitigation, Recovery.
6. Render `DiscrepancyFlag` when sources disagree on time, with expandable discrepancy explanation.
7. Implement S-16 Event Detail Panel: slides in from right, displays underlying evidence citations, actor, original link, and raw timestamp.
8. Implement Add/Edit Manual Event dialog (`POST /timeline-events/{id}`, GAP-14).
NON-GOALS: Timeline never hides conflicting timestamps.
TESTS REQUIRED: Cursor pagination stability test; discrepancy flag rendering test; manual event creation test; slide-over panel focus trap test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/timeline
```
Output: Timeline renders chronologically; key moments flagged; discrepancy flags visible; side panel opens.
ACCEPTANCE CRITERIA:
- [ ] Discrepant timestamps highlighted with explicit warning tag.
- [ ] Key moments and phases partitioned cleanly.
- [ ] Manual events marked with "Manual" badge and preserved.
STOP AND ASK IF: Timeline event create path schema differences (GAP-14).
HANDOFF OUTPUT: Timeline UI complete. Unblocks Postmortem generation and editor citations.
COMMIT AND PR: `feat(web): implement m08 timeline view discrepancy flags and event detail panel`
PROGRESS ENTRY: `AG-12 | Merged | S-15, S-16 Timeline cursor pagination, key moments, discrepancies | None | Open`

---

### PHASE: AG-13 Modules M09 and M20 AI Generation Progress and Settings
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement AI draft generation trigger and progress screen (S-18), clarification question cards (GAP-15), and AI model settings page (S-45) with connection test.
OWNER AGENT: Antigravity
BRANCH: ag/13-generation-ai-settings
DEPENDS ON: AG-12
READ FIRST: Frontend Spec M09, M20 (screens S-18, S-45); PRD 8.7 AI-3, AI-4; AI Pipeline Spec section 10.
ALLOWED PATHS:
- `web/src/features/generation/**`
- `web/src/features/ai-settings/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes AI model and generation OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-18 Generation Screen: "Generate postmortem" button triggering `POST /incidents/{id}/postmortem/generate`, showing `JobProgress` with stages progress bar.
3. Implement clarification question card rendering when generation returns open questions (GAP-15): display question, why it matters, and supported action choices.
4. Implement S-45 AI Model Settings (Admin only):
   - Model mode toggle: "Retrace default model" vs "Custom provider".
   - Custom provider fields: provider dropdown (Azure OpenAI, OpenAI, Anthropic), model name, endpoint URL, API key (write-only password input).
   - Display hosted model notice: "Evidence sent to a hosted model leaves your organization workspace."
   - "Test connection" button calling `POST /ai-model/test` with success/failure feedback.
5. Display daily usage limit warning banner when default model quota is reached.
NON-GOALS: Model API key is never rendered back in cleartext (only masked hint).
TESTS REQUIRED: Generation job progress polling test; clarification question response interaction test; model settings validation test; API key write-only masking test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/generation
pnpm --filter web test:run src/features/ai-settings
```
Output: Generation triggers job; clarification cards render; model settings validate and test.
ACCEPTANCE CRITERIA:
- [ ] Generation failure shows user-safe error with Retry button.
- [ ] Hosted model warning displayed plainly on settings page.
- [ ] Stored API key shows only masked hint.
STOP AND ASK IF: Clarification question submission route availability (GAP-15).
HANDOFF OUTPUT: Generation workflow and AI settings operational.
COMMIT AND PR: `feat(web): implement m09 draft generation progress and m20 ai model settings`
PROGRESS ENTRY: `AG-13 | Merged | S-18 Generation progress, clarification cards, S-45 AI model settings | None | Open`

---

### PHASE: AG-14 Module M10 Postmortem Editor Core
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement TipTap/ProseMirror postmortem editor (S-19), autosave with debounce, ETag concurrency, `SaveStatus` indicator, and `StaleVersionDialog` (412 handling).
OWNER AGENT: Antigravity
BRANCH: ag/14-editor-core
DEPENDS ON: AG-13
READ FIRST: Frontend Spec M10 (screen S-19), section 5.6; PRD 8.9 REV-1, 8.9a ED-1, ED-7; System Design section 22.
ALLOWED PATHS:
- `web/src/features/postmortem/editor/**`
- `web/src/hooks/useAutosave.ts`
- `web/src/components/workflow/SaveStatus.tsx`
- `web/src/components/workflow/StaleVersionDialog.tsx`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Postmortem `PUT` and `GET` OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Configure TipTap editor with ProseMirror schema storing document as JSON.
3. Editorial layout: centered column max 720px, Source Serif 4 body font, clean vertical rhythm.
4. Implement `useAutosave` hook debouncing changes (1.5 seconds) and calling `PUT /postmortems/{id}` with `If-Match: <ETag>`.
5. Implement `SaveStatus` indicator in top toolbar: `Saving...`, `Saved`, `Offline (Retry)`, `Conflict (Reload)`.
6. Handle 412 `stale_version` response: halt autosave, open `StaleVersionDialog` offering "Reload latest" and "Keep my copy" (copies local edits to clipboard).
7. Implement single-author edit locking: if document is `approved` or `published`, editor opens in read-only mode with "Approved. Reopen to make changes" banner.
NON-GOALS: Do not build Yjs real-time co-editing in v1 (single-author autosave confirmed).
TESTS REQUIRED: Autosave debounce test; ETag match and update test; 412 conflict modal test; read-only lock test on approved document.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/postmortem/editor
```
Output: Editor types smoothly, autosaves in background, detects 412 conflicts, locks when approved.
ACCEPTANCE CRITERIA:
- [ ] Autosave saves silently in background without manual save button.
- [ ] 412 conflict displays StaleVersionDialog without silently overwriting server data.
- [ ] Approved and published documents are strictly read-only.
STOP AND ASK IF: TipTap ProseMirror schema node extensions conflict with standard plugins.
HANDOFF OUTPUT: Core editor operational. Ready for citations, comments, and inline AI.
COMMIT AND PR: `feat(web): implement m10 tiptap postmortem editor autosave and concurrency`
PROGRESS ENTRY: `AG-14 | Merged | S-19 TipTap editor, autosave debounce, 412 stale handling, read-only lock | None | Open`

---

### PHASE: AG-15 Citations Node and Claim Kind Visual Hierarchy
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement TipTap custom `CitationNode`, `CitationPanel` side sheet (S-20), claim kind visual styling (facts, hypotheses, open questions), and section navigation.
OWNER AGENT: Antigravity
BRANCH: ag/15-citations-claim-kinds
DEPENDS ON: AG-14
READ FIRST: Frontend Spec M10 (screen S-20), section 2.2; PRD 8.7 AI-2; AI Pipeline Spec section 6.
ALLOWED PATHS:
- `web/src/features/postmortem/citations/**`
- `web/src/features/postmortem/editor/nodes/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: none
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement TipTap custom inline node `CitationNode` carrying `claimId`, `eventIds`, and `claimKind`.
3. Render `CitationChip` inside editor prose with distinctive claim kind styling:
   - `observed_fact`: solid citation badge.
   - `hypothesis`: amber dashed underline with "Hypothesis" tag.
   - `open_question`: purple italic text with "Open question" tag.
   - `author_context`: cyan left border with "Author context" tag.
4. Implement S-20 `CitationPanel`: slide-over from right (380px) opening on chip click, displaying source event summary, link, and timestamp.
5. Implement Section Navigation sidebar jumping to postmortem sections (Summary, Timeline, Root cause, etc.).
NON-GOALS: Never rely on color alone to differentiate claim kinds (always pair with icon and text label).
TESTS REQUIRED: CitationNode serialization to ProseMirror JSON; claim kind visual tag rendering test; CitationPanel slide-over open/close test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/postmortem/citations
```
Output: Citation chips render inside prose; click opens slide-over panel with event details.
ACCEPTANCE CRITERIA:
- [ ] Citations persist inside ProseMirror JSON document structure.
- [ ] Hypotheses and facts are visually distinct with tags and icons.
- [ ] Clicking a citation chip displays the linked timeline event in side panel.
STOP AND ASK IF: Multiple event IDs in single citation chip display formatting preference.
HANDOFF OUTPUT: Citation system integrated into postmortem editor.
COMMIT AND PR: `feat(web): implement citationnode claim kind styling and citation side panel`
PROGRESS ENTRY: `AG-15 | Merged | S-20 Custom CitationNode, CitationPanel, claim kind styling | None | Open`

---

### PHASE: AG-16 Inline AI Actions and Comment Threads
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement text selection `AIActionMenu`, SSE streaming suggestion diff view (S-21), TipTap `CommentMark`, and comments side panel (S-23).
OWNER AGENT: Antigravity
BRANCH: ag/16-inline-ai-comments
DEPENDS ON: AG-15
READ FIRST: Frontend Spec M10 (screens S-21, S-23); PRD 8.9 REV-3, 8.9a ED-2..ED-5; System Design section 22.
ALLOWED PATHS:
- `web/src/features/postmortem/inline-ai/**`
- `web/src/features/postmortem/comments/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Inline AI SSE endpoint and Comments API.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement `AIActionMenu` appearing on text selection with quick actions: "Make blameless", "Clearer", "Shorter", "Expand with evidence", and custom prompt input.
3. Implement SSE client connecting to `POST /postmortems/{id}/ai/edit` streaming suggested replacement text.
4. Implement `SuggestionDiff` component displaying old text struck through and new text highlighted with Accept and Reject buttons.
5. Suggestions are local state only; accepted text replaces document selection and triggers autosave; rejected text discards suggestion.
6. Implement TipTap `CommentMark` anchoring comment thread ID to text ranges.
7. Implement S-23 Comments Panel: list anchored threads, reply to thread, resolve thread.
NON-GOALS: AI suggestions are never auto-accepted or saved before explicit user accept.
TESTS REQUIRED: SSE streaming response parsing test; suggestion accept/reject document mutation test; comment mark anchoring test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/postmortem/inline-ai
pnpm --filter web test:run src/features/postmortem/comments
```
Output: Selection opens AI menu; streamed text renders diff; accept replaces text; comments attach to text.
ACCEPTANCE CRITERIA:
- [ ] Text selection triggers AI menu and streams response via SSE.
- [ ] Suggestions must be explicitly accepted or rejected.
- [ ] Comment marks stay anchored as surrounding text moves.
STOP AND ASK IF: SSE connection drops mid-stream (retry with error notice).
HANDOFF OUTPUT: Inline AI and comments integrated into postmortem editor.
COMMIT AND PR: `feat(web): implement inline ai sse suggestions and anchored comments panel`
PROGRESS ENTRY: `AG-16 | Merged | S-21 Inline AI SSE menu, SuggestionDiff, S-23 comments panel | None | Open`

---

### PHASE: AG-17 Module M11 Blameless Language Checker Panel
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement Blameless findings side panel (S-22), "Run blameless check" trigger, finding review cards with highlighted document anchors, and accept/edit/dismiss actions.
OWNER AGENT: Antigravity
BRANCH: ag/17-module-m11-blameless
DEPENDS ON: AG-16
READ FIRST: Frontend Spec M11 (screen S-22); PRD 8.8 BL-1..BL-4; AI Pipeline Spec section 12.
ALLOWED PATHS:
- `web/src/features/postmortem/blameless/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Blameless OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-22 Blameless Panel: slides in from right, displays open findings grouped by category (attribution, judgment, counterfactual, absolute).
3. Implement "Check language" button calling `POST /postmortems/{id}/blameless-check`.
4. Render finding cards: matched text, reason, suggested neutral rewrite, and actions: "Accept rewrite", "Edit", "Dismiss".
5. Clicking a finding scrolls editor to anchored sentence and highlights matched phrase.
6. "Accept rewrite" replaces sentence with neutral rewrite and marks finding resolved.
7. Track open findings count; display warning badge on review submission button if open findings remain.
NON-GOALS: Blameless check never forces automatic rewrites without author review.
TESTS REQUIRED: Finding anchor scroll test; rewrite accept text replacement test; dismiss finding test; review submit guard warning test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/postmortem/blameless
```
Output: Blameless panel lists findings; clicking finding scrolls editor; accept replaces sentence.
ACCEPTANCE CRITERIA:
- [ ] Finding highlights corresponding text range in editor.
- [ ] Accept rewrite replaces text cleanly and updates finding status.
- [ ] Blameless check runs on current document revision.
STOP AND ASK IF: Anchor resolution fails when underlying text was heavily modified (mark finding stale).
HANDOFF OUTPUT: Blameless check panel operational.
COMMIT AND PR: `feat(web): implement m11 blameless language checker panel and rewrites`
PROGRESS ENTRY: `AG-17 | Merged | S-22 Blameless findings panel, rewrite accept/dismiss actions | None | Open`

---

### PHASE: AG-18 Modules M12 and M13 Review, Approval, and Version History
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement review workspace (S-26), `ApprovalBar` (S-27), approval history (S-28), version history list (S-24), and side-by-side version comparison (S-25).
OWNER AGENT: Antigravity
BRANCH: ag/18-review-approval-versions
DEPENDS ON: AG-17
READ FIRST: Frontend Spec M12, M13 (screens S-24..S-28); PRD 8.9 REV-2..REV-7; System Design section 21.
ALLOWED PATHS:
- `web/src/features/postmortem/review/**`
- `web/src/features/postmortem/versions/**`
- `web/src/components/workflow/ApprovalBar.tsx`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Postmortem review state machine and versions OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-26 Review Workspace: status banner, review checklist indicators (impact stated, evidence cited, blameless check passed).
3. Implement `ApprovalBar`:
   - "Submit for review" button: disabled with tooltip if blameless check has not run on latest revision.
   - Admin action buttons: "Approve postmortem" and "Request changes" (requires note dialog).
   - Author-cannot-approve guard: if active user is postmortem author, Approve button is disabled with tooltip "You cannot approve your own postmortem." (REV-6).
   - "Publish" button: available to Admin once approved.
   - "Reopen" button: available on approved/published documents.
4. Implement S-28 Approval History Panel: list historical decisions with decider name, role, timestamp, and note.
5. Implement S-24 Version History: timeline of named version snapshots showing version number, trigger, author, and timestamp.
6. Implement S-25 Version Comparison: visual diff view between two selected versions highlighting additions and deletions.
NON-GOALS: Authors cannot approve their own postmortems under any circumstance.
TESTS REQUIRED: State machine button visibility tests per role; author approval disabled test; version comparison diff test; reopen action snapshot test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/postmortem/review
pnpm --filter web test:run src/features/postmortem/versions
```
Output: Review actions gate per role; author approval blocked; versions compare with visual diff.
ACCEPTANCE CRITERIA:
- [ ] Author is strictly blocked from approving own postmortem.
- [ ] Request changes requires non-empty note.
- [ ] Reopen takes snapshot and restores review state.
STOP AND ASK IF: Visual diff library choice needs bundle size optimization (`jsdiff` confirmed).
HANDOFF OUTPUT: Complete review, approval, and version comparison workflow operational.
COMMIT AND PR: `feat(web): implement m12 review approvals and m13 version history diff`
PROGRESS ENTRY: `AG-18 | Merged | S-24 to S-28 Review bar, author approval guard, version diff view | None | Open`

---

### PHASE: AG-19 Module M17 Exports and Postmortem Library
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement postmortem library (S-17), export options dialog (S-50), and export download progress modal (S-51) for PDF and Markdown formats.
OWNER AGENT: Antigravity
BRANCH: ag/19-module-m17-exports
DEPENDS ON: AG-18
READ FIRST: Frontend Spec M17 (screens S-17, S-50, S-51); PRD 8.10 EXP-1, EXP-2.
ALLOWED PATHS:
- `web/src/features/exports/**`
- `web/src/features/postmortem/library/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Exports OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-17 Postmortem Library: list of postmortems with search, service filter, and status pills (GAP-01 fallback using filtered incident query).
3. Implement S-50 Export Options Dialog: format selector (PDF or Markdown), include timeline toggle, version selector.
4. Implement S-51 Export Progress Modal: call `POST /postmortems/{id}/export`, track job with `useJob`, display download button with short-lived signed link on completion.
5. Render clean download failure notice if generation fails.
NON-GOALS: Do not build bulk export or audit-ready PDF bundle in v1 (P1/Later items).
TESTS REQUIRED: Library filter test; export modal submission test; signed download link redirect test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/exports
pnpm --filter web test:run src/features/postmortem/library
```
Output: Library lists postmortems; export dialog triggers job and provides download URL.
ACCEPTANCE CRITERIA:
- [ ] Exports support PDF and Markdown formats.
- [ ] Download triggers signed link download cleanly.
- [ ] Library filters by service and status.
STOP AND ASK IF: Postmortem library dedicated list endpoint availability (GAP-01).
HANDOFF OUTPUT: Exports and library operational.
COMMIT AND PR: `feat(web): implement m17 postmortem exports and s-17 postmortem library`
PROGRESS ENTRY: `AG-19 | Merged | S-17 Postmortem library, S-50/S-51 PDF/Markdown export modals | None | Open`

---

### PHASE: AG-20 Module M14 Action Items Tracking and Verification
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement action items board and list (S-29), create/edit modal (S-30), detail drawer (S-31), verification modal (S-32), and confirmation of AI-suggested items.
OWNER AGENT: Antigravity
BRANCH: ag/20-module-m14-actions
DEPENDS ON: AG-19
READ FIRST: Frontend Spec M14 (screens S-29..S-32); PRD 8.11 ACT-1..ACT-6.
ALLOWED PATHS:
- `web/src/features/actions/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Action Items OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-29 Action Items Board/List: tabbed between Kanban board and table list, with filters for owner, service, priority, and stalled flag.
3. Highlight stalled items with amber border and "Stalled" badge.
4. Implement S-30 Create/Edit Modal: title, description, owner selector, due date, priority, success criteria.
5. Implement AI-suggested confirmation banner: suggested items show "AI Suggestion" chip and require confirmed owner and due date before activation (ACT-2).
6. Implement S-31 Action Item Drawer: slides in from right, shows event history, drop reason input when dropped.
7. Implement S-32 Verification Modal: when marking Done, prompts for verification note and URL (ACT-9).
NON-GOALS: Do not build GitHub issue sync in v1 (P1).
TESTS REQUIRED: Stalled item visual highlighting test; AI suggestion confirmation test; verification note prompt test; drop reason requirement test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/actions
```
Output: Action items board renders columns; AI items confirm with owner/due date; verification prompts on Done.
ACCEPTANCE CRITERIA:
- [ ] AI-suggested action items require human confirmation of owner and due date.
- [ ] Marking status Done prompts for verification note.
- [ ] Dropping an item requires non-empty drop reason.
STOP AND ASK IF: Kanban drag-and-drop library choice (`@hello-pangea/dnd` or native).
HANDOFF OUTPUT: Action items tracking UI operational.
COMMIT AND PR: `feat(web): implement m14 action items board drawer and verification`
PROGRESS ENTRY: `AG-20 | Merged | S-29 to S-32 Action items board, drawer, verification modal | None | Open`

---

### PHASE: AG-21 Modules M19 and M15 Notifications Center and Analytics
EFFORT: L (Est. review time: 35 mins)
GOAL: Implement notification bell popover and notification center (S-46), notification settings (S-47), and analytics views (S-33 to S-36: recovery times, volume, action health).
OWNER AGENT: Antigravity
BRANCH: ag/21-notifications-analytics
DEPENDS ON: AG-20
READ FIRST: Frontend Spec M15, M19 (screens S-33..S-36, S-46, S-47); PRD 8.11 ACT-5, 8.12 ANL-1, ANL-2, ANL-5.
ALLOWED PATHS:
- `web/src/features/notifications/**`
- `web/src/features/analytics/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Notifications and Analytics OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement TopBar notification bell with unread count badge and popover of recent items.
3. Implement S-46 Notification Center: full list with mark-as-read row actions and deep links to postmortems and action items.
4. Implement S-47 Notification Settings (under `/o/:org/account/notifications` per GAP-12): email and in-app toggles, notification type mute list.
5. Implement S-33 to S-36 Analytics Tabs:
   - Recovery Times (S-34): MTTD, MTTA, MTTM, MTTR trend line charts (Recharts) with date and severity filters.
   - Incident Volume (S-35): bar charts by service, severity, type over time.
   - Action Health (S-36): completion rate gauge, stalled count, average close time.
NON-GOALS: Do not build repeat-incident analytics in v1 (Later item).
TESTS REQUIRED: Unread notification badge count test; mark-read mutation test; analytics charts rendering with empty data test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/notifications
pnpm --filter web test:run src/features/analytics
```
Output: Notification bell updates; settings toggle; Recharts render analytics trends.
ACCEPTANCE CRITERIA:
- [ ] Notification deep links navigate directly to referenced postmortem or action item.
- [ ] Notification settings live under `account/notifications` accessible to all members.
- [ ] Analytics handle zero data with clean empty states.
STOP AND ASK IF: Chart animation causes performance issues on low-power devices.
HANDOFF OUTPUT: Notifications and Analytics UI complete (Gate G5 ready).
COMMIT AND PR: `feat(web): implement m19 notifications center and m15 analytics charts`
PROGRESS ENTRY: `AG-21 | Merged | S-46/S-47 Notifications center, S-33 to S-36 Analytics charts | None | Open`

---

### PHASE: AG-22 Module M18 Audit Log and Chain Verification View
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement admin audit log table (S-48) with cursor pagination and audit log hash chain verification side panel (S-49).
OWNER AGENT: Antigravity
BRANCH: ag/22-module-m18-audit
DEPENDS ON: AG-21
READ FIRST: Frontend Spec M18 (screens S-48, S-49); PRD 8.14 ADM-1, ADM-2; Database Design section 5 (`audit_log`).
ALLOWED PATHS:
- `web/src/features/audit/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: All other features.
CONTRACTS TOUCHED: Consumes Audit OpenAPI contracts.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement S-48 Audit Log Page (Admin only): table with sequence number (`seq`), timestamp, actor, action, entity, request ID; cursor pagination using `useInfiniteQuery`.
3. Implement expandable row details displaying safe audit metadata without exposing secrets.
4. Implement "Verify log integrity" button calling `GET /audit-log/verify`.
5. Implement S-49 Audit Verification Panel: slide-over displaying genesis verification status, verified sequence range, head hash, and tamper status badge (Valid or Tampered).
NON-GOALS: Audit log is strictly read-only; no edit or delete UI exists.
TESTS REQUIRED: Cursor pagination test; Admin-only capability gating test; verification outcome display test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/audit
```
Output: Audit log pages smoothly; verify action displays integrity status.
ACCEPTANCE CRITERIA:
- [ ] Audit log restricted to Admin capability.
- [ ] Verification shows sequence count and integrity state.
- [ ] Sensitive details (secrets, evidence text) absent from audit UI.
STOP AND ASK IF: Trace ID formatting differences in request_id field.
HANDOFF OUTPUT: Audit log interface operational.
COMMIT AND PR: `feat(web): implement m18 audit log table and hash chain verification panel`
PROGRESS ENTRY: `AG-22 | Merged | S-48 Audit log cursor table, S-49 chain verification panel | None | Open`

---

### PHASE: AG-23 Frontend Live Backend Cutover
EFFORT: L (Est. review time: 40 mins)
GOAL: Cut over application modules from MSW mock server to the live Traefik gateway and backend services across Gates G2 through G5, verifying contract alignment and raising handoffs for any drift.
OWNER AGENT: Antigravity
BRANCH: ag/23-backend-cutover
DEPENDS ON: AG-22, CX-10, CX-11, CX-22, CX-17, CU-02, CU-12
READ FIRST: Master Build Guide section 9.3; Repository Conventions section 14.1.
ALLOWED PATHS:
- `web/src/api/**`
- `web/src/test/**`
- `docs/handoffs/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: Backend services, gateway, contracts.
CONTRACTS TOUCHED: Regenerates `web/src/generated/` against live backend.
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Configure environment switch disabling MSW in live mode and pointing `VITE_API_BASE_URL` to local Traefik gateway (`http://api.localhost:8000`).
3. Run `pnpm generate:api` against running gateway and verify zero type regressions.
4. Test live authentication flow: register, login, refresh rotation, organization switch.
5. Test live incident creation, evidence preview, and timeline loading.
6. Test live AI generation, editor autosave, blameless findings, and approval.
7. If any contract drift or field mismatch is detected, do NOT edit backend files; log GAP and create handoff request in `docs/handoffs/antigravity-to-<backend>-<NN>.md`.
NON-GOALS: Never modify backend implementation files to bypass a frontend cutover error.
TESTS REQUIRED: Live API integration tests against Docker Compose stack.
VERIFICATION:
```bash
pnpm --filter web generate:api
git diff --exit-code web/src/generated
pnpm --filter web test:run
```
Output: Application runs cleanly against live gateway with zero MSW interceptors active.
ACCEPTANCE CRITERIA:
- [ ] All P0 modules function against real Compose backend.
- [ ] Silent refresh and ETag optimistic concurrency hold against real server.
- [ ] Any detected drift documented in handoff requests.
STOP AND ASK IF: Gateway CORS or cookie credentials block API requests.
HANDOFF OUTPUT: Frontend fully connected to live backend stack.
COMMIT AND PR: `chore(web): cut over api client from msw mocks to live gateway`
PROGRESS ENTRY: `AG-23 | Merged | Cutover to live gateway, contract drift verification, handoffs | None | Open`

---

### PHASE: AG-24 Accessibility, States, and Design Token Audit
EFFORT: M (Est. review time: 30 mins)
GOAL: Execute automated accessibility audit (Axe), verify all four mandatory states across every data view, and audit contrast tokens across the complete UI.
OWNER AGENT: Antigravity
BRANCH: ag/24-a11y-states-audit
DEPENDS ON: AG-23
READ FIRST: Frontend Spec sections 2.6, 5.2, 8.3.
ALLOWED PATHS:
- `web/src/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: Backend services, gateway, infra.
CONTRACTS TOUCHED: none
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Run `@axe-core/react` / `vitest-axe` checks on every screen and component.
3. Verify that all 22 data views implement all four mandatory states:
   - Loading skeletons matching target layout.
   - Empty state with primary next action button.
   - Error state with user-safe message, Retry button, and "Copy reference".
   - PermissionDenied view.
4. Verify keyboard focus order, focus rings (2px accent with 2px offset), and ARIA labels on all icon buttons.
5. Verify dialog focus traps and restore focus on close.
6. Verify status indicators always pair color with text or icon.
NON-GOALS: Do not skip accessibility issues on secondary screens.
TESTS REQUIRED: Automated axe accessibility test suite; states test suite for every data view.
VERIFICATION:
```bash
pnpm --filter web test:run src/test/a11y.test.tsx
```
Output: Zero axe accessibility violations; all four states verified across components.
ACCEPTANCE CRITERIA:
- [ ] Zero critical or serious accessibility violations.
- [ ] Every list, table, and panel has all four states tested.
- [ ] Keyboard navigation functions across entire incident-to-approval workflow.
STOP AND ASK IF: Any third-party component fails focus trap requirements.
HANDOFF OUTPUT: Frontend audited and compliant with Definition of Done.
COMMIT AND PR: `test(web): verify accessibility axe audit and four mandatory states`
PROGRESS ENTRY: `AG-24 | Merged | Axe accessibility audit, four mandatory states verification | None | Open`

---

### PHASE: AG-25 End-to-End Core Workflow Playwright Suite
EFFORT: L (Est. review time: 40 mins)
GOAL: Implement end-to-end Playwright test suite executing the complete core loop (WF-2: describe, discover, confirm, draft, review, approve, export) in a headless browser against the Compose stack.
OWNER AGENT: Antigravity
BRANCH: ag/25-playwright-core-loop
DEPENDS ON: AG-24
READ FIRST: Frontend Spec section 7 (WF-2), section 8.4; PRD section 7.
ALLOWED PATHS:
- `web/tests/**`
- `web/playwright.config.ts`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: Backend services, gateway, infra.
CONTRACTS TOUCHED: none
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement Playwright test for workflow WF-2:
   - Sign in as Admin.
   - Navigate to Incidents, open New Incident modal.
   - Enter short description and submit.
   - Verify transition to Evidence preview; toggle candidate inclusion.
   - Confirm evidence; verify timeline generates.
   - Trigger draft generation; wait for completion banner.
   - Open editor, verify ProseMirror JSON loads with citation chips.
   - Run blameless check; accept suggested rewrite.
   - Verify autosave indicator shows "Saved".
   - Submit for review; approve postmortem as Admin.
   - Trigger PDF export; verify download link.
3. Capture screenshots of key milestones for PR evidence.
NON-GOALS: Do not test non-critical secondary flows in Playwright (Vitest handles component coverage).
TESTS REQUIRED: Playwright E2E test run against local Compose stack.
VERIFICATION:
```bash
pnpm --filter web test:e2e
```
Output: Playwright WF-2 core loop passes completely from sign-in to export.
ACCEPTANCE CRITERIA:
- [ ] Automated browser completes incident-to-export loop without error.
- [ ] Citations and blameless panels interact cleanly.
- [ ] Screenshots captured for PR documentation.
STOP AND ASK IF: Browser flakiness occurs during background job polling.
HANDOFF OUTPUT: Complete frontend validated for release candidate (Gate G7).
COMMIT AND PR: `test(web): implement playwright end-to-end core loop test suite`
PROGRESS ENTRY: `AG-25 | Merged | Playwright E2E WF-2 core loop test suite | None | Open`

---

### PHASE: AG-26 P1 Enhancements (Optional Command Palette and Saved Filters)
EFFORT: M (Est. review time: 30 mins)
GOAL: Implement optional P1 enhancements: Cmd+K command palette for fast navigation (S-52) and saved filters popover (S-53) if schedule allows.
OWNER AGENT: Antigravity
BRANCH: ag/26-p1-command-palette
DEPENDS ON: AG-25
READ FIRST: Frontend Spec M16 (screens S-52, S-53); PRD 8.13 DSH-3, DSH-4.
ALLOWED PATHS:
- `web/src/features/search/**`
- `web/src/components/navigation/**`
- `docs/progress/antigravity.md`
FORBIDDEN PATHS: Backend services, gateway, infra.
CONTRACTS TOUCHED: none
TASKS:
1. Load and follow the hallmark skill. Confirm to Praveen that it is available before writing any UI. If it is not available, stop and ask.
2. Implement Cmd+K command palette modal using `cmdk` library:
   - Fast navigation to recent incidents, postmortems, action items, and settings pages.
   - Keyboard shortcut hints (Kbd primitive).
   - Navigation only (no full-text backend search in v1 per GAP-18).
3. Implement saved filters popover on incident list allowing local storage of filter presets.
4. Mark phase as optional enhancement in documentation.
NON-GOALS: Do not build backend full-text search engine in v1.
TESTS REQUIRED: Command palette keyboard shortcut (Cmd+K / Ctrl+K) test; navigation item selection test.
VERIFICATION:
```bash
pnpm --filter web test:run src/features/search
```
Output: Command palette opens with keyboard shortcut and navigates accurately.
ACCEPTANCE CRITERIA:
- [ ] Cmd+K opens palette; Escape closes.
- [ ] Arrow navigation and Enter select destinations smoothly.
- [ ] Phase is strictly additive and non-blocking for v1 release.
STOP AND ASK IF: Bundle size impact of command palette exceeds budget.
HANDOFF OUTPUT: Frontend implementation complete for final release candidate (Gate G7).
COMMIT AND PR: `feat(web): implement optional command palette navigation and saved filters`
PROGRESS ENTRY: `AG-26 | Merged | S-52 Command palette navigation, S-53 saved filter presets | None | Done`
