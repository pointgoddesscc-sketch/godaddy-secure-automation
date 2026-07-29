# GoDaddy Secure Automation — Copilot Instructions

You are assisting with the professional GoDaddy domain & DNS automation suite.

## Core Context
This repository provides:
- Python CLI (`godaddy_automation.py`) for secure, local domain health checks, DNS listing, and controlled updates.
- Dry-run by default. Real changes require explicit `--apply`.
- Credentials loaded only from environment / `.env` (never hard-coded).
- Designed for business & marketing website operators who manage multiple domains.

## Rules for All Suggestions
1. Never hard-code API keys, secrets, passwords, or personal domains.
2. Always prefer dry-run / validation-first patterns.
3. Use official GoDaddy API only (`https://api.godaddy.com/v1` or OTE).
4. Auth header format: `Authorization: sso-key KEY:SECRET`
5. Produce production-ready, well-commented code with logging.
6. For JavaScript dashboard work: clean ES modules, accessibility, silent analytics, professional UI (Tailwind-friendly).
7. Remind the user that human review and testing (especially in OTE) are mandatory before production use.
8. Align with Meta-Agent system prompt (see meta-agent repo) when generating website-related code.

## Preferred Stack
- Python 3 + requests + python-dotenv for CLI automation
- Node.js + Express + axios for any local secure dashboard proxy
- Cron / GitHub Actions / Apple Shortcuts for scheduling
- Never store secrets in repo or chat

## Response Style
Professional, structured with headings and bullet lists. Ready-to-copy code blocks. Business-oriented language suitable for marketing teams managing domains and landing pages.
