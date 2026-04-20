---
name: cst
description: |
  Use when investigating a customer service issue that requires symptom alignment, evidence from logs, frontend/backend code, MySQL data, root-cause explanation for product and engineering, or optional Feishu investigation logging.
---

# Customer Service Troubleshooting (CST)

## First Use

First check whether the current shell already has the required environment variables for git access, database access, log access, and optional Feishu doc logging.

Treat frontend code location and backend code location as separate inputs. Do not assume they live in the same directory or the same repository.

Prefer a named log access method in `CST_LOG_ACCESS_METHOD`. If it is already set, use it as the default log-query method for this investigation.

If the relevant environment variables are already present, confirm they are the right ones to use for this investigation and only ask the user for anything that is still missing.

If required values are missing, ask for the frontend code location, the backend code location, mysql host/user/password, the log-query method the user already uses, and any log-related connection details or credentials required to use it.

Create or update a local `config.env` in the investigation workspace, write both database and log-related environment variables into it, and ask the user to export those values into the shell before continuing. Do not commit local credentials.

If the chosen log access method needs credentials, endpoints, project names, logstore names, cluster context, tokens, or other connection details, put them in `config.env` with clear variable names before querying logs.

If `CST_LOG_ACCESS_METHOD=aliyun-cli`, use `aliyun-cli` directly and keep its required credentials in environment variables. Prefer:

- `ALIBABA_CLOUD_ACCESS_KEY_ID`
- `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
- `ALIBABA_CLOUD_REGION_ID`
- `ALIBABA_CLOUD_SECURITY_TOKEN` (optional, if using STS)

If `CST_LOG_ACCESS_METHOD` is set to another value, use that method and the corresponding environment variables or connection details instead.

If the team wants every finished investigation written to Feishu Docs, prefer this setup:

- Install `lark-cli`
- Run `lark-cli config init` locally once
- Run `lark-cli auth login --recommend` locally once
- Put the target doc URL in `CST_FEISHU_DOC_URL`
- Optionally set `CST_FEISHU_LOG_TITLE_PREFIX` to customize each case title

Do not ask the user to paste their Feishu token into chat if local CLI login can be done instead.

If `CST_FEISHU_DOC_URL` is present, treat doc logging as enabled for this investigation unless the user explicitly says not to write this case.

## Available Assets

- `config.env.example`: a reference for environment variables used to configure code locations, database access, log access, and optional Feishu doc logging.
- `assets/templates/feishu-investigation-log-template.md`: a report skeleton for the final investigation summary before appending it to Feishu.

## Workflow

### 1. Align On The Issue First

Start by confirming what the user actually means. Ask clarifying questions until the symptom is aligned: user identity, time window, page or feature, expected behavior, actual behavior, frequency, and whether the issue is still happening.

Do not move on while the reported phenomenon is still vague. If the description is unclear, keep asking until both sides are talking about the same thing.

### 2. Query Logs

First check `CST_LOG_ACCESS_METHOD`.

If `CST_LOG_ACCESS_METHOD` is already configured, use that method directly and do not ask the user again unless the configuration is missing, ambiguous, or clearly wrong.

If `CST_LOG_ACCESS_METHOD` is not configured, ask the user how the relevant logs should be accessed, then store that method in `config.env` for future runs.

Check the relevant logs first to verify whether the reported symptom actually occurred, when it occurred, which request, task, or job was involved, and what failed around that time.

If multiple log sources are available, ask the user which one is most relevant or authoritative for the issue before proceeding.

### 3. Read Code

Do not assume frontend and backend code live in the same place.

Treat frontend and backend as separate code locations even when they are in the same repository.

If `CST_FRONTEND_CODE_PATH` or `CST_BACKEND_CODE_PATH` is set, use those paths as the authoritative local source locations for this investigation.

If only repository URLs are configured, create or refresh local working copies in locations appropriate for the current environment. Do not assume fixed temporary directories or a universal default branch.

If multiple branches, environments, or code locations could match the reported issue, stop and ask which one reflects the incident before reading code.

Search relevant files in the corresponding frontend and backend locations. Read the frontend entry points, request construction, page logic, and state handling when the symptom is user-facing. Read the backend handlers, services, jobs, and data-processing logic that receive or continue that flow.

When the issue crosses layers, trace the full path from frontend behavior to backend processing and then to database changes, task execution, or external calls. Understand the logic flow that matches the symptom and the log evidence.

### 4. Query Database

Use the configured MySQL access method and credentials from the current shell or local investigation config. Database access is read-only for investigation unless the user explicitly asks for a data repair plan.

If multiple database environments or replicas could match the issue, stop and ask which one is authoritative for the reported incident.

Use database checks to confirm or rule out the hypothesis formed from the logs and code.

### 5. Report Root Cause

Do not stop at a shallow technical conclusion. Explain the result in this structure:

- **Symptoms**: What the user or business side actually observed, including the trigger, visible behavior, and impact window
- **Action**: What needs to be done next, such as whether to compensate data, communicate to product or customer service, keep observing, or create a fix branch
- **Code Problem**: The real code-level issue, logic bug, data-processing bug, configuration bug, or missing guard that caused the symptom
- **Why it happened**: The link between the symptom, the required action, and the code problem
- **Impact**: What product, customer service, and engineering each need to know
- **Evidence**: The key code path, SQL result, log, or record that proves the conclusion

The explanation must be readable to both engineering and product. Avoid reporting only internal implementation details or only surface symptoms.

### 6. Write The Record To Feishu Docs

If `CST_FEISHU_DOC_URL` is configured, append the final investigation summary to that doc after the root cause is clear.

Use a short case heading that includes the current date and a concise summary. If available, include the user identifier, issue window, or ticket number in the heading.

Keep the doc entry readable to product, customer service, and engineering. Reuse the same conclusion structure:

- **Symptoms**
- **Action**
- **Code Problem**
- **Why it happened**
- **Impact**
- **Evidence**

Prefer writing the summary to a temporary markdown file first, then append it with `lark-cli docs +update` in append mode against `CST_FEISHU_DOC_URL`.

If `CST_FEISHU_LOG_TITLE_PREFIX` is set, prepend it to the case heading.

After writing, report one of these outcomes explicitly:

- **Write succeeded**: include the doc URL and note that the case record has been appended
- **Write skipped**: explain why it was intentionally skipped for this case
- **Write failed**: explain whether the likely cause is missing `lark-cli`, missing `lark-cli config init`, missing `lark-cli auth login --recommend`, missing doc permission, or an API/auth error

If the investigation is complete but Feishu write-back fails, do not lose the conclusion. Still show the final report in chat and tell the user the exact next step needed to enable doc logging.

### 7. Decide Whether To Fix

After the cause is clear, ask whether the user wants a fix branch created.

**User confirms**: create a fix branch from the repository and base branch that match the investigated issue, implement the fix in the affected frontend and/or backend code, then commit and push according to the project's normal git workflow.

**User declines**: end the investigation after reporting the final conclusion and next action.

## Completion Signals

The investigation is complete only when all applicable criteria are satisfied:

- The symptom is aligned: user or entity, time window, feature/page, expected behavior, actual behavior, frequency, and current status are known or explicitly unavailable.
- Logs were checked through the configured access method, or the access gap is reported with the exact missing prerequisite.
- Relevant frontend and backend code paths were read and traced for the implicated flow; if one side is not relevant, explain why it was excluded.
- MySQL data was checked when the hypothesis depends on persisted state, or the report explains why database verification was not needed or not available.
- The final report includes **Symptoms**, **Action**, **Code Problem**, **Why it happened**, **Impact**, and **Evidence**.
- The root cause is backed by concrete evidence from logs, code, database records, or a clearly named absence of evidence.
- If Feishu doc logging is enabled, the write-back outcome is reported as succeeded, skipped, or failed with the reason.
- The post-investigation fix decision is recorded: no fix needed, user declined a fix, or the target repo/base branch for a fix has been identified.

Do not close the investigation after only seeing a suspicious log line or only reading one code path. Close it when the symptom, evidence, cause, action, and write-back state all line up.
