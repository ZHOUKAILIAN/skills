---
name: cst
description: |
  Use when investigating a customer service issue that requires aligning on the observed symptoms first, checking the relevant logs the user provides access to, reading the relevant frontend and backend code, verifying MySQL data, identifying the real root cause, and explaining both symptoms and the underlying problem in language product and engineering can both understand.
---

# Customer Service Troubleshooting (CST)

## First Use

First check whether the current shell already has the required environment variables for git access, database access, and log access.

Treat frontend code location and backend code location as separate inputs. Do not assume they live in the same directory or the same repository.

Prefer a named log access method in `CST_LOG_ACCESS_METHOD`. If it is already set, use it as the default log-query method for this investigation.

If the relevant environment variables are already present, confirm they are the right ones to use for this investigation and only ask the user for anything that is still missing.

If required values are missing, ask for the frontend code location, the backend code location, mysql host/user/password, the log-query method the user already uses, and any log-related connection details or credentials required to use it.

Create or update `config.env`, write both database and log-related environment variables into it, and ask user to `export $(cat config.env | grep -v '^#' | xargs)`.

If the chosen log access method needs credentials, endpoints, project names, logstore names, cluster context, tokens, or other connection details, put them in `config.env` with clear variable names before querying logs.

If `CST_LOG_ACCESS_METHOD=aliyun-cli`, use `aliyun-cli` directly and keep its required credentials in environment variables. Prefer:

- `ALIBABA_CLOUD_ACCESS_KEY_ID`
- `ALIBABA_CLOUD_ACCESS_KEY_SECRET`
- `ALIBABA_CLOUD_REGION_ID`
- `ALIBABA_CLOUD_SECURITY_TOKEN` (optional, if using STS)

If `CST_LOG_ACCESS_METHOD` is set to another value, use that method and the corresponding environment variables or connection details instead.

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

If frontend and backend are in different repositories, keep them in separate working directories such as `/tmp/cst-frontend-repo/` and `/tmp/cst-backend-repo/`.

If they are in the same repository, still treat them as different code locations and use separate path hints such as `CST_FRONTEND_CODE_PATH` and `CST_BACKEND_CODE_PATH`.

Frontend repo: if `CST_FRONTEND_GIT_REPO` is set and `/tmp/cst-frontend-repo/` exists, `cd /tmp/cst-frontend-repo && git checkout master && git pull origin master`. If it is set and the directory does not exist, `git clone "$CST_FRONTEND_GIT_REPO" /tmp/cst-frontend-repo`

Backend repo: if `CST_BACKEND_GIT_REPO` is set and `/tmp/cst-backend-repo/` exists, `cd /tmp/cst-backend-repo && git checkout master && git pull origin master`. If it is set and the directory does not exist, `git clone "$CST_BACKEND_GIT_REPO" /tmp/cst-backend-repo`

Treat the code path as potentially split across frontend code and backend code.

Search relevant files with `rg` or `Glob` in the corresponding frontend and backend locations. Read the frontend entry points, request construction, page logic, and state handling when the symptom is user-facing. Read the backend handlers, services, jobs, and data-processing logic that receive or continue that flow.

When the issue crosses layers, trace the full path from frontend behavior to backend processing and then to database changes, task execution, or external calls. Understand the logic flow that matches the symptom and the log evidence.

### 4. Query Database

`mysql -h "$CST_MYSQL_HOST" -P "$CST_MYSQL_PORT" -u "$CST_MYSQL_USER" -p"$CST_MYSQL_PASSWORD"` (READ ONLY)

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

### 6. Decide Whether To Fix

After the cause is clear, ask whether the user wants a fix branch created.

**User confirms**: `cd /tmp/cst-repo && git checkout master && git checkout -b fix/cst-[issue]-[date]`, implement fix, commit and push

**User declines**: end workflow
