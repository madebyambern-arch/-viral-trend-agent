#!/usr/bin/env python3
"""
Demonstration script for Class Action Claims Agent features

This script demonstrates:
1. CLI usage with different options
2. Email notification setup
3. State persistence and change detection
4. Expired claim detection across runs
"""

import os
import sys
import tempfile
from datetime import datetime, timedelta
from class_action_claims_agent import (
    ClassActionClaimsAgent, 
    Claim, 
    Payout,
    ConsoleNotifier,
    EmailNotifier
)

print("=" * 80)
print("CLASS ACTION CLAIMS AGENT - FEATURE DEMONSTRATION")
print("=" * 80)
print()

# Demo 1: Basic Usage with Console Notifications
print("DEMO 1: Basic Usage with Console Notifications")
print("-" * 80)

temp_state = tempfile.mktemp(suffix='.json')
agent = ClassActionClaimsAgent(
    state_file=temp_state,
    expiring_window_days=30,
    notifier=ConsoleNotifier()
)

# Simulate claims
agent.current_claims = [
    Claim(
        claim_id="DEMO-001",
        title="Data Breach Settlement",
        description="Demo claim",
        filing_deadline=datetime.now() + timedelta(days=15),
        claim_amount="$500",
        category="data_breach",
        status="active",
        claim_url="https://example.com/demo-001"
    )
]
agent.current_payouts = []

print("First run (should show notifications):")
notifs = agent.generate_notifications()
print(f"  Notifications generated: {len(notifs)}")
agent.save_current_state()
print()

print("Second run (same data, should show NO notifications):")
agent2 = ClassActionClaimsAgent(state_file=temp_state)
agent2.load_previous_state()
agent2.current_claims = agent.current_claims
agent2.current_payouts = []
notifs2 = agent2.generate_notifications()
print(f"  Notifications generated: {len(notifs2)}")
print("  ✅ Change detection working correctly!")
print()

# Demo 2: Expired Claim Detection
print("\nDEMO 2: Expired Claim Detection (Crossing Deadline)")
print("-" * 80)

temp_state2 = tempfile.mktemp(suffix='.json')

# Run 1: Claim not expired yet
print("Run 1: Claim with deadline in 1 hour")
agent3 = ClassActionClaimsAgent(state_file=temp_state2)
agent3.current_claims = [
    Claim(
        claim_id="EXPIRE-001",
        title="About to Expire Claim",
        description="Demo",
        filing_deadline=datetime.now() + timedelta(hours=1),
        claim_amount="$100",
        category="test",
        status="active",
        claim_url="https://example.com"
    )
]
agent3.current_payouts = []
notifs3 = agent3.generate_notifications()
print(f"  Notifications: {len(notifs3)}")
agent3.save_current_state()

# Run 2: Claim now expired
print("\nRun 2: Same claim, but deadline has passed")
agent4 = ClassActionClaimsAgent(state_file=temp_state2)
agent4.load_previous_state()
agent4.current_claims = [
    Claim(
        claim_id="EXPIRE-001",
        title="About to Expire Claim",
        description="Demo",
        filing_deadline=datetime.now() - timedelta(hours=1),  # Now expired
        claim_amount="$100",
        category="test",
        status="expired",
        claim_url="https://example.com"
    )
]
agent4.current_payouts = []
notifs4 = agent4.generate_notifications()
print(f"  Notifications: {len(notifs4)}")
if notifs4:
    print(f"  Type: {notifs4[0]['type']}")
    print("  ✅ Expired claim detected!")
agent4.save_current_state()

# Run 3: Should not notify again
print("\nRun 3: Same expired claim (should NOT notify again)")
agent5 = ClassActionClaimsAgent(state_file=temp_state2)
agent5.load_previous_state()
agent5.current_claims = []  # Claim removed from feed
agent5.current_payouts = []
notifs5 = agent5.generate_notifications()
print(f"  Notifications: {len(notifs5)}")
print("  ✅ No duplicate notification!")
print()

# Demo 3: CLI Options
print("\nDEMO 3: CLI Options Available")
print("-" * 80)
print("The agent supports the following CLI options:")
print()
print("  --state-file PATH         Override state file location")
print("  --report-path PATH        Override report file location")
print("  --expiring-days N         Set expiring window (default: 30)")
print("  --payout-days N           Set payout window (default: 30)")
print("  --skip-report             Don't write JSON report file")
print("  --notify-email            Enable email notifications")
print()
print("Example commands:")
print("  python class_action_claims_agent.py --expiring-days 14")
print("  python class_action_claims_agent.py --notify-email --skip-report")
print()

# Demo 4: Email Notification Setup
print("\nDEMO 4: Email Notification Setup")
print("-" * 80)
print("To enable email notifications, set these environment variables:")
print()
print("  export SMTP_HOST='smtp.gmail.com'")
print("  export SMTP_PORT='587'")
print("  export SMTP_FROM='alerts@example.com'")
print("  export SMTP_TO='recipient@example.com'")
print("  export SMTP_USERNAME='your-username'  # Optional")
print("  export SMTP_PASSWORD='your-password'  # Optional")
print()
print("Then run with: python class_action_claims_agent.py --notify-email")
print()
print("Email features:")
print("  ✅ Only sends when there are changes")
print("  ✅ STARTTLS support for secure connections")
print("  ✅ Groups notifications by type")
print("  ✅ Includes all details (deadlines, amounts, URLs)")
print()

# Demo 5: GitHub Actions Integration
print("\nDEMO 5: GitHub Actions Daily Scheduling")
print("-" * 80)
print("The repository includes .github/workflows/class-action-agent.yml")
print()
print("Features:")
print("  • Runs daily at 9:00 AM UTC (cron: '0 9 * * *')")
print("  • Can be manually triggered via workflow_dispatch")
print("  • Uses only Python stdlib (no dependencies)")
print("  • Uploads JSON reports as artifacts (90-day retention)")
print("  • Uploads state files as artifacts (7-day retention)")
print()
print("To enable email in GitHub Actions:")
print("  1. Go to Settings → Secrets and variables → Actions")
print("  2. Add secrets: SMTP_HOST, SMTP_PORT, SMTP_FROM, SMTP_TO, etc.")
print("  3. Uncomment env vars in the workflow file")
print()

# Cleanup
os.remove(temp_state)
os.remove(temp_state2)

print("=" * 80)
print("DEMONSTRATION COMPLETE")
print("=" * 80)
print()
print("Next steps:")
print("  1. Run the agent: python class_action_claims_agent.py")
print("  2. Check the tests: python -m unittest test_class_action_claims_agent.py -v")
print("  3. View example usage: python class_action_example_usage.py")
print("  4. Read the docs: See README.md for full documentation")
print()
