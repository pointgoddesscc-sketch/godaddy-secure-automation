#!/usr/bin/env python3
"""
GoDaddy + Email Automation Suite
Built for professional domain & DNS management on YOUR machine.

This is the real, working automation.
It runs LOCALLY on YOUR machine or home server with YOUR credentials (loaded securely from .env).

It CANNOT run inside this chat or have persistent login to your accounts.
You run it. It does the work. You stay in control.

Features:
- Secure API access to GoDaddy (no passwords ever shared)
- List domains, check status, DNS records
- Update DNS records safely (dry-run by default)
- "Auto mode" for hands-off operation: check everything, apply your rules, log results
- Optional email notification stub (add your own IMAP/SMTP logic)
- Easy to trigger from Apple Shortcuts, Android, Home Assistant, cron, etc.
- Human-readable logs + habit-friendly summaries

How to use:
1. pip install -r requirements.txt
2. cp .env.example .env   then edit .env with your real keys (from developer.godaddy.com)
3. python godaddy_automation.py --help
4. Start with: python godaddy_automation.py check --dry-run
5. When ready: python godaddy_automation.py auto --apply

For true "set and forget": 
- Run via cron/systemd timer every hour/day
- Or add a small web server (Flask/FastAPI) and call from your devices
- Or use the schedule library inside this script for simple internal loops

Security promise: This script never phones home with your secrets. Everything stays on your machine.
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import requests

# ============== SETUP ==============
load_dotenv()  # Loads .env file from same directory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("godaddy_automation.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load credentials securely
GODADDY_KEY = os.getenv("GODADDY_API_KEY")
GODADDY_SECRET = os.getenv("GODADDY_API_SECRET")
BASE_URL = os.getenv("GODADDY_BASE_URL", "https://api.ote.godaddy.com/v1")
DOMAINS_ENV = os.getenv("DOMAINS_TO_MANAGE", "")

if not GODADDY_KEY or not GODADDY_SECRET:
    logger.error("Missing GODADDY_API_KEY or GODADDY_API_SECRET in .env file")
    logger.error("Get them at https://developer.godaddy.com/  (start with OTE/test keys)")
    sys.exit(1)

HEADERS = {
    "Authorization": f"sso-key {GODADDY_KEY}:{GODADDY_SECRET}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# ============== GODADDY CLIENT ==============
class GoDaddyClient:
    def __init__(self):
        self.base_url = BASE_URL.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        logger.info(f"GoDaddy client initialized | Base: {self.base_url}")

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            resp = self.session.request(method, url, timeout=30, **kwargs)
            if resp.status_code >= 400:
                logger.error(f"API {method} {endpoint} failed: {resp.status_code} {resp.text}")
            resp.raise_for_status()
            return resp.json() if resp.content else {}
        except Exception as e:
            logger.exception(f"Request error: {e}")
            raise

    def list_domains(self) -> List[Dict[str, Any]]:
        logger.info("Fetching all domains...")
        return self._request("GET", "/domains")

    def get_domain_info(self, domain: str) -> Dict[str, Any]:
        return self._request("GET", f"/domains/{domain}")

    def get_dns_records(self, domain: str) -> List[Dict[str, Any]]:
        return self._request("GET", f"/domains/{domain}/records")

    def update_dns_record(self, domain: str, record_type: str, name: str, records: List[Dict[str, Any]], dry_run: bool = True) -> Optional[Dict[str, Any]]:
        endpoint = f"/domains/{domain}/records/{record_type}/{name}"
        if dry_run:
            logger.info(f"[DRY RUN] Would update {domain} {record_type} {name} → {records}")
            return None
        logger.info(f"Updating DNS: {domain} {record_type} {name}")
        return self._request("PUT", endpoint, json=records)

    def check_expiring_soon(self, days: int = 30) -> List[Dict[str, Any]]:
        """Simple helper: returns domains expiring within X days (basic version)."""
        domains = self.list_domains()
        expiring = []
        for d in domains:
            # GoDaddy API returns expires date in some responses; this is simplified
            if "expires" in d:
                try:
                    exp_date = datetime.fromisoformat(d["expires"].replace("Z", "+00:00"))
                    if (exp_date - datetime.now()).days <= days:
                        expiring.append(d)
                except Exception:
                    pass
        return expiring

# ============== AUTOMATION LOGIC ==============
def run_domain_check(client: GoDaddyClient, apply_changes: bool = False):
    """Core 'make everything correct' check."""
    logger.info("=== Starting Domain Health Check ===")
    domains = client.list_domains()
    logger.info(f"Found {len(domains)} domains in account")

    for domain_data in domains:
        domain = domain_data.get("domain", "unknown")
        logger.info(f"\n--- Checking {domain} ---")
        try:
            info = client.get_domain_info(domain)
            logger.info(f"Status: {info.get('status', 'N/A')} | Expires: {info.get('expires', 'N/A')}")

            records = client.get_dns_records(domain)
            logger.info(f"DNS records count: {len(records)}")
            # Example: You can add your own rules here
            # e.g. if certain record is missing or wrong → update it

        except Exception as e:
            logger.error(f"Error checking {domain}: {e}")

    # Example auto-action (commented — customize to your needs)
    # if apply_changes:
    #     client.update_dns_record("example.com", "A", "www", [{"data": "203.0.113.50", "ttl": 3600}], dry_run=False)

    logger.info("=== Domain Check Complete ===")

def run_auto_mode(client: GoDaddyClient, apply_changes: bool = False):
    """The 'do everything automatically' mode you wanted."""
    logger.info("=== AUTO MODE: Full hands-off run ===")
    run_domain_check(client, apply_changes=apply_changes)

    # Add your custom rules here:
    # - Check for expiring domains and alert
    # - Enforce specific DNS settings for certain domains
    # - Parse renewal emails (add IMAP code below)
    # - Call your home webhook if something changed

    logger.info("Auto mode finished. Check godaddy_automation.log for details.")

# ============== EMAIL STUB (Secure - you add the real logic) ==============
def check_email_and_act():
    """
    Placeholder for email automation.
    To activate:
    1. Add your IMAP details to .env
    2. Uncomment and implement real IMAP login using imaplib + app password
    3. Parse specific emails (e.g. GoDaddy renewal notices)
    4. Trigger domain API actions based on email content
    Never hardcode passwords. Never run this with main account password.
    """
    logger.info("Email check placeholder — add your secure IMAP logic here if needed.")
    # Example skeleton (do not use without proper secrets handling):
    # import imaplib
    # mail = imaplib.IMAP4_SSL(os.getenv("EMAIL_IMAP_SERVER"))
    # mail.login(os.getenv("EMAIL_IMAP_USER"), os.getenv("EMAIL_IMAP_APP_PASSWORD"))
    # ... search, fetch, act ...

# ============== CLI ==============
def main():
    parser = argparse.ArgumentParser(
        description="GoDaddy Automation — built to run correctly and securely on YOUR machine"
    )
    parser.add_argument("mode", choices=["check", "auto", "list", "dns"], 
                        help="check = health check, auto = full automatic run, list = list domains, dns = show DNS")
    parser.add_argument("--domain", help="Specific domain for dns action")
    parser.add_argument("--apply", action="store_true", help="Actually make changes (default is dry-run safe mode)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview only (safe default)")

    args = parser.parse_args()
    dry_run = not args.apply   # --apply turns off dry-run

    client = GoDaddyClient()

    if args.mode == "list":
        domains = client.list_domains()
        print(json.dumps(domains, indent=2))

    elif args.mode == "check":
        run_domain_check(client, apply_changes=args.apply)

    elif args.mode == "auto":
        run_auto_mode(client, apply_changes=args.apply)

    elif args.mode == "dns":
        if not args.domain:
            print("Please provide --domain example.com")
            sys.exit(1)
        records = client.get_dns_records(args.domain)
        print(json.dumps(records, indent=2))

    # Optional: call email check
    # check_email_and_act()

if __name__ == "__main__":
    main()
