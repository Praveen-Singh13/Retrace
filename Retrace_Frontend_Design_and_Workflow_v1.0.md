# Retrace: Frontend Design and Workflow Specification

**Version:** 1.0 | **Date:** 10 November 2026 | **Status:** Implementation baseline for review
**Applies to:** `web/` (React SPA), its generated API types, and every coding-agent task that touches the frontend
**Visual direction:** Hybrid. Dense, calm dashboard shell around an editorial, writing-first postmortem editor. **Dark theme only in v1.**

---

## 0. How to use this document

This is one document with two jobs: (A) the **design** (how Retrace looks, what components exist, how the app is structured) and (B) the **workflow** (every screen, every control, where it leads, what it calls, what happens on success and failure). It is written so an implementation plan can be cut directly from it, one chapter or one screen at a time.

### 0.1 Reading order for humans and agents

1. Part 1 to 3: product frame, design system, app architecture. Read once, before any task.
2. Part 4: the screen index. Every screen has a stable ID (`S-01` to `S-69` matching the master inventory) and every module a stable ID (`M01` to `M21`).
3. Part 5: cross-cutting behavior. Every screen inherits it; module chapters do not repeat it.
4. Part 6: module chapters. Each one is self-contained and is the unit of an implementation task.
5. Part 7: end-to-end workflows and state machines.
6. Part 8: build plan, task template, definition of done.
7. Part 9: gaps and assumptions register. Read before touching anything marked **GAP**.

### 0.2 Stable identifiers (use these in task prompts, commits and PRs)

| Prefix | Meaning | Example |
| --- | --- | --- |
| `S-nn` | Screen or surface from the master inventory | `S-19` Postmortem editor |
| `Mnn` | Module chapter | `M10` Postmortem editor |
| `Mnn-Xm` | Interaction row in a module | `M12-X04` Approve button |
| `Mnn-ACk` | Acceptance criterion | `M10-AC07` |
| `WF-n` | End-to-end workflow | `WF-2` Incident to approved postmortem |
| `SM-n` | State machine | `SM-1` Postmortem |
| `GAP-n` | Missing contract detail that blocks or constrains frontend work | `GAP-04` |

### 0.3 Authority and labels

This document must not contradict the PRD v0.6, System Design, Database Design v0.1, AI Pipeline Spec v0.2, API and Event Contracts v1.0, or Repository Conventions v1.0. Where they disagree, use the reconciliation order in Repository Conventions section 1. Labels used here:

| Label | Meaning |
| --- | --- |
| **Fixed** | Decided in a source document. Implement as written. |
| **Design choice** | Decided in this document. Visual and interaction decisions only; changeable by editing this file. |
| **GAP** | A source document leaves the detail open. Do not invent it. Build against the documented fallback and record the gap in the PR. |
| **P0 / P1 / P2 / Later** | Priority from the PRD and master inventory. |

### 0.4 Non-negotiable frontend rules

1. **No invented endpoints, fields, numeric limits or provider behavior.** Only the endpoint inventory in API Contracts section 4 exists. Anything else is a GAP.
2. **UI hiding is cosmetic.** Every action also fails safely when the server returns 403 or 404.
3. **Every claim in a postmortem stays traceable.** A citation chip always resolves to a timeline event.
4. **AI output is a suggestion until a human accepts it.** The UI never writes AI text into a document without an explicit accept action.
5. **Facts, hypotheses and open questions are always visually distinct.** Never rely on color alone.
6. **A stored secret is never rendered back.** Only a masked hint.
7. **Tenant context is explicit.** Every tenant request carries the active `org_id` from the route.
8. **Never display "verified" when semantic verification was unavailable.**
9. **Generated API types in `web/src/generated/` are never hand-edited.**

---

# PART 1. PRODUCT FRAME FOR THE FRONTEND

## 1.1 What the user is trying to do

Retrace turns a resolved incident into a reviewed, blameless postmortem and tracked follow-up work. The frontend exists to make one loop feel short and trustworthy:

**Describe, Discover, Confirm evidence, Generate, Edit, Blameless check, Review, Approve, Publish, Track actions.**

The only required author input per incident is one short description. Everything else is discovered, inferred, or optional. Every screen decision below is judged against that.

## 1.2 Experience principles (Design choices)

| Principle | What it means on screen |
| --- | --- |
| **Evidence first** | Source, time and a link back to the original are always one click away from any statement. |
| **Quiet by default** | Dense data lives in the shell. The editor is calm: wide margins, serif body, no chrome until needed. |
| **Honest uncertainty** | Hypotheses, open questions, discrepancies and "verification unavailable" are shown plainly, never hidden. |
| **Human decides** | Every AI action ends in Accept or Reject. Every approval is an explicit button. |
| **Never lose work** | Autosave with visible status, conflict detection, retry on failed jobs, no silent overwrite. |
| **Progress is visible** | Every background job shows state, progress and a user-safe error with a retry. |

## 1.3 Roles in the UI

v1 builds **Admin** and **Member**. Manager and Viewer arrive later, so the UI is built around a **capability map**, not hard-coded role names (see 3.7). Adding a role later means editing one table.

| Role | v1 | UI summary |
| --- | --- | --- |
| Admin | Built | Everything, including members, integrations, AI model, audit log, approve, publish. |
| Member | Built | Create incidents, generate drafts, edit, comment, manage action items, view analytics, export. |
| Manager | Later | Manage catalog, approve. Until enabled, Admins approve. |
| Viewer | Later | Read published postmortems and analytics; comment only. |

## 1.4 Scope by phase (matches the 8-week plan)

| Phase | Weeks | Frontend deliverables |
| --- | --- | --- |
| 1. Foundation | 1 to 2 | Shell, auth screens, org creation and "setting up" screen, org switcher, invitations, members, incident list/create/detail shell. |
| 2. Core loop | 3 to 5 | Integrations, allowlists, service catalog, evidence preview, timeline, generation progress, editor with inline AI, citations and comments, blameless panel, review/approval, versions, PDF/Markdown export. Stretch: GitHub screens. |
| 3. Close the loop | 6 to 8 | Action items and reminders UI, notifications, analytics (recovery time, volume, action health), audit log, AI usage, polish, demo data views. |
| Later | After v1 | Real-time co-editing, repeat-incident UI, audit-ready reports, Manager/Viewer, teams, 2FA, org archive, share links, offline, voice. |

---

# PART 2. DESIGN SYSTEM (DARK ONLY)

All values are **Design choices**. They are expressed as CSS variables so a light theme can be added later without touching components. Set `color-scheme: dark` on `:root`.

## 2.1 Principles

- Dark surfaces layered by elevation, not by heavy borders.
- One accent color. Status and claim colors carry meaning; the accent carries action.
- Minimum body contrast 4.5:1, large text 3:1, focus rings always visible.
- Color is never the only signal: pair with an icon or text label.

## 2.2 Color tokens

| Token | Value | Use |
| --- | --- | --- |
| `--bg` | `#0B0D10` | App background |
| `--surface-1` | `#111418` | Cards, panels, sidebar |
| `--surface-2` | `#171B21` | Raised: popovers, menus, table header |
| `--surface-3` | `#1E232B` | Hover, selected row |
| `--border` | `#232932` | Default hairline |
| `--border-strong` | `#2F3744` | Inputs, focused containers |
| `--text` | `#E6E9EE` | Primary text |
| `--text-muted` | `#9AA3B0` | Secondary text |
| `--text-faint` | `#6B7480` | Placeholder, disabled |
| `--accent` | `#7C8CFF` | Primary buttons, links, focus ring, active nav |
| `--accent-hover` | `#95A2FF` | Hover |
| `--accent-soft` | `rgba(124,140,255,.14)` | Selected backgrounds |
| `--danger` | `#F47067` | Destructive, errors |
| `--warning` | `#E3B341` | Warnings, stalled |
| `--success` | `#56D364` | Success, done |
| `--info` | `#58A6FF` | Informational |

### Severity (incident)

| Severity | Token | Color | Label |
| --- | --- | --- | --- |
| sev1 | `--sev1` | `#F47067` | SEV1 (critical) |
| sev2 | `--sev2` | `#F0883E` | SEV2 (major) |
| sev3 | `--sev3` | `#E3B341` | SEV3 (minor) |
| sev4 | `--sev4` | `#8B949E` | SEV4 (low) |

### AI claim kinds (postmortem text and citation UI)

Each kind has a color, an icon and a text label. Hypotheses must never look like facts.

| Claim kind | Color | Icon | Text treatment in editor |
| --- | --- | --- | --- |
| `observed_fact` | `#56D364` | check-circle | Normal text, solid citation chips |
| `causal_claim` | `#58A6FF` | link | Normal text, chips plus a "causal" badge on hover |
| `hypothesis` | `#E3B341` | flask | Dashed underline, "Hypothesis" tag, amber chip |
| `open_question` | `#B392F0` | help-circle | Italic, "Open question" tag |
| `author_context` | `#76E3EA` | user | Cyan left rule, "Author context, not verified" tag |
| `process_recommendation` | `#9AA3B0` | lightbulb | Muted, "Proposal" tag |

## 2.3 Typography

Self-host fonts through `@fontsource` packages (no external font request).

| Role | Family | Fallback | Use |
| --- | --- | --- | --- |
| UI | Inter | system-ui, sans-serif | All shell UI |
| Editorial | Source Serif 4 | Georgia, serif | Postmortem editor body and exported-view reading mode |
| Mono | JetBrains Mono | ui-monospace, monospace | IDs, timestamps, code, evidence snippets |

| Style | Size / line | Weight |
| --- | --- | --- |
| Page title | 24 / 32 | 600 |
| Section title | 18 / 26 | 600 |
| Body (UI) | 14 / 22 | 400 |
| Small / meta | 12 / 18 | 400 |
| Editor body | 17 / 28 | 400 |
| Editor H1 / H2 | 30 / 38, 22 / 32 | 600 |

## 2.4 Spacing, radius, elevation, layout

- 4px base unit. Scale: 4, 8, 12, 16, 24, 32, 48, 64.
- Radius: 6 (inputs, chips), 10 (cards), 14 (dialogs). Full radius for avatars and pills.
- Elevation by surface step and a subtle border; shadow only on popovers and dialogs.
- Shell: left sidebar 240px (collapsible to 64px icon rail), top bar 56px, content max-width 1280px for dashboards.
- **Editor layout:** centered column max 720px, generous vertical rhythm, side panels slide over from the right (360 to 420px) and never reflow the column.
- Breakpoints: laptop 1024+ is the design target; tablet 768 to 1023 collapses sidebar to icon rail and side panels become overlays. Below 768 is out of scope (PRD: laptop and tablet).

## 2.5 Motion

150ms ease-out for hover and focus, 200ms for panel slide and dialog, 300ms max for anything else. Respect `prefers-reduced-motion` (remove sliding, keep opacity). Streaming AI text appears incrementally with no typing-animation flourish.

## 2.6 Accessibility (Fixed by PRD usability requirement, details are Design choices)

Keyboard navigation for all core flows, visible focus ring (2px accent, 2px offset), ARIA labels on icon-only buttons, dialogs trap focus and restore it on close, toasts use `aria-live="polite"`, errors use `role="alert"`, tables are real tables with headers, status is never color-only.

## 2.7 Component library

Built on shadcn/ui primitives, themed with the tokens above. Every component below is a shared component in `src/components/` unless it is feature-specific (then it lives in its feature folder).

| Group | Components |
| --- | --- |
| Primitives | Button (primary, secondary, ghost, danger, icon), Input, Textarea, Select, Combobox, Checkbox, Switch, RadioGroup, Tabs, Tooltip, Popover, DropdownMenu, Dialog, AlertDialog, Sheet (side panel), Toast, Skeleton, Badge, Avatar, Kbd |
| Data | DataTable (sort, filter row, cursor/page pagination), Pagination (page), CursorPager, FilterBar, SortMenu, EmptyState, ErrorState, PermissionDenied, StatCard, TrendChart (Recharts) |
| Domain | SeverityBadge, StatusBadge (incident, postmortem, action item, evidence, job), RoleBadge, SourceIcon (slack, github, pagerduty, manual), ClaimKindTag, CitationChip, TimestampLabel (with precision and timezone-unknown marker), DiscrepancyFlag, ConfidenceMeter, UserChip, ServiceChip |
| Workflow | JobProgress, StaleVersionDialog, ConfirmDestructiveDialog, ApprovalBar, SaveStatus, VerificationStatusBanner, LimitationsList |
| Editor | PostmortemEditor (TipTap), CitationNode, CommentMark, AIActionMenu, SuggestionDiff, SectionNav, BlamelessPanel, CommentPanel, CitationPanel |
| Shell | AppShell, Sidebar, TopBar, OrgSwitcher, NotificationBell, UserMenu, Breadcrumbs, SettingUpScreen |

### 2.7.1 Key component contracts

**StatusBadge** takes `kind` (`incident|postmortem|action|evidence|job|generation`) and `value`, and maps to label, color and icon in one lookup table. No screen builds its own badge.

**TimestampLabel** takes the five evidence timestamp fields (`occurred_at`, `occurred_at_raw`, `observed_at`, `timestamp_precision`, `timezone_known`). It renders:
- UTC value in mono when precise.
- Precision hint (for example "minute precision") when not exact.
- A warning icon with tooltip "Timezone not known" when `timezone_known` is false.
- It never formats a date-only value as an exact instant.

**CitationChip** takes a claim id, one or more timeline event ids and a claim kind. Click opens the CitationPanel on the first event; chips with several events show a count and open a list.

**JobProgress** takes a `job_id`, polls `GET /jobs/{job_id}` (start 2s, back off), later upgrades to SSE (GAP-03). It renders queued/running/succeeded/failed/cancelled, progress percent as an indeterminate-friendly bar (never infer hidden AI stages from the integer), user-safe error, and a Retry button where retry is allowed.

**ConfirmDestructiveDialog** requires an explicit confirm button labeled with the action ("Delete incident"). For org deletion and incident deletion, also requires typing the resource name.

**SaveStatus** states: `Saving...`, `Saved`, `Offline or failed (Retry)`, `Conflict (Reload)`.

---

# PART 3. APPLICATION ARCHITECTURE

## 3.1 Stack (Fixed)

React + Vite + TypeScript, Tailwind CSS, shadcn/ui, React Router, TanStack Query, TipTap (ProseMirror JSON), typed client generated from OpenAPI, pnpm, ESLint + Prettier, Vitest + React Testing Library + Playwright. Hosted on Azure Static Web Apps, calling the gateway on the `api` subdomain.

Additional libraries (Design choices, all optional to swap): Recharts (charts), React Hook Form + Zod (forms), `diff` or `jsdiff` (version compare), `date-fns` (dates, UTC display), `lucide-react` (icons), `cmdk` (command palette and search, P1).

## 3.2 Folder structure (Fixed shape, Design-choice contents)

```
web/src/
  app/                      # bootstrap, router, providers, guards
    router.tsx
    providers.tsx           # QueryClient, Auth, Org, Toast, Theme
    guards/                 # RequireAuth, RequireOrg, RequireCapability
  features/
    auth/                   # M01
    orgs/                   # M02 (orgs, members, invitations, switcher)
    dashboard/              # M03
    incidents/              # M04
    integrations/           # M05
    services/               # M06
    evidence/               # M07
    timeline/               # M08
    generation/             # M09
    postmortem/             # M10, M11, M12, M13 (editor, blameless, review, versions)
    actions/                # M14
    analytics/              # M15
    search/                 # M16
    exports/                # M17
    audit/                  # M18
    notifications/          # M19
    ai-settings/            # M20
  components/               # shared presentational components (2.7)
  api/                      # handwritten query/mutation functions + client wiring
    client.ts               # fetch wrapper: auth, org, ETag, Idempotency-Key, errors
    queryKeys.ts
    <service>/*.ts          # core, ingestion, ai, notifications
  generated/                # committed generated types (never hand-edit)
  hooks/                    # useJob, useAutosave, useCapability, useOrg, useDebounce
  lib/                      # dates, ids, errors, permissions, format
  styles/                   # tokens.css, globals
  test/                     # fixtures, MSW handlers, render helpers
```

Rule: code is promoted from a feature to `components/` or `hooks/` only when a genuine second consumer exists.

## 3.3 Route map

All authenticated, tenant routes live under `/o/:org`. `:org` is the organization id (UUIDv7) or its slug resolved to the id by the org context (**Design choice:** use the slug in the URL, keep the id in context; every API call uses the id).

| Route | Screen(s) | Guard |
| --- | --- | --- |
| `/login`, `/signup` | S-01, S-02 | Public (redirect if signed in) |
| `/verify-email` | S-03 | Public (token in query) |
| `/forgot-password`, `/reset-password` | S-04, S-05 | Public |
| `/auth/callback/:provider` | S-06 | Public (OAuth return) |
| `/accept-invite` | Invitation acceptance | Public, then auth |
| `/orgs/new` | S-08 | Auth |
| `/o/:org` | S-09 Dashboard | Auth + org |
| `/o/:org/incidents` | S-10 | Auth + org |
| `/o/:org/incidents/new` | S-11 (modal route over list) | Auth + org, can `incident.create` |
| `/o/:org/incidents/:id` | S-12 Overview tab | Auth + org |
| `/o/:org/incidents/:id/evidence` | S-13, S-14 | Auth + org |
| `/o/:org/incidents/:id/timeline` | S-15, S-16 | Auth + org |
| `/o/:org/incidents/:id/postmortem` | S-18 to S-23, S-26, S-27 | Auth + org |
| `/o/:org/incidents/:id/postmortem/versions` | S-24 | Auth + org |
| `/o/:org/incidents/:id/postmortem/versions/compare?a=&b=` | S-25 | Auth + org |
| `/o/:org/incidents/:id/actions` | Incident action items | Auth + org |
| `/o/:org/incidents/:id/activity` | Incident activity | Auth + org |
| `/o/:org/postmortems` | S-17 Library | Auth + org |
| `/o/:org/actions` | S-29 | Auth + org |
| `/o/:org/actions/:itemId` | S-31 (drawer route) | Auth + org |
| `/o/:org/analytics` (+ `/recovery`, `/volume`, `/action-health`) | S-33 to S-36 | Auth + org |
| `/o/:org/notifications` | S-46 | Auth + org |
| `/o/:org/account/profile` | S-07 | Auth |
| `/o/:org/account/notifications` | S-47 | Auth |
| `/o/:org/settings/general` | S-42 | Admin |
| `/o/:org/settings/members` (+ invitations tab) | S-43, S-44 | Admin |
| `/o/:org/settings/integrations` (+ `/:id`, `/:id/allowlist`) | S-37 to S-39 | Admin |
| `/o/:org/settings/services` | S-40, S-41 | Admin write, members read (see M06) |
| `/o/:org/settings/ai-model` | S-45 | Admin |
| `/o/:org/settings/audit-log` (+ `/verify`) | S-48, S-49 | Admin |
| `/o/:org/search` | S-52 (P1) | Auth + org |

**Deviation note:** the System Design lists notification settings under `settings/*` (Admin). Because notification preferences are per user (`GET/PATCH /notification-settings`), this document places them under `account/` so Members can reach them. Flagged as **GAP-12** for confirmation.

Unknown tenant resource id returns the not-found screen (never a "forbidden" that discloses existence). An `:org` the user is not a member of renders the same not-found screen.

## 3.4 API client layer

One fetch wrapper in `api/client.ts`. Handwritten functions per endpoint call it; generated types provide request/response shapes.

| Concern | Behavior |
| --- | --- |
| Base URL | Gateway at the `api` subdomain, path prefix `/api/v1`. Tenant calls: `/api/v1/orgs/{org_id}/...`. |
| Auth | `Authorization: Bearer <access token>` held in memory only. Refresh token is an HttpOnly cookie; send `credentials: "include"` to `/auth/refresh`. |
| Silent refresh | On 401, call `POST /auth/refresh` once (single-flight: concurrent 401s share one refresh), replay the request. If refresh fails, clear session and go to `/login?next=...`. |
| Org binding | Active org comes from the route `:org`. The access token carries the active org; switching org requires a token for that org (see M02, GAP-11). |
| ETag | Store the `ETag` response header with the cached resource. Send `If-Match` on PUT/PATCH/DELETE for mutable important resources. Never construct an ETag. |
| Idempotency | For create/command POSTs, generate one UUID per user intent and send it as `Idempotency-Key`; reuse the same key on automatic retry of that intent; new key for a new intent. |
| Errors | Parse the standard error shape `{ code, message, details?, correlation_id }` into a typed `ApiError`. Map `code` to user text in `lib/errors.ts`. Always keep `correlation_id` for the "Copy reference" affordance. |
| 202 jobs | Commands returning `202 { job_id, status }` hand off to `useJob(job_id)`. |
| 429 | Read `Retry-After`; show a toast with the wait and disable the triggering control until then. |
| Pagination | Cursor lists (timeline, audit, activity) use `useInfiniteQuery` with `cursor` + `limit`. Page lists (incidents, actions, services, notifications, library) use `page` + `page_size`. Page-size defaults are a **GAP** (CFG-01): read from a single frontend config constant until resolved. |
| Filter and sort | Query params named from resource fields (`status`, `severity`, `service_id`, `owner_user_id`, `created_at_gte`, `created_at_lte`); `sort=-field,field`. Unlisted fields are never sent. |

### 3.4.1 Error code to UI behavior

| Status / code | UI behavior |
| --- | --- |
| 401 | Silent refresh, else redirect to login with `next`. |
| 403 | Inline PermissionDenied for the action; toast "You do not have permission". |
| 404 | NotFound screen for pages; for background fetches, EmptyState. |
| 409 | Toast with specific message from `code` (state conflict). Refetch the resource. |
| 412 `stale_version` | StaleVersionDialog (see 5.6). |
| 422 | Map `details` field errors onto form fields. |
| 429 | Toast with Retry-After countdown; control disabled. |
| 5xx / network | ErrorState with Retry and "Copy reference" (correlation id). |

## 3.5 State management

| State type | Where it lives |
| --- | --- |
| Server state | TanStack Query. Query keys in `api/queryKeys.ts`, always prefixed by `[orgId, resource, ...]`. |
| Session and active org | Small React context (`AuthProvider`, `OrgProvider`). Access token in memory only. |
| URL state | Filters, sort, page, cursor, selected tab, selected item (so views are shareable and back-button safe). |
| Form state | React Hook Form + Zod, per form. |
| Editor state | TipTap/ProseMirror document, local until autosaved. |
| Ephemeral UI | Component state (open panels, dialogs). |

**Invalidation rules:** a mutation invalidates the narrowest affected keys. Generation success invalidates `[orgId, postmortem, incidentId]`, versions, and blameless findings. Evidence include/exclude invalidates evidence list, timeline, and marks the generation as "needs regeneration" (see M07).

## 3.5.1 Events and the frontend

The browser does **not** consume Redis Streams events. Backend events (for example `draft.ready`, `timeline.ready`, `postmortem.approved`) surface in the UI through job status, SSE, notifications and refetching. This table is the translation layer.

| Backend event | How the UI learns of it | UI reaction |
| --- | --- | --- |
| `incident.reported` | Incident appears in list on refetch or notification | Incident shows "Resolved, awaiting description" banner |
| `incident.description_submitted` | Command returned 202 + job | Evidence tab shows discovery JobProgress |
| `evidence.ready` | Discovery job succeeded | Evidence tab shows preview, awaiting confirmation |
| `timeline.ready` | Timeline job succeeded after evidence confirm | Timeline tab populates; "Generate postmortem" enabled |
| `draft.requested` | Command returned 202 + job | Generation progress screen |
| `draft.ready` | Generation job succeeded; notification | Postmortem tab shows new named version; blameless result shown |
| `postmortem.submitted` | Command response | Status badge changes; reviewer notification |
| `postmortem.approved` | Command response; notification | Editor locks (read-only), approval history updates |
| `tenant.provisioned` | Poll `GET /orgs/{org_id}` status | SettingUpScreen exits to workspace |
| `incident.deleted` | Command response | Redirect to incident list; related caches dropped |
| `audit.recorded` | Audit log refetch | None directly |

---

## 3.6 Auth, session and tenant context

1. On load, call `POST /auth/refresh`. Success restores a session; failure shows login.
2. `GET /me` returns the user and memberships. `OrgProvider` resolves `:org` against memberships; no match renders NotFound.
3. Org switching (OrgSwitcher) requests a token for the chosen org through Core (GAP-11 for the exact call), clears all query caches for the previous org, and navigates to `/o/{newOrg}`.
4. Critical actions (role change, approve, delete) may re-check current role through Core; the UI treats a 403 here as "your permissions changed", refetches `/me`, and shows PermissionDenied.
5. Sign out calls `POST /auth/logout`, clears memory state and all caches, redirects to `/login`.

## 3.7 Capability map (role gating)

Components ask `can(capability)`; they never check role names. One table in `lib/permissions.ts` maps role to capabilities. Derived from the PRD permission matrix.

| Capability | Admin | Member | Manager (later) | Viewer (later) |
| --- | --- | --- | --- | --- |
| `members.manage` | Yes | No | No | No |
| `integrations.manage`, `aiModel.manage`, `audit.view` | Yes | No | No | No |
| `services.manage` | Yes | No | Yes | No |
| `services.view` | Yes | Yes | Yes | Yes |
| `incident.create`, `draft.generate` | Yes | Yes | Yes | No |
| `postmortem.edit` | Yes | Yes | Yes | No |
| `postmortem.comment` | Yes | Yes | Yes | Yes |
| `postmortem.approve`, `postmortem.publish` | Yes | No | Yes (approve) | No |
| `actions.manage` | Yes | Yes | Yes | No |
| `analytics.view`, `export.create`, `postmortem.view` | Yes | Yes | Yes | Yes |

Disabled-with-reason beats hidden when the user can see the feature but a guard blocks it (for example "Submit" disabled with tooltip "Run the blameless check first"). Hidden is used only when the capability is never available to the role.

---

# PART 4. SCREEN INDEX

Every screen from the master inventory (S-01 to S-69). **Type** says how it is built: Page, Tab (inside a page), Panel (side sheet), Modal, Drawer, or Section. This resolves the inventory's note that the 69 screens are not 69 routes.

| Inv # | Screen | Route / surface | Type | Module | Priority | Roles |
| --- | --- | --- | --- | --- | --- | --- |
| S-01 | Login | `/login` | Page | M01 | P0 | Public |
| S-02 | Registration | `/signup` | Page | M01 | P0 | Public |
| S-03 | Email verification | `/verify-email` | Page | M01 | P0 | Public |
| S-04 | Forgot password | `/forgot-password` | Page | M01 | P0 | Public |
| S-05 | Reset password | `/reset-password` | Page | M01 | P0 | Public |
| S-06 | OAuth callback | `/auth/callback/:provider` | Page (transient) | M01 | P0 | Public |
| S-07 | User profile | `/o/:org/account/profile` | Page | M01 | P0 | Auth |
| S-08 | Create organization | `/orgs/new` | Page | M02 | P0 | Auth |
| S-09 | Dashboard | `/o/:org` | Page | M03 | P0 | All |
| S-10 | Incident list | `/o/:org/incidents` | Page | M04 | P0 | All |
| S-11 | Create incident | `/o/:org/incidents/new` | Modal | M04 | P0 | Admin, Member |
| S-12 | Incident overview | `/o/:org/incidents/:id` | Tab | M04 | P0 | All |
| S-13 | Evidence discovery | `.../:id/evidence` | Tab | M07 | P0 | All (write: Admin, Member) |
| S-14 | Evidence preview/review | `.../:id/evidence` | Section | M07 | P0 | Admin, Member |
| S-15 | Timeline | `.../:id/timeline` | Tab | M08 | P0 | All |
| S-16 | Timeline event details | Timeline | Panel | M08 | P0 | All |
| S-17 | Postmortem library | `/o/:org/postmortems` | Page | M10 | P0 | All |
| S-18 | AI generation progress | Postmortem tab | Section | M09 | P0 | Admin, Member |
| S-19 | Postmortem editor | `.../:id/postmortem` | Tab | M10 | P0 | All (edit: Admin, Member) |
| S-20 | Citation side panel | Editor | Panel | M10 | P0 | All |
| S-21 | AI suggestions panel | Editor | Panel/inline | M10 | P0 | Admin, Member |
| S-22 | Blameless findings | Editor | Panel | M11 | P0 | Admin, Member |
| S-23 | Comments panel | Editor | Panel | M10 | P0 | All |
| S-24 | Version history | `.../postmortem/versions` | Page/Panel | M13 | P0 | All |
| S-25 | Version comparison | `.../versions/compare` | Page | M13 | P0 | All |
| S-26 | Review workspace | Postmortem tab (review mode) | Section | M12 | P0 | All |
| S-27 | Approval screen | Postmortem tab ApprovalBar | Section/Modal | M12 | P0 | Admin |
| S-28 | Approval history | Postmortem tab | Panel | M12 | P0 | All |
| S-29 | Action item list | `/o/:org/actions` | Page | M14 | P0 | All |
| S-30 | Create/edit action item | Modal/Drawer | Modal | M14 | P0 | Admin, Member |
| S-31 | Action item details | `/o/:org/actions/:itemId` | Drawer | M14 | P0 | All |
| S-32 | Action item verification | Drawer step | Modal | M14 | P0 | Owner, Admin |
| S-33 | Analytics overview | `/o/:org/analytics` | Page | M15 | P0 | All |
| S-34 | Recovery-time analytics | `/o/:org/analytics/recovery` | Tab | M15 | P0 | All |
| S-35 | Incident-volume analytics | `/o/:org/analytics/volume` | Tab | M15 | P0 | All |
| S-36 | Action-health analytics | `/o/:org/analytics/action-health` | Tab | M15 | P0 | All |
| S-37 | Integrations | `/o/:org/settings/integrations` | Page | M05 | P0 | Admin |
| S-38 | Integration details | `.../integrations/:id` | Page | M05 | P0 | Admin |
| S-39 | Source allowlists | `.../integrations/:id/allowlist` | Tab | M05 | P0 | Admin |
| S-40 | Service catalog | `/o/:org/settings/services` | Page | M06 | P0 | Admin write, all read |
| S-41 | Add/edit service | Modal | Modal | M06 | P0 | Admin |
| S-42 | Organization settings | `/o/:org/settings/general` | Page | M02 | P0 | Admin |
| S-43 | Members | `/o/:org/settings/members` | Page | M02 | P0 | Admin |
| S-44 | Invitations | Members page tab | Tab | M02 | P0 | Admin |
| S-45 | AI model settings | `/o/:org/settings/ai-model` | Page | M20 | P0 | Admin |
| S-46 | Notification center | `/o/:org/notifications` | Page + popover | M19 | P0 | All |
| S-47 | Notification settings | `/o/:org/account/notifications` | Page | M19 | P0 | All |
| S-48 | Audit log | `/o/:org/settings/audit-log` | Page | M18 | P0 | Admin |
| S-49 | Audit verification | Audit log action | Panel | M18 | P0 | Admin |
| S-50 | Export options | Postmortem toolbar | Modal | M17 | P0 | All |
| S-51 | Export progress/download | Export modal step | Modal | M17 | P0 | All |
| S-52 | Global search | Command palette + `/o/:org/search` | Modal/Page | M16 | P1 | All |
| S-53 | Saved filters | Filter bar menu | Popover | M16 | P1 | All |
| S-54 | Bulk export | Library toolbar | Modal | M17 | P1 | All |
| S-55 | Recurring causes analytics | Analytics tab | Tab | M15 | P1 | All |
| S-56 | Postmortem timeliness analytics | Analytics tab | Tab | M15 | P1 | All |
| S-57 | Two-factor authentication | Profile section | Section | M01 | P1 | Auth |
| S-58 | Reviewer assignment | Review workspace | Popover | M12 | P1 | Admin, Member |
| S-59 | Suggestion mode | Editor mode | Mode | M10 | P1 | Admin, Member |
| S-60 | GitHub issue linking | Action item drawer | Section | M14 | P1 | Admin, Member |
| S-61 | Teams management | Settings | Page | M02 | P1 | Admin |
| S-62 | Repeat-incident detection | Incident overview card | Section | M15 | Later | Admin, Member |
| S-63 | Repeat-incident analytics | Analytics tab | Tab | M15 | Later | All |
| S-64 | Audit-ready reports | Export modal option | Modal | M17 | Later | All |
| S-65 | Organization data archive | Settings general | Section | M17 | P1 | Admin |
| S-66 | Shareable postmortem links | Export/share menu | Modal | M17 | P2 | All |
| S-67 | Real-time collaborative editor | Editor | Mode | M10 | Later | Admin, Member |
| S-68 | Offline editing | Editor | Mode | M10 | Later | Admin, Member |
| S-69 | Voice dictation | Editor toolbar | Control | M10 | Later | Admin, Member |

**Build rule:** P0 rows are the v1 build list. P1 rows are built only if the schedule allows and only after the P0 acceptance criteria pass. "Later" rows get no UI in v1 except the reserved hooks listed in the module chapters (for example, a disabled placeholder is **not** added; code structure just must not block them).

---

# PART 5. CROSS-CUTTING BEHAVIOR (EVERY SCREEN INHERITS THIS)

## 5.1 App shell

```
+----------------------------------------------------------------------------------+
| Sidebar 240px            | Top bar 56px: Breadcrumbs | Search(P1) | Bell | User     |
|  Retrace wordmark (home) |--------------------------------------------------------|
|  Org switcher            |                                                        |
|  Dashboard               |   Page content (max 1280px)                            |
|  Incidents               |                                                        |
|  Postmortems             |                                                        |
|  Action items            |                                                        |
|  Analytics               |                                                        |
|  ---- (Admin only) ----  |                                                        |
|  Integrations            |                                                        |
|  Services                |                                                        |
|  Members                 |                                                        |
|  AI settings             |                                                        |
|  Audit log               |                                                        |
+----------------------------------------------------------------------------------+
```

| Control | Action | Result |
| --- | --- | --- |
| Retrace wordmark | Click | Navigate `/o/:org` |
| Sidebar item | Click | Navigate; active item highlighted with accent |
| Sidebar collapse | Click | Toggle 240px / 64px rail; persisted in `localStorage` |
| OrgSwitcher | Click, choose org | Switch tenant context (M02), reload dashboard |
| OrgSwitcher "Create organization" | Click | Navigate `/orgs/new` |
| Notification bell | Click | Popover of latest notifications with "View all" to S-46; badge shows unread count |
| User menu | Click | Profile, Notification settings, Sign out, Sign out of all devices (GAP-06) |
| Breadcrumbs | Click segment | Navigate up |

Services appears under Admin settings for write and also needs a read-only entry for Members: **Design choice:** show "Services" in the main (non-admin) nav group for everyone, with write controls gated by `services.manage`.

## 5.2 Mandatory states on every data view

Every list, table, chart and panel implements all four:

| State | Rule |
| --- | --- |
| Loading | Skeletons matching the final layout. No full-page spinners except initial session restore. |
| Empty | EmptyState with one-sentence explanation and the primary next action button (for example "Create incident"). |
| Error | ErrorState with a message from the error map, a Retry button, and "Copy reference" for the correlation id. |
| Permission denied | PermissionDenied panel, never a blank screen. |

## 5.3 Forms

- Validation with Zod, errors shown inline under the field on blur and on submit; server 422 `details` map onto fields.
- Primary button shows a spinner and is disabled while submitting; double-submit is impossible.
- Success feedback: toast plus navigation or inline update.
- Unsaved changes in a modal or page prompt a confirm before closing.
- Secrets use write-only inputs (see 5.9).

## 5.4 Destructive actions

Always through ConfirmDestructiveDialog. Soft-deleted resources disappear from lists after success (response shape is GAP-07: handle both 204 and a resource body). Incident and organization deletion use type-to-confirm.

## 5.5 Asynchronous operations

Every 202 command follows this pattern:

1. Button shows pending; the response returns `job_id`.
2. A JobProgress component appears in place (not a separate page unless the module says so).
3. On `succeeded`: invalidate relevant queries, toast, move the user to the result.
4. On `failed`: show user-safe error, a Retry button when retryable, preserve prior data.
5. Leaving the page does not cancel the job. Returning shows the current job state (the job id is kept in the resource, or the latest job is looked up by `entity_id`; see GAP-03).

## 5.6 Optimistic concurrency and stale data

All mutable important resources carry an ETag. On **412 `stale_version`** show StaleVersionDialog:

- Title: "This changed while you were working."
- For the editor: options **Reload latest** and **Keep my copy** (copy local content to clipboard/scratch before reloading). Autosave stops until the user chooses.
- For forms and drawers: **Reload** discards local edits after confirming.

Never auto-retry a 412.

## 5.7 Rate limits and job errors

429 shows a toast with the wait time (from `Retry-After`) and disables the triggering control until it elapses. Failed jobs show the user-safe error and a `correlation_id` reference. Default-model daily limit reached (AI) shows a dedicated LimitReached message with a link to AI settings (Admin) or "Ask an admin to configure a model" (Member).

## 5.8 Session expiry

Silent refresh first. If refresh fails while editing, keep the editor content in memory, show "Session expired. Sign in again to save your work" in a non-dismissible banner, open a login dialog (not a full redirect) that on success replays the pending save. Full-page redirect only when no unsaved work exists.

## 5.9 Secrets

API keys and tokens are write-only. Input type is password-style with a "Replace" flow when a value exists. After save, show only the masked hint (for example last four characters). Never put secret values in query params, local storage, logs, error reports or toasts.

## 5.10 Timestamps and times

All stored times are UTC ISO 8601. Display in the organization's `timezone` setting when present (display-only per DB design), else browser local, always with a "UTC" toggle on evidence and timeline views. Use TimestampLabel for evidence and timeline; use plain relative time ("2h ago", with exact time in tooltip) for everything else.

## 5.11 Copy and tone

Neutral, plain language, no blame wording anywhere in the product UI. Error text says what happened and what to do next. No em-dashes in UI copy.

---

# PART 6. MODULE CHAPTERS

Each chapter uses the same template: **Purpose, Screens, Layout, Interactions table, States, Rules and edge cases, API dependencies, Acceptance criteria.** Interaction rows are written `control | trigger | action | result`. Endpoint paths are relative to `/api/v1/orgs/{org_id}` unless they begin `/api/v1`.

---

## M01. Authentication and account

**Purpose:** get a person into the product safely. **Phase:** 1. **Screens:** S-01 to S-07, S-57.

### Layout
Centered card (max 400px) on `--bg`, Retrace wordmark above, tagline "Hindsight, without the bias." below the form. No sidebar.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M01-X01 | Sign in form (email, password) | Submit | `POST /api/v1/auth/login` | Success: load `/me`; go to `next` or last org or `/orgs/new` if no memberships. Failure: inline "Email or password is incorrect". 429: lockout message with wait time. |
| M01-X02 | "Continue with GitHub" / "Continue with Google" | Click | Browser navigates `GET /api/v1/auth/oauth/{provider}/start` | Provider flow, returns to S-06 |
| M01-X03 | OAuth callback page | Load | `GET /api/v1/auth/oauth/{provider}/callback` (completed by browser redirect) then refresh session | Success: same routing as M01-X01. Failure: error message and link back to login. |
| M01-X04 | Sign up form (name, email, password) | Submit | `POST /api/v1/auth/register` | "Check your email" screen; no auto sign-in until verified |
| M01-X05 | Verify email page | Load with token | `POST /api/v1/auth/verify-email` | Success: "Email verified" and button to sign in. Expired or invalid token: message plus "Resend" (GAP-05) |
| M01-X06 | "Forgot password?" link | Click | Navigate S-04 | Email form |
| M01-X07 | Forgot password form | Submit | `POST /api/v1/auth/password-reset` | Always shows neutral "If an account exists, we sent instructions" (no account disclosure) |
| M01-X08 | Reset password form (new password) | Submit with token | `POST /api/v1/auth/password-reset` (confirm step, body is GAP-05) | Success: go to login with toast |
| M01-X09 | Profile page | Load | `GET /api/v1/me` | Shows name, email, active org, role, memberships |
| M01-X10 | "Sign out" | Click | `POST /api/v1/auth/logout` | Clear state, go to `/login` |
| M01-X11 | "Sign out of all devices" | Click, confirm | GAP-06 (no documented endpoint) | Hide the control until the endpoint exists |
| M01-X12 | Two-factor setup (P1) | Click | GAP (not in inventory) | Not built in v1 |

### States
Session restore shows a branded full-screen loader. Login errors never reveal which of email or password was wrong. Locked accounts show the 429/lockout message.

### Rules and edge cases
- Signed-in users visiting `/login` are redirected to their last org.
- `next` parameter is validated as a same-origin relative path before use.
- Password field shows strength hint; actual rules come from the server (422 details).
- Password reset and verify tokens are read from the query string then removed from the URL (`history.replaceState`).

### API dependencies
Auth endpoints and `GET /me` (Fixed inventory). Verify and reset body fields are open (API Contracts 4.1): **GAP-05**.

### Acceptance criteria
- [ ] M01-AC01 Valid login lands in the correct org; invalid login shows a generic error.
- [ ] M01-AC02 OAuth round trip works for GitHub and Google and handles failure.
- [ ] M01-AC03 Refresh on page reload restores the session without showing login.
- [ ] M01-AC04 Concurrent 401s trigger exactly one refresh call.
- [ ] M01-AC05 Password reset never discloses whether an email exists.
- [ ] M01-AC06 Access token is never written to storage.

---

## M02. Organizations, workspace and members

**Purpose:** create and manage the private workspace. **Phase:** 1. **Screens:** S-08, S-42, S-43, S-44, S-61 (P1).

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M02-X01 | Create organization form (name, slug) | Submit | `POST /api/v1/orgs` (Idempotency-Key) | Navigate to SettingUpScreen; creator becomes Admin |
| M02-X02 | SettingUpScreen | Load | Poll `GET /orgs/{org_id}` for `status` | `provisioning`: friendly progress copy. `active`: go to dashboard. `failed`: error with Admin "Retry" (provisioning retry endpoint is GAP-10) |
| M02-X03 | OrgSwitcher list | Choose org | Core token for that org (GAP-11), clear caches | Navigate `/o/{org}` |
| M02-X04 | Organization settings form (name, stall days, escalation days, retention) | Save | `PATCH /orgs/{org_id}`, `PATCH /orgs/{org_id}/settings` with `If-Match` | Toast, update cache. Fields shown: `stall_days`, `escalation_days`, `pre_due_days`, `evidence_retention_days`, `timezone` (DB design org_settings) |
| M02-X05 | Members table | Load | `GET /members` | Columns: name, email, role, status, joined. Row actions menu |
| M02-X06 | Change role (row menu) | Select role | `PATCH /members/{id}` | Toast; if it would remove the last Admin, server returns an error shown inline. Self-demotion shows a warning |
| M02-X07 | Remove member (row menu) | Confirm | `DELETE /members/{id}` | Row removed; copy states "Their authored content stays; access ends" |
| M02-X08 | "Invite member" dialog (email, role) | Submit | `POST /invitations` (Idempotency-Key) | Toast "Invitation sent"; appears in Invitations tab |
| M02-X09 | Invitations tab | Load | **GAP-08** (no documented list endpoint) | Build the tab shell; if no endpoint, show invites created this session and a note. Do not invent the route |
| M02-X10 | Revoke invitation | Confirm | `DELETE /invitations` (identifier shape GAP-08) | Row removed |
| M02-X11 | Accept invitation page | Load with token (signed in or sign in first) | `POST /invitations/accept` | Success: go to org. Expired or revoked: clear message and "Ask an admin to resend" |
| M02-X12 | Enable optional roles toggle | Click | Later (`enabled_optional_roles`) | Not built in v1; hide |
| M02-X13 | Delete organization (P1) | Type org name to confirm | GAP-09 (no documented route) | Hidden in v1 unless endpoint documented |
| M02-X14 | Teams (P1) | | No endpoint in inventory | Not built |

### Rules and edge cases
- Role selector in v1 offers Admin and Member only.
- The last active Admin cannot be demoted or removed (control disabled with tooltip, plus server enforcement).
- Org deletion, when built, shows the exact consequences: all incidents, evidence, drafts, comments and keys are permanently removed.
- Settings number fields enforce `> 0` for stall and escalation days (DB check).

### Acceptance criteria
- [ ] M02-AC01 New org shows SettingUpScreen until `active`, then lands on the dashboard.
- [ ] M02-AC02 Switching orgs clears the previous org's cached data and never shows stale tenant content.
- [ ] M02-AC03 Last-Admin protections are enforced in UI and handled when the server rejects.
- [ ] M02-AC04 Admin-only screens redirect Members to NotFound-safe PermissionDenied.

---

## M03. App shell navigation and Dashboard

**Purpose:** orient the user and surface what needs attention. **Phase:** 1 (shell) and 3 (metrics). **Screen:** S-09.

### Layout
A 12-column grid. Row 1: four StatCards (headline metrics). Row 2: "Recent incidents" (8 cols) and "Postmortems awaiting review" (4 cols). Row 3: "Stalled action items" (6 cols) and "Open and overdue action items" (6 cols).

### Interactions

| ID | Control | Action / API | Result |
| --- | --- | --- | --- |
| M03-X01 | "New incident" primary button (`incident.create`) | Open S-11 modal | |
| M03-X02 | Recent incidents row | Click | Navigate to incident overview |
| M03-X03 | Awaiting review row | Click | Navigate to that postmortem tab |
| M03-X04 | Stalled / overdue / open row | Click | Open action item drawer (S-31) |
| M03-X05 | StatCards | Click | Navigate to the matching analytics tab with filters preset |
| M03-X06 | "View all" links | Click | Incident list, library, action list |

Data sources: incidents list (`GET /incidents`, page 1 sorted `-started_at`), postmortems awaiting review (incidents list filtered by postmortem status, see GAP-01), action items (`GET /action-items` filtered), analytics summaries (`GET /analytics/*`). Headline metrics default to the latest period of `analytics_summaries`.

### States
Each card loads independently; one failing card shows its own ErrorState and does not break the page.

### Acceptance criteria
- [ ] M03-AC01 Dashboard renders under 2 seconds for typical data (PRD) with skeletons then data.
- [ ] M03-AC02 Every card has loading, empty and error states.
- [ ] M03-AC03 Members never see Admin-only nav items.

---

## M04. Incidents

**Purpose:** list, create, view and edit incidents; entry point of the core loop. **Phase:** 1. **Screens:** S-10, S-11, S-12.

### Incident list (S-10)
Table with columns: Severity, Title, Type, Status, Services, Started, Postmortem status, Owner/author. Filter bar: severity, status, service, type, date range. Sort menu. Page pagination. Row click opens the incident.

### Incident detail frame (S-12)
Header: title (editable inline for authors), SeverityBadge, StatusBadge, services chips, started/ended times, source (PagerDuty or manual). Below, tabs: **Overview, Evidence, Timeline, Postmortem, Actions, Activity**. A "next step" banner above the tabs guides the loop (table below).

| Incident state | Banner copy and primary action |
| --- | --- |
| Resolved, no description | "Tell Retrace what happened." Button: Add description |
| Description saved, discovery running | JobProgress "Finding evidence" |
| Evidence ready, unconfirmed | "Review the evidence we found." Button: Review evidence |
| Timeline ready, no postmortem | "Ready to draft." Button: Generate postmortem |
| Generating | JobProgress "Drafting postmortem" |
| Postmortem in progress | "Continue editing." Button: Open postmortem |
| Closed | "Postmortem published." |

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M04-X01 | Filter bar, sort | Change | `GET /incidents` with declared filters (URL state) | Table refetches; filters in URL |
| M04-X02 | "New incident" button | Click | Open S-11 | |
| M04-X03 | Create incident modal: required **short description**; optional severity, type, services, start/end | Submit | `POST /incidents` (Idempotency-Key) then `POST /incidents/{id}/description` | Navigate to the Evidence tab; discovery job starts (INC-3: description is the only required input) |
| M04-X04 | Description field (resolved PagerDuty incident) | Submit | `POST /incidents/{id}/description` | `202` job; banner changes |
| M04-X05 | Edit incident (title, type, severity, services, times, responders) | Save | `PATCH /incidents/{id}` with `If-Match` | Toast; 412 handled |
| M04-X06 | Incident source / lifecycle timestamps | View | From `GET /incidents/{id}` | Show detected, acknowledged, mitigated, resolved with TimestampLabel |
| M04-X07 | "Open postmortem" | Click | Navigate postmortem tab | |
| M04-X08 | Delete incident (menu, Admin) | Type title to confirm | GAP-09 (no documented DELETE) | Hidden until documented. Copy ready: "Deletes its evidence, drafts and comments" |
| M04-X09 | PagerDuty duplicates merge (P1) | | Not in inventory | Not built |

### Rules and edge cases
- Severity values `sev1` to `sev4`; type values `outage, performance, security, data, other`.
- Editing `resolved_at` earlier than `started_at` is blocked client-side (DB check) with an inline error.
- A manually created incident has no PagerDuty times: show "Approximate start and end" fields (evidence window input per System Design 20.1).
- Incident list for a service that is archived still shows its snapshot name.

### Acceptance criteria
- [ ] M04-AC01 An author can go from "New incident" to the evidence preview with one text field filled.
- [ ] M04-AC02 Filters, sort and page are in the URL and survive reload.
- [ ] M04-AC03 The next-step banner reflects each incident state in the table above.
- [ ] M04-AC04 A stale incident edit shows the stale dialog.

---

## M05. Integrations and source allowlists

**Purpose:** connect Slack, PagerDuty (and GitHub as stretch) and control exactly what the AI may read. **Phase:** 2. **Screens:** S-37, S-38, S-39.

### Layout
Integrations page: three provider cards (Slack, PagerDuty, GitHub) each showing status badge (active, error, revoked), account name, last sync, last error. GitHub card is marked "Stretch" in v1 and hidden if the feature flag is off (**Design choice:** feature flag `VITE_FEATURE_GITHUB`).

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M05-X01 | "Connect Slack" | Click | `POST /integrations/slack/connect` then redirect to provider OAuth | Return to `GET /integrations/slack/callback`, show success and go to allowlist step |
| M05-X02 | "Connect PagerDuty" | Click | `POST /integrations/pagerduty/connect` | Show connected state and the webhook setup instructions (webhook URL is `POST /webhooks/pagerduty/{token}`; display exactly what the API returns, nothing constructed client-side) |
| M05-X03 | "Connect GitHub" (stretch) | Click | `POST /integrations/github/connect` | App installation flow; same pattern |
| M05-X04 | Integration card | Click | Navigate details S-38 | Shows status, scopes, auth mode, connected by/at, health, masked hint where supported |
| M05-X05 | Allowlist tab | Load | `GET /integrations/{id}/allowlist` | Table of allowed channels or repos with name, private flag, added by |
| M05-X06 | Add or remove allowlist entries (searchable multi-select of channels or repos the provider exposes) | Save | `PUT /integrations/{id}/allowlist` (full replace) | Toast. Private channels require an extra confirm dialog |
| M05-X07 | "Disconnect" | Confirm | `DELETE /integrations/{id}` | Status revoked; copy: "Retrace stops reading immediately" |
| M05-X08 | "Use your own Slack app" (rate-limit workaround) | Expand advanced section | GAP-13 (field names not in contract) | Not built until contract defines credential fields |
| M05-X09 | Slack export upload fallback | | GAP-13 | Not built in v1 UI |
| M05-X10 | Time-window configuration | | Discovery window lives on the incident (M07), not here | No control on this screen |

### Rules and edge cases
- Allowlist default: public incident channels (System Design); the UI preselects none and recommends channels by name matching only if the API provides suggestions (otherwise no suggestions).
- Direct messages and private channels are off by default; adding a private channel shows an explicit warning.
- Hosted-model warning: any page where evidence flows to a model (AI settings) states plainly that evidence leaves the tenant when a hosted model is used.
- Integration `last_error` is user-safe text; show and offer Reconnect when status is `error`.

### Acceptance criteria
- [ ] M05-AC01 Slack and PagerDuty can be connected, listed, and disconnected.
- [ ] M05-AC02 Allowlist changes persist and require confirmation for private channels.
- [ ] M05-AC03 No token, key or secret is ever shown; only status and masked hint.
- [ ] M05-AC04 Admin-only: Members hitting these routes see PermissionDenied.

---

## M06. Service catalog

**Purpose:** link services to repos, channels and PagerDuty so discovery is accurate with no per-incident setup. **Phase:** 2. **Screens:** S-40, S-41.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M06-X01 | Services table | Load | `GET /services` | Name, owning team, description, link counts, archived toggle |
| M06-X02 | "Add service" | Click | Open S-41 modal | |
| M06-X03 | Service form (name, owning team, description) | Save | `POST /services` or `PATCH /services/{id}` | Toast; table updates |
| M06-X04 | Links editor (repos, channels, PagerDuty service, runbook URL) | Save | `PUT /services/{id}/links` | Only allowlisted sources are selectable (DB rule: links must exist in allowlist). Non-allowlisted source shows "Add to allowlist first" with a link to M05 |
| M06-X05 | Archive/delete service | Confirm | `DELETE /services/{id}` | Archived services stay for history but are not offered for new incidents |
| M06-X06 | Suggested links (P1) | | No contract | Not built |

### Rules
- Service name unique among non-archived services (inline 409/422 mapped).
- If a service has no links, show a hint: discovery will fall back to PagerDuty data and keyword search.
- Members see the table read-only.

### Acceptance criteria
- [ ] M06-AC01 Admin can add, edit, link and archive services.
- [ ] M06-AC02 Link pickers only list allowlisted resources.
- [ ] M06-AC03 Members see read-only view with no write controls.

---

## M07. Evidence discovery and preview

**Purpose:** show what Retrace found, let the author correct it quickly, and lock a snapshot for drafting. **Phase:** 2. **Screens:** S-13, S-14.

### Flow summary
Describe, discovery job runs (JobProgress), **Evidence preview** appears, author optionally includes/excludes/adds, **Confirm**, timeline builds.

### Layout (Evidence tab)
- Top: window card ("Window: 13:32 to 15:20 UTC", Edit link). Window is derived automatically (60 min before first alert to 30 min after resolution), visible and editable.
- Left (7 cols): evidence list grouped by source (PagerDuty, Slack, GitHub, Manual), each row: SourceIcon, kind, text preview (redacted), actor, TimestampLabel, ConfidenceMeter with "Why this score?" popover (reasons from `score_reasons`), include toggle.
- Right (5 cols): selected item detail: full redacted text, original link, redaction count, state.
- Footer bar: counts ("42 included, 18 excluded"), **Confirm evidence** primary button.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M07-X01 | Discovery progress | Automatic after description | JobProgress on the `discover_evidence` job | On success the preview loads |
| M07-X02 | Evidence list | Load | `GET /incidents/{id}/evidence` (page pagination, filter by source/state) | Rows by relevance |
| M07-X03 | Include/exclude toggle | Click | `PATCH /evidence/{id}` | Row updates; creates a new immutable evidence snapshot; any running AI job becomes stale; show inline notice "Evidence changed. Regenerate to use it." (API 9.3) |
| M07-X04 | "Add evidence" (paste link or text) | Submit | `POST /incidents/{id}/evidence` | Added as manual. Links to non Slack/GitHub/PagerDuty hosts are stored as notes and **not fetched**; show that explanation in the dialog |
| M07-X05 | "Edit window" | Save | Window change on the incident (field names GAP-01b) then re-run discovery | Re-runs discovery with a confirm |
| M07-X06 | "Confirm evidence" | Click | `POST /incidents/{id}/evidence/confirm` | `202` job `build_timeline`; navigate to Timeline tab when done |
| M07-X07 | "Open original" | Click | New tab to `url` | External link icon, `rel="noopener noreferrer"` |
| M07-X08 | Filter: source, included/excluded, failed | Change | Query params | List filters |
| M07-X09 | Failed collection list | View | `evidence` items with state `failed` | Show provider, reason, "Retry collection" (re-sync on demand is P1; button hidden in v1) |
| M07-X10 | Excluded history | Toggle "Show excluded" | Same list, state filter | Excluded stay visible, greyed, with one-click re-include |

### Rules and edge cases
- The preview step is **optional and takes seconds**: Confirm is always enabled once discovery succeeds.
- Excluded evidence must never reach generation; the UI makes the snapshot change explicit.
- Evidence text is already redacted; never attempt to un-redact. Show redaction count as a small badge.
- If discovery returns zero items, EmptyState: "We found no evidence in the allowed sources." Actions: add evidence manually, widen window, review allowlist (link to M05).
- If a source rate-limited, `stats` shows partial results: show a visible partial-collection banner with "Some sources were rate limited" (never hide).

### Acceptance criteria
- [ ] M07-AC01 Include/exclude updates immediately and shows the stale-generation notice.
- [ ] M07-AC02 Pasting an external link adds a note without any fetch.
- [ ] M07-AC03 Timestamps use TimestampLabel and never fake precision.
- [ ] M07-AC04 Partial or failed collection is visibly reported.

---

## M08. Timeline

**Purpose:** a single ordered, source-linked chronology with honest uncertainty. **Phase:** 2. **Screens:** S-15, S-16.

### Layout
Vertical timeline grouped by **phase** (Detection, Diagnosis, Mitigation, Recovery, Other) as collapsible sections. Each event row: time (TimestampLabel), SourceIcon(s), one-line summary, key-moment badge (first symptom, detection, escalation, mitigation, resolution), DiscrepancyFlag, "Manual" tag, hidden events dimmed. Clicking a row opens the event Panel (S-16) on the right.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M08-X01 | Timeline list | Load / scroll | `GET /incidents/{id}/timeline` cursor + limit | Infinite load; stable under inserts |
| M08-X02 | Filter by source, phase, key moment; "show hidden" | Change | Query params | Filtered list |
| M08-X03 | Event Panel | Click row | Local from loaded data | Summary, detail, sources, linked evidence (via `timeline_event_evidence`), timestamps (all five fields), confidence, discrepancy note |
| M08-X04 | "Open source" | Click | New tab to evidence URL | |
| M08-X05 | "Add event" | Submit form (time, summary, detail, key moment, phase) | `POST /timeline-events/{id}` per inventory (path shape GAP-14) | Added with Manual tag; survives timeline rebuild |
| M08-X06 | Edit event | Save | `PATCH /timeline-events/{id}` `If-Match` | Marked manual |
| M08-X07 | Hide event | Toggle | `PATCH /timeline-events/{id}` (`is_hidden`) | Dimmed; excluded from default view |
| M08-X08 | Delete event | Confirm | `DELETE /timeline-events/{id}` | Removed; confirm text explains citations may reference it |
| M08-X09 | Mark key moment | Menu | `PATCH` | Badge changes (P1 for editing; automatic detection is P0) |
| M08-X10 | Discrepancy flag | Hover / click | Local | Explains "Sources disagree on time by more than the configured gap" and shows both times |

### Rules and edge cases
- Order is server-determined (`sort_key`); the client never re-sorts.
- Hiding or deleting an event cited by a postmortem shows a warning listing affected sections (the citation will become unresolved; see M10 rule "unresolved citation").
- A date-only or timezone-unknown event shows its limitation, never an exact minute.
- After the timeline changes, the postmortem tab shows "Timeline changed since this draft" with a Regenerate suggestion.

### Acceptance criteria
- [ ] M08-AC01 Events appear in server order with phases and key moments.
- [ ] M08-AC02 Discrepancies and timestamp uncertainty are visible, not hidden.
- [ ] M08-AC03 Manual events are tagged and survive a rebuild.
- [ ] M08-AC04 Cursor paging does not duplicate or skip when events are added.

---

## M09. AI generation, progress and clarification

**Purpose:** start drafting, show honest progress, recover from failure, and collect clarifications. **Phase:** 2. **Screen:** S-18.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M09-X01 | "Generate postmortem" (`draft.generate`) | Click | `POST /incidents/{id}/postmortem/generate` (Idempotency-Key) | `202`; GenerationProgress replaces the empty state |
| M09-X02 | Usage guard | Click when limit reached | Server response (limit error) | LimitReached notice (see 5.7) |
| M09-X03 | GenerationProgress | Automatic | Poll `GET /jobs/{job_id}`; later SSE | Shows queued/running/succeeded/failed/**partial** (partial is an AI-specific outcome). Shows model name and prompt version when available |
| M09-X04 | Retry failed | Click | Re-issue generate with a new Idempotency-Key | Collected evidence is preserved (never re-collected) |
| M09-X05 | Retry partial | Click | Same | Reuses completed stages server-side |
| M09-X06 | Result summary | On success | Refetch postmortem | Shows: claims counts by kind, **limitations** list, validation status, **VerificationStatusBanner** |
| M09-X07 | VerificationStatusBanner | Render | From run metadata | If semantic verification unavailable: amber banner "Semantic verification unavailable. Deterministic checks passed." Never shown as a pass |
| M09-X08 | Clarification questions | Render | From generation result (field GAP-15) | Cards, each with why-it-matters, related event chips and four actions: **Provide context, Add evidence, Mark unresolved, Continue without answering** |
| M09-X09 | "Provide context" | Submit text | GAP-15 (endpoint for answers not in inventory) | Stored as author-provided context; rendered with `author_context` styling |
| M09-X10 | "Add evidence" | Click | Navigate to evidence tab add dialog (M07-X04) | New snapshot; dependent stages rerun |
| M09-X11 | Token usage and cost (P1) | View | From run metadata | Small meta line |

### Rules and edge cases
- Do not infer or display hidden AI stage names from a progress integer (API 6.2).
- While generation runs, editing is allowed only on a previously saved version; the new result arrives as a new version, never overwriting.
- If the evidence snapshot changes mid-run, show "This run is out of date" with Regenerate.
- Clarification is a pause for the **affected stage only**; the rest of the draft remains usable.

### Acceptance criteria
- [ ] M09-AC01 Generation shows progress and ends in success, partial or failed with correct UI.
- [ ] M09-AC02 Retry does not require re-collecting evidence.
- [ ] M09-AC03 Verification-unavailable is always displayed distinctly from passed.
- [ ] M09-AC04 Clarification answers appear as author context, never as verified facts.

---

## M10. Postmortem editor (core product screen)

**Purpose:** a calm, fast, evidence-linked writing workspace with built-in AI. **Phase:** 2. **Screens:** S-17, S-19, S-20, S-21, S-23, S-59 (P1), S-67 to S-69 (Later).

### Layout
```
+--------------------------------------------------------------------------------+
| Toolbar: status badge | version label | SaveStatus | Export | Versions | Review   |
+------------+-----------------------------------------------+-------------------+
| Section nav|     Centered 720px editorial column            | Right panel       |
| Summary    |     H1 title                                   | (Citations |      |
| Impact     |     Serif body 17/28, citation chips,          |  Comments |       |
| Timeline   |     claim-kind tags, inline comment marks      |  Blameless |      |
| Root cause |                                                | Suggestions)      |
| ...        |                                                |                   |
+------------+-----------------------------------------------+-------------------+
```
Left section nav (collapsible) lists the 11 sections and jumps to them. The right panel is a single tabbed sheet (Citations, Comments, Blameless, Suggestions) that slides over; the column never reflows. **Focus mode** hides nav, panel and toolbar (toggle with `Cmd/Ctrl+.`).

### Document model
TipTap with ProseMirror JSON (Fixed). Custom nodes and marks:
- `citation` inline node: attrs `claimId`, `eventIds[]`, `kind`.
- `comment` mark: attr `threadId` (maps to `anchor_mark_id`).
- `claimKind` decoration/mark: drives the visual treatment in 2.2.
- Section headings are real heading nodes with a stable `sectionKey` attribute (`summary, impact, timeline, root_cause, contributing_factors, detection, response, went_well, went_poorly, lessons, action_items`).

### Interactions (editing)

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M10-X01 | Open postmortem | Load | `GET /incidents/{id}/postmortem` | Content, `revision`, ETag, status, lock state |
| M10-X02 | Typing | Edit | Local immediately; debounced autosave `PUT /postmortems/{id}` with `If-Match` and base revision | SaveStatus Saving then Saved. Autosave updates only the working draft, never creates a named version |
| M10-X03 | Save failed / offline | Error | Keep local, retry with backoff | SaveStatus "Failed (Retry)"; content never discarded |
| M10-X04 | Stale save | 412 | StaleVersionDialog | Reload or keep copy; autosave paused (also covers a second browser tab, PRD ED-7) |
| M10-X05 | "Save version" | Click, optional label | Command surface is GAP-16 | Disabled with tooltip until the explicit-save command is defined; autosave remains |
| M10-X06 | Section nav item | Click | Scroll to section | Active section highlighted |
| M10-X07 | Citation chip | Click | Open Citations panel with the event | Panel shows the timeline event (summary, source, times, original link). Unresolvable ids show "Source event unavailable" in warning style |
| M10-X08 | Insert citation | Select text, "Cite evidence" | Open event picker (search timeline) | Inserts chip; claim kind chosen from a small menu |
| M10-X09 | Read-only state | Postmortem `approved` or `published` | Editor non-editable | Banner "Approved. Reopen to edit." with Reopen button (Admin, Member per state machine); toolbar shows lock icon |
| M10-X10 | Slash commands (P1) / shortcuts (P1) | `/` or keys | Local | Insert blocks, trigger actions |
| M10-X11 | Library (S-17) | Load | **GAP-01**: no list endpoint for postmortems in the inventory | Build the library as the incident list filtered to incidents that have a postmortem, using incident filters; show status per postmortem from the postmortem resource when opened. Revisit when an endpoint exists |

### Interactions (inline AI, S-21)

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M10-X20 | AIActionMenu | Select text | Floating menu: Make blameless, Clearer, Shorter, Expand with evidence, Custom instruction | |
| M10-X21 | Run action | Choose | `POST /postmortems/{id}/ai/edit` via SSE (path details GAP-03) | Stream arrives into a SuggestionDiff: old text struck through, new text highlighted |
| M10-X22 | Accept | Click / `Enter` | Apply the change to the document locally | Triggers normal autosave. New facts added by AI arrive with citation chips |
| M10-X23 | Reject | Click / `Esc` | Discard | Suggestion removed; nothing saved |
| M10-X24 | Cancel streaming | Click Stop | Abort the request | Partial text shown as a suggestion the user may accept or discard |
| M10-X25 | AI error | Failure | `error` SSE event | Inline message with Retry; document untouched |
| M10-X26 | Regenerate section | Section menu | `POST /postmortems/{id}/sections/{key}/regenerate` | `202`; result arrives as suggestion/new version (never overwrites human edits). Optional guidance text is P1 |
| M10-X27 | Suggestions not saved | | | Suggestions live in client memory only until accepted (API 6.5) |

### Interactions (comments, S-23)

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M10-X30 | "Comment" on selected text | Click | `POST /postmortems/{id}/comments` (creates thread anchored to mark id) | Highlight in text; thread opens in panel |
| M10-X31 | Comment list | Open panel | `GET /postmortems/{id}/comments` | Threads grouped Open, Resolved, Orphaned |
| M10-X32 | Reply | Submit | `POST /postmortems/{id}/comments` with thread | Appended |
| M10-X33 | Resolve / reopen thread | Click | `PATCH /comments/{id}` | Status changes (reopen supported where API allows) |
| M10-X34 | Anchor follows text | Edit around comment | Local marks | If anchored text deleted, thread becomes **orphaned** and is shown in an Orphaned group with quoted text |
| M10-X35 | Viewer comment-only | Role | `postmortem.comment` only | Editing disabled, commenting enabled |

### Rules and edge cases
- **One author at a time** in v1. A second tab triggers the stale flow on save; no live presence UI is built. The editor is structured (extensions array, document serialization isolated) so Yjs collaboration extensions can be added later without a rewrite.
- Role rules apply live: nobody edits while status is Approved or Published.
- The editor never writes an AI-generated claim into the document without citations or an explicit hypothesis/open-question label.
- Claim-kind styling comes from the document attributes; manually typed text has no kind and shows as plain text.
- Large documents: set a client-side soft warning near the document size limit once the server value is known (DB open item 5).
- Exports (M17) must include citations in readable form; the editor view and export use the same claim data.

### Acceptance criteria
- [ ] M10-AC01 Typing feels instant; autosave never blocks input.
- [ ] M10-AC02 A stale second-tab save is detected and nothing is silently overwritten.
- [ ] M10-AC03 Every citation chip opens its event; broken ones are flagged.
- [ ] M10-AC04 Inline AI shows a diff, and nothing changes until Accept.
- [ ] M10-AC05 Approved and Published documents are not editable until reopened.
- [ ] M10-AC06 Comments stay attached as text moves and become orphaned when text is removed.
- [ ] M10-AC07 Hypotheses, open questions and author context are visually distinct and labeled in text, not only by color.

---

## M11. Blameless language check

**Purpose:** flag and rewrite blame, with the author in control. **Phase:** 2. **Screen:** S-22.

### Layout
Right-panel tab. Header: last-checked revision, counts (open, accepted, edited, dismissed). List of findings; each card shows the **matched text** (highlighted in the document when selected), **category** (attribution, judgment, counterfactual, absolute; also personal blame, unsupported intent, team blame, negligence, minimizing as the AI pipeline expands), a short **reason**, and a **suggested rewrite** when available.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M11-X01 | "Run blameless check" | Click | `POST /postmortems/{id}/blameless-check` | `202`; findings refresh when done |
| M11-X02 | Auto-check | On Submit for review | Same endpoint | Submit waits for a completed check on the latest revision |
| M11-X03 | Findings list | Open tab | `GET /postmortems/{id}/blameless-suggestions` | Open findings first; stale findings (older revision) greyed with "Text changed" |
| M11-X04 | Select finding | Click | Local | Scrolls to and highlights matched text via stored `anchor` |
| M11-X05 | Accept rewrite | Click | `PATCH /blameless-suggestions/{id}` (`accept`) and apply replacement locally | Text replaced; autosave; recorded in version history |
| M11-X06 | Edit rewrite | Edit then Apply | `PATCH` (`edit`) | Custom replacement applied |
| M11-X07 | Dismiss | Click | `PATCH` (`dismiss`) | Finding closed |
| M11-X08 | Rule-only mode | LLM unavailable | Findings without rewrite | Show "Suggested rewrite unavailable" and keep Dismiss/Edit manual |
| M11-X09 | Reviewer view | Reviewer opens | Read-only list | Shows check status and counts; no actions unless they can edit |
| M11-X10 | Show responders by role (P1) | Toggle | Not in inventory | Not built |

### Rules and edge cases
- The rule check works with no LLM; the UI must never imply the check failed because rewrites are missing.
- Accurate factual accountability ("the on-call engineer ran the rollback") is not blame; do not nag. Dismissal is always available.
- Counts shown on the Submit button tooltip: "3 open findings. You can still submit; reviewers will see them."
- **Design choice:** Open findings do not block submit (PRD requires the check to have run, not to be clean).

### Acceptance criteria
- [ ] M11-AC01 Check runs automatically before submit and results are visible to reviewers.
- [ ] M11-AC02 Accept, edit and dismiss each persist and update counts.
- [ ] M11-AC03 Findings for older revisions are marked stale, not silently removed.
- [ ] M11-AC04 Rule findings appear even when no rewrite is available.

---

## M12. Review and approval

**Purpose:** move a postmortem from draft to published with explicit human decisions. **Phase:** 2. **Screens:** S-26, S-27, S-28, S-58 (P1).

### Layout
**ApprovalBar** sits under the editor toolbar and changes with status and role. A **Review panel** tab shows the review checklist (P1), reviewer list (P1), blameless status, unresolved comment count and approval history.

### Interactions (state machine SM-1 in Part 7)

| ID | Control | Visible when | Action / API | Result |
| --- | --- | --- | --- | --- |
| M12-X01 | "Submit for review" | Draft or Changes requested, can edit | `POST /postmortems/{id}/submit` | Status In review; editor stays editable per PRD role rules only until approval; reviewers notified. Disabled with reason if blameless check not run on latest revision or generation running |
| M12-X02 | "Request changes" | In review, Admin | Dialog with required note | `POST /postmortems/{id}/request-changes` | Status Changes requested; note shown to author in a banner |
| M12-X03 | "Approve" | In review, Admin, not the author | Confirm dialog showing version, open findings, unresolved comments | `POST /postmortems/{id}/approve` | Status Approved; document locks; approval recorded |
| M12-X04 | Author viewing own postmortem | In review | Approve disabled with tooltip "You cannot approve your own postmortem" | Server also enforces (409/403) |
| M12-X05 | "Publish" | Approved, Admin | `POST /postmortems/{id}/publish` | Status Published; incident may close when no critical action items are open |
| M12-X06 | "Reopen" | Approved or Published, Admin or Member | Confirm dialog explaining a snapshot is stored first | `POST /postmortems/{id}/reopen` | Status In review; document editable again |
| M12-X07 | Approval history | Open panel | From postmortem approvals data (via postmortem/versions; exact read route GAP-17) | List: approver, role at time, decision, note, time, version |
| M12-X08 | "Assign reviewers" (P1) | | Not in inventory | Not built |
| M12-X09 | Review checklist (P1) | | Not in inventory | Local-only UI is not allowed; skip until defined |
| M12-X10 | Stale approval | Latest version changed after review | Server 409 | Dialog: "The version changed. Review the latest version first." Refetch |

### Rules and edge cases
- Approver is Admin in v1 (Manager later). Button availability uses the `postmortem.approve` capability **and** the "not author" guard.
- Approve is tied to the **latest** version; the confirm dialog names the version label.
- Unresolved comments and open blameless findings are **warnings, not blockers**, in the approve dialog (Design choice).
- After Approve, show "Read-only. Reopen to make changes."

### Acceptance criteria
- [ ] M12-AC01 State transitions and guards match SM-1 exactly.
- [ ] M12-AC02 Authors cannot approve their own postmortem in UI and server.
- [ ] M12-AC03 Reopen stores a snapshot and returns to In review.
- [ ] M12-AC04 Approval history shows approver, time and version.

---

## M13. Versions

**Purpose:** a trustworthy, immutable history with compare and restore. **Phase:** 2. **Screens:** S-24, S-25.

### Layout
Version history: vertical list (newest first) showing version number, label, trigger (generation, submit, request changes, approve, publish, reopen, restore, manual), creator, time, model and prompt version (if AI), blameless open count. Rolling queue: only the latest 15 named versions are active; a note says so.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M13-X01 | Versions list | Load | `GET /postmortems/{id}/versions` | Newest first |
| M13-X02 | Select version | Click | Local | Read-only preview of that snapshot |
| M13-X03 | "Compare" (pick two) | Click | Client-side diff of the two snapshots' `content_text` / JSON | S-25: side by side or inline diff with additions/removals highlighted; citation changes shown |
| M13-X04 | "Restore this version" | Confirm | **GAP-16** (no restore command in the inventory) | Hidden or disabled until defined. Restore must create a **new** version, never mutate history |
| M13-X05 | Version provenance popover | Hover | From version fields | Trigger, label, creator, model, prompt version, blameless count |
| M13-X06 | Rolling-queue note | Always | Static copy | "Older versions leave this list under the retention policy" (mechanics GAP-16) |

### Rules
Versions are immutable and read-only everywhere. Autosave drafts are not versions and never appear here.

### Acceptance criteria
- [ ] M13-AC01 Versions list shows provenance for each entry.
- [ ] M13-AC02 Compare highlights textual and citation differences.
- [ ] M13-AC03 No UI path edits or deletes a named version.

---

## M14. Action items and reminders

**Purpose:** make prevention work get done. **Phase:** 3. **Screens:** S-29 to S-32, S-60 (P1).

### Layout
Action item page: tab bar (Board-like **List**, **Stalled**, **Overdue**, **Nearly due**) over a filterable table. Columns: Title, Priority, Owner, Due, Status, Stalled indicator, Linked incident. Row click opens the **Drawer** (S-31) with details, timeline of changes, verification block.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M14-X01 | List with filters (owner, service, priority, status, stalled) | Load/Change | `GET /action-items` | URL-state filters |
| M14-X02 | "New action item" | Click | Modal (S-30) | |
| M14-X03 | Create form: title (required), description, owner, due date, priority, success criterion | Submit | `POST /action-items` (Idempotency-Key) | Created as confirmed only when owner and due date are both set (`confirmed_at` rule) |
| M14-X04 | AI-proposed items (from postmortem Action items section) | View | From postmortem/draft proposals | Shown as **Suggested** with ai confidence; no owner or due date; clearly labeled "Not assigned" |
| M14-X05 | Accept suggestion | Click | Opens create form prefilled; owner and due date must be chosen by a person | `POST /action-items` | Nothing is tracked or reminded until confirmed |
| M14-X06 | Dismiss suggestion | Click | Local or `PATCH` drop (reason) | Item removed from suggestions |
| M14-X07 | Change status (Open, In progress, Blocked, Done, Dropped) | Menu | `PATCH /action-items/{id}` `If-Match` | Dropped requires a reason (dialog). Done opens verification step |
| M14-X08 | Edit fields | Save | `PATCH /action-items/{id}` | Toast; 412 handled |
| M14-X09 | Verification (Done) | Submit note and/or link | `POST /action-items/{id}/verify` | Shows verification block; note encouraged, not required |
| M14-X10 | Stalled indicator | Render | From `stalled_since` | Warning badge with "Stalled since X" and cause (overdue or no update for N days) |
| M14-X11 | Change history | Open drawer | From item events | Created, status, owner, due, verified, confirmed entries |
| M14-X12 | Linked incident / postmortem | Click | Navigate | |
| M14-X13 | Create GitHub issue (P1) / Slack reminders (P1) | | Not in inventory | Not built |
| M14-X14 | Reminder visibility | Notification center | Notifications (M19) | Owner sees pre-due, stalled, escalated notices |

### Rules and edge cases
- Stalled is **computed**, not a status. Never show it as a selectable status.
- Owner picker lists active org members (display names from `/members`).
- Dropped requires a non-empty reason; Done does not require a note.
- Items on a deleted incident disappear on refresh.

### Acceptance criteria
- [ ] M14-AC01 No AI-proposed item is tracked or assigned without a person confirming owner and due date.
- [ ] M14-AC02 Dropped requires a reason; stalled displays correctly and is filterable.
- [ ] M14-AC03 Filters by owner, service, priority, status work and persist in the URL.

---

## M15. Analytics

**Purpose:** show recovery performance, volume and action health. **Phase:** 3 (P0), later for repeat analytics. **Screens:** S-33 to S-36, S-55, S-56, S-62, S-63.

### Layout
Analytics page with tabs: **Overview, Recovery time, Incident volume, Action health** (P1 tabs: Recurring causes, Timeliness; Later: Repeat incidents). A shared filter bar: period (week/month, range), service, severity. Charts use Recharts with tokens; every chart has a data table toggle and text summary for accessibility.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M15-X01 | Recovery time tab | Load | `GET /analytics/recovery-times` | Cards: time to detect, acknowledge, mitigate, resolve (mean). Trend line chart by period |
| M15-X02 | Incident volume tab | Load | `GET /analytics/incident-volume` | Stacked bars by severity or type, group-by selector (service, severity, type) |
| M15-X03 | Action health tab | Load | `GET /analytics/action-health` | Completion rate, average time to close, stalled count |
| M15-X04 | Filters | Change | Query params | Charts update, URL state |
| M15-X05 | Chart point click | Click | Navigate to incident list filtered by the clicked bucket | |
| M15-X06 | Empty analytics | No data | EmptyState | "Analytics appear after your first resolved incidents" |
| M15-X07 | Repeat incident UI (Later) | | Reserved | Incident overview will get a "Possible repeat" card with Confirm/Dismiss; no v1 UI |

### Rules
Durations display as human units ("12m 30s"), stored as seconds. Null means "No data", never zero. Demo-tenant data shows a small "Demo data" badge.

### Acceptance criteria
- [ ] M15-AC01 The three P0 analytics views render from their endpoints with loading, empty and error states.
- [ ] M15-AC02 Filters by service, severity and period work and persist in the URL.
- [ ] M15-AC03 Missing values show "No data", not 0.

---

## M16. Search and filtering

**Purpose:** find things fast. **Phase:** P1 (global search, saved filters); filters per list are P0 in their modules. **Screens:** S-52, S-53.

- Per-list filters and sorts are implemented inside their modules (M04, M14, M07, M08).
- **Global search (P1):** command palette (`Cmd/Ctrl+K`). **GAP-18:** no search endpoint is documented (PRD DSH-3 mentions Postgres full-text search). Until defined, the palette only searches navigation items and recently viewed incidents from local cache.
- **Saved filters (P1):** stored per user; **GAP-18** (no endpoint). Not built in v1.

### Acceptance criteria
- [ ] M16-AC01 Palette opens with a shortcut and navigates to pages; it does not claim to search content until an endpoint exists.

---

## M17. Exports and reports

**Purpose:** get postmortems out as PDF and Markdown with citations intact. **Phase:** 2 (single export), P1 and Later for bulk and reports. **Screens:** S-50, S-51, S-54, S-64, S-65, S-66.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M17-X01 | "Export" button (postmortem toolbar) | Click | Open modal S-50 | Choose format: PDF or Markdown. Shows "Includes timeline, source references, version label" |
| M17-X02 | "Start export" | Click | `POST /postmortems/{id}/export` (format field per OpenAPI, Idempotency-Key) | `202`; modal moves to progress step |
| M17-X03 | Export progress | Automatic | JobProgress | On success: "Download" button |
| M17-X04 | "Download" | Click | `GET /exports/{id}/download` (signed link) | Browser downloads; link is short-lived, so request a fresh one on each click, never store it |
| M17-X05 | Export failure | Error | User-safe message + Retry | |
| M17-X06 | Export history (P1) | | No list endpoint | Not built; modal only shows the current export |
| M17-X07 | Bulk export / org archive / audit-ready report / share link | | P1, Later, P2 | Not built in v1. No placeholder UI |

### Rules
Which version is exported: default to the current version; display its label in the modal. Exports must preserve citations in readable, traceable form (AI-pipeline requirement).

### Acceptance criteria
- [ ] M17-AC01 PDF and Markdown export both complete and download.
- [ ] M17-AC02 The download link is never cached or reused after expiry.

---

## M18. Audit log

**Purpose:** a read-only, verifiable record. **Phase:** 3 (UI), 1 (backend log). **Screens:** S-48, S-49.

### Layout
Admin-only table with cursor pagination: time, actor (name and role at the time), service, action, entity, summary. Filter by action, actor, entity, date. Row click opens a details drawer (details JSON shown as a safe key/value list; `details` never contains secrets).

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M18-X01 | Log table | Load/scroll | `GET /audit-log` cursor + limit | Infinite load |
| M18-X02 | Filters | Change | Query params | URL state |
| M18-X03 | Details drawer | Click row | Local | Full entry: action, entity, request id, hashes shown shortened with copy |
| M18-X04 | "Verify integrity" | Click | `GET /audit-log/verify` | Panel S-49: result (OK or first mismatched entry) with timestamp of verification and head hash |
| M18-X05 | Retention controls (P1) | | Org settings (M02) | Not here |

### Rules
No edit or delete controls exist anywhere. Copy states entries are append-only and hash-chained.

### Acceptance criteria
- [ ] M18-AC01 Log loads with cursor pagination and filters.
- [ ] M18-AC02 Verify shows OK or the first failing entry clearly.
- [ ] M18-AC03 No mutation affordance exists on this screen.

---

## M19. Notifications

**Purpose:** in-app awareness of reviews, approvals and action reminders. **Phase:** 3. **Screens:** S-46, S-47.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M19-X01 | Bell badge | Load, poll | `GET /notifications` (unread count from list) | Count badge; poll interval is a frontend config constant (no push in v1) |
| M19-X02 | Bell popover | Click | Same list (latest) | Latest notifications with relative times; "View all" |
| M19-X03 | Notification center | Load | `GET /notifications` page pagination, unread filter | Full list with type icon, title, body, time |
| M19-X04 | Open notification | Click | `PATCH /notifications/{id}` (mark read), then navigate to `link_path` | Navigates inside the app |
| M19-X05 | "Mark all as read" | Click | PATCH each unread (no bulk endpoint) | Do in sequence with progress; hide if many (GAP-19) |
| M19-X06 | Notification settings | Load | `GET /notification-settings` | Switches: email, in-app; per-type mute |
| M19-X07 | Save settings | Toggle | `PATCH /notification-settings` | Immediate save with toast |
| M19-X08 | Reminder timing / thresholds (P1) | | Org settings (M02 fields) | Admin only |

### Notification types (from DB design)
`draft_ready, review_requested, approved, changes_requested, action_due, action_stalled, action_escalated`. Each type maps to an icon and a deep link target.

### Acceptance criteria
- [ ] M19-AC01 New notifications appear within the polling interval and deep-link correctly.
- [ ] M19-AC02 Mark-read persists and the badge updates.
- [ ] M19-AC03 Preferences save and are respected in the UI list (muted types are not shown as toasts).

---

## M20. AI model settings and usage

**Purpose:** let an Admin choose the model with clear privacy messaging. **Phase:** 2 (setting), 3 (usage). **Screen:** S-45.

### Layout
Two cards. **Model:** radio between **Retrace default model** and **Custom model**. Custom shows Provider (select: azure_openai, openai, anthropic, openai_compatible), Model name, Endpoint URL, API key (write-only), optional max context tokens. **Usage:** daily calls and limit on the default model; message when reached.

### Interactions

| ID | Control | Trigger | Action / API | Result |
| --- | --- | --- | --- | --- |
| M20-X01 | Load settings | Load | `GET /ai-model` | Shows current mode, provider, model name, endpoint, **masked key hint**, last test result and time |
| M20-X02 | Switch to Default | Select, Save | `PUT /ai-model` | Toast |
| M20-X03 | Custom config | Fill, Save | `PUT /ai-model`; key sent once | Connection test runs on save (PRD AI-3); show result inline |
| M20-X04 | "Test connection" | Click | `POST /ai-model/test` | Inline success or user-safe failure; does not reveal the key |
| M20-X05 | "Replace key" | Click | Opens an empty write-only field | Old key is never displayed |
| M20-X06 | Privacy notice | Always visible | Static, plain | "Evidence sent to a hosted model leaves your organization workspace." (PRD AI model configuration) |
| M20-X07 | Usage meter | Load | Usage data endpoint is not in the inventory | **GAP-20**: show limit messaging only when a generation returns the limit error; no usage chart until defined |

### Rules
Provider list is fixed to DB design values. Using a custom key removes the default-model limit (provider limits still apply); show that sentence in the custom section.

### Acceptance criteria
- [ ] M20-AC01 The API key is never visible after saving; only a masked hint.
- [ ] M20-AC02 Connection test result is shown; failure does not discard other fields.
- [ ] M20-AC03 The hosted-model privacy notice is always visible on this screen.

---

## M21. Jobs and system feedback (cross-cutting)

**Purpose:** one consistent way to show background work and system problems.

| ID | Behavior | Rule |
| --- | --- | --- |
| M21-X01 | `useJob(jobId)` hook | Polls `GET /jobs/{job_id}` (start 2s, back off to a cap, stop at terminal state). Upgrades to SSE when the AI/Core SSE contract is published (GAP-03), keeping polling as fallback |
| M21-X02 | Job states | queued, running, succeeded, failed, cancelled, plus AI "partial" |
| M21-X03 | Retry | Offered only where retry is meaningful (generation, export, discovery) and creates a new command with a new Idempotency-Key |
| M21-X04 | Cancel | Only where the service exposes it (none generic in v1). No cancel button otherwise |
| M21-X05 | Job list view | Not required. Jobs are shown in place. The "view queued/running/failed jobs" inventory items are satisfied by per-screen JobProgress |
| M21-X06 | Error reference | Every job error and API error shows a copyable `correlation_id` |
| M21-X07 | Global banners | Session expiring, offline, rate limited (429), degraded service |

### Acceptance criteria
- [ ] M21-AC01 Every 202 flow uses JobProgress and handles all terminal states.
- [ ] M21-AC02 Navigating away and back during a job restores its progress view.

---

# PART 7. END-TO-END WORKFLOWS AND STATE MACHINES

## WF-1. Onboarding to first incident

```
Sign up -> verify email -> sign in -> Create organization -> SettingUpScreen (poll)
-> Dashboard (empty) -> Settings: AI model (default preselected, confirm)
-> Integrations: connect Slack, PagerDuty (GitHub stretch)
-> Allowlist: choose channels -> Services: add services + links
-> Members: invite teammates -> Create incident
```
**Empty-dashboard guide:** until setup is complete the dashboard shows a checklist (Choose AI model, Connect Slack, Connect PagerDuty, Add a service, Invite a teammate). Each item deep-links to the right settings screen and checks off from real state (integration status, service count, member count), not local flags.

## WF-2. Incident to approved postmortem (the core loop)

```
Incident (from PagerDuty or manual)
 -> [M04] Describe what happened (only required input)
 -> [M07] Discovery job -> Evidence preview -> (optional include/exclude/add) -> Confirm
 -> [M08] Timeline built (phases, key moments, discrepancies)
 -> [M09] Generate -> progress -> result, limitations, clarifications
 -> [M10] Edit with citations, inline AI, comments
 -> [M11] Blameless check (auto before submit) -> accept/edit/dismiss
 -> [M12] Submit for review -> reviewers comment -> Admin approves or requests changes
 -> Publish -> [M17] Export -> [M14] Action items tracked
```

| Step | Screen | Primary control | Next |
| --- | --- | --- | --- |
| 1 | Create incident modal | "Create and find evidence" | Evidence tab with JobProgress |
| 2 | Evidence tab | "Confirm evidence" | Timeline tab with JobProgress |
| 3 | Timeline tab | "Generate postmortem" | Postmortem tab with GenerationProgress |
| 4 | Postmortem tab | Edit, comment, check | "Submit for review" |
| 5 | Postmortem tab (review) | "Approve" (Admin) | Locked read-only |
| 6 | Postmortem tab | "Publish" | Export, track actions |

## WF-3. Changes requested loop

```
In review -> Admin "Request changes" (note required) -> author sees banner with note
-> author edits (blameless re-check if text changed) -> "Submit for review" -> In review
```

## WF-4. Reopen after approval

```
Approved/Published -> "Reopen" -> confirm (snapshot stored) -> In review (editable)
-> edit -> submit -> approve again (new version, new approval record)
```

## WF-5. Evidence changes after generation

```
Author excludes/includes evidence -> new immutable evidence snapshot
-> running AI job marked stale -> banner "Evidence changed. Regenerate."
-> Generate again -> new version created (previous versions keep their original snapshot reference)
```

## WF-6. Action item lifecycle

```
AI suggests (Suggested, unassigned) -> person confirms owner + due date -> Open
-> In progress / Blocked -> Done (+ optional verification) | Dropped (+ required reason)
Stalled (computed): not Done AND (past due OR no update for N days)
-> reminders: pre-due (owner) -> stalled (owner) -> escalated (Admins) -> in-app + email
```

## WF-7. Invitation and join

```
Admin invites email+role -> invitee opens link -> sign in or sign up (same email)
-> accept -> lands in org -> org appears in switcher
Expired/revoked -> clear message, "Ask an admin for a new invite"
```

## SM-1. Postmortem state machine (Fixed: PRD 9, System Design 21, API 10.1)

| From | To | Who | UI guard |
| --- | --- | --- | --- |
| Draft | In review | Admin, Member | Blameless check run on latest revision, no generation running |
| In review | Changes requested | Admin | Note required |
| In review | Approved | Admin, not author | Reviewing the latest version |
| Changes requested | In review | Admin, Member | A new version exists (editing creates it) |
| Approved | Published | Admin | None |
| Approved or Published | In review | Admin, Member | Snapshot stored; read-only until reopened |

Editable only in Draft, In review (by roles), Changes requested. Locked in Approved and Published.

## SM-2. Incident states
Open, Resolved, Postmortem in progress, Closed. Transitions are system-driven (PagerDuty event or manual, generation, publish with no open critical action items). The UI never exposes manual state-change buttons for these except through the described actions.

## SM-3. Action item states
Open, In progress, Blocked, Done, Dropped. Any non-terminal to Dropped requires a reason. Stalled is a flag.

## SM-4. Evidence item states
Collected, Included, Excluded, Failed. Excluded items remain in history and can be re-included.

## SM-5. Job states
Queued, Running, Succeeded, Failed, Cancelled (AI additionally exposes partial).

## 7.1 "Which file opens which" (navigation map)

| From | Control | To |
| --- | --- | --- |
| Dashboard | Recent incident row | Incident overview |
| Dashboard | Awaiting review row | Postmortem tab |
| Dashboard | Action row | Action item drawer |
| Incident list | Row | Incident overview |
| Incident overview | Banner button | Evidence / Timeline / Postmortem tab by state |
| Evidence tab | Confirm | Timeline tab |
| Timeline tab | Generate | Postmortem tab |
| Timeline event panel | Linked evidence | Evidence tab item |
| Postmortem editor | Citation chip | Citation panel, then Timeline event panel |
| Postmortem editor | Versions | Version history |
| Version history | Compare | Version comparison |
| Postmortem toolbar | Export | Export modal |
| Postmortem editor | Action items section | Action item create form |
| Action item drawer | Linked incident | Incident overview |
| Notification | Click | `link_path` target |
| Settings integrations | Card | Integration details, then allowlist |
| Service catalog | Link editor | (missing allowlist item) Integrations allowlist |

---

# PART 8. BUILD PLAN AND AGENT TASK TEMPLATE

## 8.1 Build order (matches the 8-week plan; one coherent PR per row)

| Order | Work | Modules | Done when |
| --- | --- | --- | --- |
| 1 | Tokens, theme, base components, AppShell, router, providers | Design system, M03 shell | Shell renders all nav items with role gating |
| 2 | API client (auth, ETag, idempotency, errors), query keys, generated types pipeline (`pnpm generate:api`) | Architecture | One generated type consumed by one handwritten call |
| 3 | Auth screens + session restore | M01 | M01 acceptance criteria pass |
| 4 | Org creation, SettingUpScreen, switcher, members, invitations, org settings | M02 | A new org reaches the dashboard and invites a member |
| 5 | Incident list, create, detail frame, next-step banner | M04 | Description-only create reaches Evidence tab |
| 6 | Integrations + allowlists, service catalog | M05, M06 | Slack and PagerDuty connect; services link |
| 7 | Evidence preview + timeline | M07, M08 | Description to confirmed timeline |
| 8 | JobProgress/useJob + generation + AI settings | M09, M20, M21 | Generation completes, retry works |
| 9 | Editor core: TipTap, autosave, ETag/stale, citations, section nav | M10 | M10-AC01 to AC03, AC05 |
| 10 | Inline AI, comments, blameless panel | M10, M11 | M10-AC04, AC06; M11 criteria |
| 11 | Review/approval, versions, export | M12, M13, M17 | Incident to approved, exported postmortem |
| 12 | Action items + notifications | M14, M19 | Suggested to done lifecycle and reminders visible |
| 13 | Analytics + audit log | M15, M18 | Three analytics views + verify |
| 14 | Dashboard completion, empty states, a11y pass, demo data, E2E | M03, all | Playwright core loop passes |

If the schedule slips, cut in the order from the PRD: email delivery (backend), analytics, GitHub, extra export formats. **Never cut:** tenant isolation tests, stale-version handling, citation resolution, human-accept for AI.

## 8.2 Task template (use for every Cursor, Antigravity or Codex task)

```
TASK: <Mnn / S-nn / WF-n, one line>
ALLOWED PATHS: web/src/features/<x>/**, web/src/components/** (only if promoting shared code)
READ FIRST: this document (Part 0.4, Part 5, the module chapter), Repository Conventions Spec, API and Event Contracts Spec section(s) <..>
CONTRACTS: endpoints used (from the chapter), generated types in web/src/generated/
DO: implement the chapter's interactions Mnn-X.., states, and acceptance criteria Mnn-AC..
DO NOT: invent endpoints or fields, edit generated files, add libraries not listed in 3.1 without an ADR, hide a GAP by guessing
TESTS: Vitest + RTL for behavior (states, permission gating, error mapping); Playwright only for WF-n critical flows
HANDOFF: PR summary listing GAPs hit, files changed, screenshots of each state (loading, empty, error, permission-denied)
```

## 8.3 Definition of done (every module PR)

- [ ] All interaction rows in the chapter implemented or explicitly listed as GAP/not-built with the documented fallback.
- [ ] Loading, empty, error and permission-denied states exist and are tested.
- [ ] Every mutation handles 412, 422, 429 and network failure.
- [ ] Role gating uses `can(capability)`; backend failure paths handled.
- [ ] No secrets or tenant data in logs, toasts or URLs.
- [ ] Keyboard navigation and focus order verified for the core flow.
- [ ] Acceptance criteria checkboxes in the chapter all pass.
- [ ] Generated types current (`pnpm generate:api` produces no diff).
- [ ] Conventional Commit messages and PR description per Repository Conventions.

## 8.4 Testing focus (frontend)

| Area | Test |
| --- | --- |
| Session | Single-flight refresh, expiry during edit, org switch cache clear |
| Concurrency | 412 on editor autosave and forms, no auto-retry |
| Idempotency | Retry reuses key, new intent gets new key |
| Permissions | Admin vs Member rendering per capability, 403 handling |
| Editor | Autosave debounce, citation click, read-only locks, suggestion accept/reject, comment anchoring |
| AI states | partial, failed, verification unavailable, limit reached |
| Evidence | Include/exclude shows snapshot notice; external link is note-only |
| Cross-tenant | Switching orgs never leaks cached data |
| A11y | Axe checks on core screens |
| E2E (Playwright) | WF-2 happy path against mocked backend |

---

# PART 9. GAPS AND ASSUMPTIONS REGISTER

**Do not resolve a GAP by guessing in code.** Build the documented fallback, mark the control, and record it in the PR. Resolve gaps in the central `contracts/` folder or an ADR first.

| ID | Gap | Source of gap | Documented fallback in this doc |
| --- | --- | --- | --- |
| GAP-01 | No `GET /postmortems` list endpoint for the library; no incident filter for "postmortem status"; evidence window field names | API Contracts 4.1 | Library = incident list filtered by existing incident filters; status read per postmortem on open. Window edited through incident `PATCH` once fields are defined |
| GAP-02 | Exact request/response fields, validation and filters for every endpoint | API-01 | Use generated types only; do not hand-write unknown fields |
| GAP-03 | Public job resource mapping, SSE path, reconnect and payloads; how to find the latest job for a resource | API-03 | Poll `GET /jobs/{job_id}`; store `job_id` from the 202 response in client state; SSE adapter built behind `useJob` later |
| GAP-04 | Page-size defaults, rate-limit numbers, retry/backoff values | CFG-01 | Single frontend config constants file, clearly marked provisional |
| GAP-05 | Verify-email, resend-verification and password-reset confirm bodies | API Contracts 4.1 | Build screens; hide "Resend" if no endpoint |
| GAP-06 | "Sign out of all devices" endpoint | Not in inventory | Control hidden |
| GAP-07 | Soft-delete success response (204 vs body) and restore endpoints | API 10.3 | Handle both; no restore UI |
| GAP-08 | List and revoke invitations (identifier shape) | Not in inventory | Invitations tab shell with session-local list |
| GAP-09 | Delete incident, delete organization, retry provisioning endpoints | Not in inventory | Controls hidden |
| GAP-10 | Provisioning retry endpoint | System Design 4.5 | SettingUpScreen shows error; Admin retry hidden |
| GAP-11 | Exact call to switch the active organization token | API 3.2 | Wrap in `switchOrg()` in `api/`; implement when documented |
| GAP-12 | Notification settings route placement (`settings/*` Admin vs per-user) | System Design vs this doc | Placed under `account/` |
| GAP-13 | Credential fields for org-owned Slack app; Slack export upload | System Design 15 | Not built |
| GAP-14 | Timeline event create path (inventory lists `POST, PATCH, DELETE /timeline-events/{id}`) | System Design 15 | Follow OpenAPI once published; build the form now |
| GAP-15 | Where clarification questions arrive and the endpoint to submit answers | AI Pipeline 10 | Render from generation result if provided; "Provide context" disabled until endpoint exists |
| GAP-16 | Explicit save command, restore command, rolling-queue archive mechanics | PM-01 | "Save version" and "Restore" disabled with tooltip |
| GAP-17 | Read route for approval history | Not in inventory | Derive from versions provenance and approve/decline entries when available |
| GAP-18 | Search endpoint and saved filters | PRD DSH-3, DSH-4 | Command palette navigates only |
| GAP-19 | Bulk "mark all read" | Not in inventory | Sequential PATCH or hide |
| GAP-20 | AI usage and limit read endpoint | Not in inventory | Show limit messaging only from error responses |

### Assumptions made in this document (all Design choices, change freely)

1. Dark theme only in v1; tokens are CSS variables so a light theme is additive.
2. Accent color `#7C8CFF`; fonts Inter, Source Serif 4, JetBrains Mono, self-hosted.
3. Hybrid layout: dense dashboard shell, calm editorial editor (max 720px column, right slide-over panel).
4. Open blameless findings and unresolved comments are warnings, not blockers, on submit and approve.
5. Services entry is visible to all members; write controls are Admin-only.
6. Notification settings live under `account/`, not `settings/`.
7. Sidebar collapse state is stored in `localStorage` (non-sensitive UI preference only).
8. GitHub UI is behind a feature flag in v1 (stretch).
9. Polling intervals (jobs, notifications) are frontend constants until contracts define better.

---

# APPENDIX A. ENDPOINT TO SCREEN MAP

Prefix tenant paths with `/api/v1/orgs/{org_id}`. Auth and org creation use `/api/v1`.

| Endpoint | Module | Screens |
| --- | --- | --- |
| `POST /auth/register, /login, /logout, /refresh, /verify-email, /password-reset`, `GET /auth/oauth/{provider}/start, /callback`, `GET /me` | M01 | S-01 to S-07 |
| `POST /orgs`; `GET, PATCH /orgs/{org_id}`; `GET, PATCH /settings` | M02 | S-08, S-42 |
| `GET /members`; `PATCH, DELETE /members/{id}`; `POST, DELETE /invitations`; `POST /invitations/accept` | M02 | S-43, S-44 |
| `GET, POST /incidents`; `GET, PATCH /incidents/{id}`; `POST /incidents/{id}/description` | M04 | S-10 to S-12 |
| `GET /integrations`; `POST /integrations/{provider}/connect`; `GET .../callback`; `DELETE /integrations/{id}`; `GET, PUT /integrations/{id}/allowlist` | M05 | S-37 to S-39 |
| `GET, POST, PATCH, DELETE /services`; `PUT /services/{id}/links` | M06 | S-40, S-41 |
| `GET /incidents/{id}/evidence`; `PATCH /evidence/{id}`; `POST /incidents/{id}/evidence`; `POST /incidents/{id}/evidence/confirm` | M07 | S-13, S-14 |
| `GET /incidents/{id}/timeline`; `POST, PATCH, DELETE /timeline-events/{id}` | M08 | S-15, S-16 |
| `POST /incidents/{id}/postmortem/generate` | M09 | S-18 |
| `GET /incidents/{id}/postmortem`; `PUT /postmortems/{id}`; `GET /postmortems/{id}/versions` | M10, M13 | S-19, S-24, S-25 |
| `GET, POST /postmortems/{id}/comments`; `PATCH /comments/{id}` | M10 | S-23 |
| `POST /postmortems/{id}/ai/edit` (SSE); `POST /postmortems/{id}/sections/{key}/regenerate` | M10 | S-21 |
| `POST /postmortems/{id}/blameless-check`; `GET /postmortems/{id}/blameless-suggestions`; `PATCH /blameless-suggestions/{id}` | M11 | S-22 |
| `POST /postmortems/{id}/submit, /approve, /request-changes, /publish, /reopen` | M12 | S-26 to S-28 |
| `GET, POST /action-items`; `PATCH /action-items/{id}`; `POST /action-items/{id}/verify` | M14 | S-29 to S-32 |
| `GET /analytics/recovery-times, /incident-volume, /action-health` | M15 | S-33 to S-36 |
| `POST /postmortems/{id}/export`; `GET /exports/{id}/download` | M17 | S-50, S-51 |
| `GET /audit-log`; `GET /audit-log/verify` | M18 | S-48, S-49 |
| `GET /notifications`; `PATCH /notifications/{id}`; `GET, PATCH /notification-settings` | M19 | S-46, S-47 |
| `GET, PUT /ai-model`; `POST /ai-model/test` | M20 | S-45 |
| `GET /jobs/{job_id}` | M21 | All async screens |

# APPENDIX B. COPY AND MESSAGE CATALOG (SEED)

| Situation | Text |
| --- | --- |
| Stale save | "This changed while you were working. Reload the latest version or keep a copy of your text." |
| Own approval blocked | "You cannot approve your own postmortem." |
| Blameless not run | "Run the blameless check before submitting." |
| Verification unavailable | "Semantic verification unavailable. Deterministic checks passed." |
| No evidence found | "We found no evidence in the allowed sources. Add evidence, widen the time window, or review the allowlist." |
| Hosted model notice | "Evidence sent to a hosted model leaves your organization workspace." |
| Hypothesis tag | "Hypothesis. Not confirmed." |
| Author context tag | "Author context. Not independently verified." |
| Locked document | "Approved. Reopen to make changes." |
| Rate limited | "Too many requests. Try again in {n} seconds." |
| Session expired while editing | "Session expired. Sign in again to save your work." |
| Last admin | "An organization must keep at least one Admin." |
| Private channel | "Private channels can contain sensitive conversations. Add this channel only if the team expects Retrace to read it." |

---

*End of document. Version 1.0, 10 November 2026. Next revision should resolve GAP-01, GAP-03, GAP-15 and GAP-16 first, since they block the editor, job UX and generation clarification flows.*
