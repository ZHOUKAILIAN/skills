---
name: customer-service-troubleshoot
description: |
  Customer service issue troubleshooting. Workflow: read repo (pull master) → query database → find root cause → report to user → create fix branch only if user confirms.
commands:
  - /cst
  - /troubleshoot
  - /fix
---

# Customer Service Troubleshooting

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
Explain what caused the issue clearly.

**User confirms**: `cd /tmp/cst-repo && git checkout master && git checkout -b fix/cst-[issue]-[date]`, implement fix, commit and push

**User declines**: end workflow
