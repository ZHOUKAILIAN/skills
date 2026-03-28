---
name: cst
description: |
  Use when investigating a customer service issue that requires reading the repo, checking MySQL data, identifying the real root cause, and explaining both symptoms and the underlying problem in language product and engineering can both understand.
---

# Customer Service Troubleshooting (CST)

## First Use
Ask for git repo URL, mysql host/user/password. Create `config.env` and ask user to `export $(cat config.env | grep -v '^#' | xargs)`

## Workflow

### 1. Pull Repo
Repo at `/tmp/cst-repo/`. If exists: `cd /tmp/cst-repo && git checkout master && git pull origin master`. If not: `git clone "$CST_GIT_REPO" /tmp/cst-repo`

### 2. Understand Issue
Ask clarifying questions if needed (user, time, error messages, etc.)

### 3. Read Code
Search relevant files with `rg` or `Glob`. Understand the logic flow.

### 4. Query Database
`mysql -h "$CST_MYSQL_HOST" -P "$CST_MYSQL_PORT" -u "$CST_MYSQL_USER" -p"$CST_MYSQL_PASSWORD"` (READ ONLY)

### 5. Report Root Cause
Do not stop at a shallow technical conclusion. Explain the result in this structure:

- **Symptoms**: What the user or business side actually observed, including the trigger, visible behavior, and impact window
- **Problem**: The real root cause in code, data, configuration, or process
- **Why it happened**: The link between the symptom and the root cause
- **Impact**: What product, customer service, and engineering each need to know
- **Evidence**: The key code path, SQL result, log, or record that proves the conclusion

The explanation must be readable to both engineering and product. Avoid reporting only internal implementation details or only surface symptoms.

**User confirms**: `cd /tmp/cst-repo && git checkout master && git checkout -b fix/cst-[issue]-[date]`, implement fix, commit and push

**User declines**: end workflow
