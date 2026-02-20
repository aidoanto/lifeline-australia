# How we use Twilio data (and what matters most)

Summary of how Lifeline uses data from Twilio and which data is most important, based on Digital Product Wiki / Notion.

---

## How we use Twilio data

### 1. **Flex Insights (in-product dashboards)**

- **What:** Twilio’s built-in analytics for Flex (agent desktop). The “analytics panel” is linked to Flex Insights; access is controlled by worker roles (e.g. `wfo.data_analyst`, `wfo.full_access`).
- **Where:** Flex Admin → Dashboards (and role setup via [Flex Insights User Roles](https://www.twilio.com/docs/flex/admin-guide/setup/sso-configuration/insights-user-roles)).
- **Who:** STLs, SDLs, admins (by platform: CISS Central voice vs DIGI Central). Specific users are granted access per platform (see Land of Technology → Twilio for lists).
- **Use:** Day-to-day performance and resourcing: team/agent KPIs, queue stats, support types, duration, reject/transfer rates, and links to conversation transcripts.

### 2. **Conversation transcripts**

- **What:** Out-of-the-box Twilio transcripts of CS↔ISS chat. Described as “not structured” and “not yet reviewed and assessed” historically.
- **Where:** Flex → Admin → Dashboards → Conversations → click conversation ID to open transcript. (Access via Twilio login, not Microsoft SSO; specific accounts only.)
- **Who:** Limited (e.g. Alison Maltby, Bruno have/had access).
- **Use:** Review of individual CS–ISS conversations when needed.

### 3. **C-ISS activity / task-level reporting**

- **What:** Twilio captures interaction data (queues, task lifecycle). Initially only two queues (urgent / non-urgent); later extended so Digi uses the same queue model as Voice for reporting (e.g. by conversation type).
- **Use:** Understanding volume, assignment, and task flow for CISS activity; aligning Voice and Digi reporting.

### 4. **Queue-based reporting (aligned Voice + Digi)**

- **What:** Queues and channels configured so reporting “works the same way as voice” for Digi. Queue categories used for reporting include: check_in, check_out, safety, support, debrief, imminent (and technical_support for Digi).
- **Use:** Consistent metrics across CISS Central and DIGI Central (today stats, daily stats, monthly stats, support types, queue reporting). Management Report and queue reporting depend on this.

### 5. **Twilio data + Databricks (planned / in progress)**

- **What:** Pipe Twilio data into Databricks for maintained, reliable reports consistent with other tools (e.g. Power BI), with Australian data storage for compliance.
- **Status:** Task “Twilio data and reporting with Data Bricks” (DPT-1481) — Solution Refinement. Acceptance criterion: “All data is piped into Data Bricks.”

### 6. **Operational / debugging data**

- **What:** Task attributes, conversation SIDs, reservation/task SIDs, Twilio conversation export URLs and message APIs (e.g. when investigating “stuck in wrapping” or chat visibility). Also Twilio serverless build/deploy logs.
- **Use:** Incident investigation, fixing stuck tasks, and understanding disconnect/visibility issues.

---

## Data that’s most important

In order of practical importance for operations, compliance, and product:

| Priority | Data / area | Why it matters |
|----------|-------------|----------------|
| **1** | **Queue + support-type metrics (by agent / team / time)** | Resourcing, performance, and “management dashboard” views. STLs/SDLs need conversation types (imminent, safety, support, debrief, check_in, check_out) by agent/team/day/week/month and date range. Aligned between CISS Central and Digi Central. |
| **2** | **Task lifecycle and timing** | Duration of supports, reject/transfer rates, RONA by support type, “logged status” as % by agent. Needed for KPIs and understanding workload and behaviour. |
| **3** | **Conversation list + transcript link** | Ability to see CS name, ISS name, and open the chat transcript. Critical for quality, escalation, and incident review. |
| **4** | **Access control and roles** | Correct Flex Insights roles (e.g. `wfo.full_access`, `wfo.team_leader`, `wfo.data_analyst`) so the right people see the right dashboards (CISS vs Digi, STL vs SDL vs admin). Documented in Land of Technology → Twilio. |
| **5** | **Reliable, maintainable reporting (e.g. Databricks)** | So reporting is consistent with other tools (e.g. Power BI) and data is stored in Australia for compliance. |
| **6** | **Task/conversation identifiers and attributes** | For fixing stuck tasks, cancelling tasks in queue, and debugging (e.g. reservation SID, task SID, conversation SID). Twilio docs task mentions “fix issues without a release” (e.g. cancelling a task stuck in queue). |

---

## Where it’s documented in Notion

- **Data and reporting in Twilio** — Flex Insights setup, roles, C-ISS Activity Reporting, Twilio transcripts.
- **C-ISS Activity Reporting** — What Twilio captures (queues, interaction data); transcripts “not structured”.
- **Twilio transcripts** — How to access (Flex → Admin → Dashboards → Conversations → ID).
- **CISS twilio insights - dashboard setup** — Management Report, Today/Daily/Monthly stats, queue reporting (check_in, check_out, safety, support, debrief, imminent), Support Types, alignment CISS Central vs Digi Central.
- **Insights dashboard** — User story: STLs see key metrics; metrics listed for DIGI and CISS Central (conversation types by agent/team/period, duration, reject/transfer, transcript link, rejected/RONA by support type, logged status %).
- **Queues for Reporting** — Digi queues aligned to Voice so “reporting will work the same way”.
- **Twilio data and reporting with Data Bricks** — User story: maintained reports, consistency with Power BI, data in AU.
- **Twilio** (Land of Technology) — Insights access by platform, roles, onboarding.
- **Twilio Documentation** (task) — Document solution; admin fixes without release (e.g. cancel stuck task); onboarding (e.g. profile photo).

---

## Quick reference: support types / queues for reporting

- **CISS Central (voice):** check_in, check_out, debrief, imminent, safety, support.
- **DIGI Central:** Same plus **technical_support**. “Support types” and “queue reporting categories” are to be aligned between both; Management Report and Support Types links must work in both.
