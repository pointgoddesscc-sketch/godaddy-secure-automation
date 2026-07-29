# GoDaddy Secure Automation

Professional secure GoDaddy domain & DNS automation suite — Python CLI + ready for JavaScript dashboard.

Dry-run by default • Environment-based secrets • Ready for Apple Shortcuts / cron / GitHub Actions / Home Assistant.
Built for business & marketing website operators who manage multiple domains and landing pages.

**Repository:** https://github.com/pointgoddesscc-sketch/godaddy-secure-automation

## Security First

- Never hard-code API keys or passwords.
- Credentials live only in local `.env` (git-ignored) or your OS keychain / CI secrets.
- Default mode is dry-run. Real changes require the explicit `--apply` flag.
- Always test against the GoDaddy OTE (test) environment first.
- This tool never phones home with your secrets.

## Quick Start (Python CLI)

```bash
# 1. Clone
git clone https://github.com/pointgoddesscc-sketch/godaddy-secure-automation.git
cd godaddy-secure-automation

# 2. Install
pip install -r requirements.txt

# 3. Configure (never commit the real .env)
cp .env.example .env
# Edit .env with keys from https://developer.godaddy.com/

# 4. Safe preview
python godaddy_automation.py check
python godaddy_automation.py list
python godaddy_automation.py dns --domain example.com

# 5. When you are ready for real changes
python godaddy_automation.py auto --apply
```

## GitHub Copilot Integration (Ready)

This repository is fully prepared for **GitHub Copilot Chat**, **Agent mode**, and **Spaces**.

### Project Instructions
`.github/copilot-instructions.md` is already present. Copilot will automatically use it when you work inside this repository (VS Code, GitHub.com, JetBrains, etc.).

### Recommended Workflow
1. Open this repo in VS Code (or any supported IDE) with the GitHub Copilot extension.
2. Create a **Copilot Space** that includes:
   - This repository (`godaddy-secure-automation`)
   - Your `meta-agent` repository (system prompt + commands)
   - Optionally `meta-website` / `email-domain-validator` for marketing context
3. In chat, start with:
   ```
   Using the project instructions and Meta-Agent rules, help me add a new DNS rule for my marketing landing page.
   ```
4. Always review generated code. Use OTE keys first. Never paste real secrets into the chat.

### Agent Mode
In supported IDEs you can switch to Agent mode and ask Copilot to:
- Extend the CLI with new validation rules
- Scaffold a secure local Express dashboard (proxy only, no secrets in browser)
- Generate a GitHub Actions workflow for scheduled domain health checks
- Create Apple Shortcut / shortcut payload examples that call a local FastAPI endpoint

Human oversight remains mandatory for every change that touches production domains.

## Next Steps (Professional)

- Add a lightweight FastAPI / Express proxy for device-triggered checks (Apple Shortcuts, Android, Home Assistant).
- Build the secure JavaScript Command Center dashboard (domain health + one-click DNS for campaign launches).
- Wire scheduled GitHub Actions using repository secrets (never store keys in the workflow file itself).
- Connect to your habit / Orgsuite workflows for monthly domain review summaries.

## License
MIT — use freely for your business and client marketing properties.

---

**Your professional domain automation is live and Copilot-ready.**  
Open the repo, load your OTE keys, and start with a dry-run. Everything stays under your control.
