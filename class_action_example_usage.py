"""
Example Usage Guide for Class Action Claims Agent

This file demonstrates how to use the ClassActionClaimsAgent
in practical scenarios. Each example is beginner-friendly with comments.
"""

from class_action_claims_agent import ClassActionClaimsAgent, Claim, Payout
from datetime import datetime, timedelta

print("=" * 70)
print("CLASS ACTION CLAIMS AGENT - EXAMPLE USAGE")
print("=" * 70)
print()

# ============================================================================
# EXAMPLE 1: Basic Usage - Run the Agent
# ============================================================================

print("EXAMPLE 1: Basic Usage - Run the Claims Agent")
print("-" * 70)

# Step 1: Create an agent instance
agent = ClassActionClaimsAgent()
print("✓ Created ClassActionClaimsAgent instance\n")

# Step 2: Run the agent
print("Running agent to scan for claims and payouts...")
summary = agent.run()

print(f"✓ Scan complete!")
print(f"  • Total active claims: {summary['total_active_claims']}")
print(f"  • Claims expiring soon: {summary['expiring_soon']}")
print(f"  • Recent payouts: {summary['total_recent_payouts']}")
print(f"  • Notifications: {summary['notifications_count']}")
print()

# ============================================================================
# EXAMPLE 2: Display Notifications
# ============================================================================

print("EXAMPLE 2: Display Notifications")
print("-" * 70)

if summary['notifications']:
    print(f"Found {len(summary['notifications'])} notification(s):\n")
    
    for notif in summary['notifications']:
        print(f"  [{notif['type'].upper()}] - {notif['severity'].upper()}")
        print(f"  Title: {notif['title']}")
        print(f"  Message: {notif['message']}")
        print(f"  URL: {notif.get('url', 'N/A')}")
        print()
else:
    print("✓ No new notifications - all claims unchanged\n")

print()

# ============================================================================
# EXAMPLE 3: Get Detailed Report
# ============================================================================

print("EXAMPLE 3: Get Formatted Report")
print("-" * 70)

report = agent.format_notification_report(summary)
print("\nFormatted Report Preview (first 500 chars):")
print(report[:500])
print("...\n")

print()

# ============================================================================
# EXAMPLE 4: Export Report to File
# ============================================================================

print("EXAMPLE 4: Export Report to JSON File")
print("-" * 70)

filename = agent.export_report(summary, "example_report.json")
print(f"✓ Report exported to: {filename}\n")

print()

# ============================================================================
# EXAMPLE 5: Access Specific Claims Data
# ============================================================================

print("EXAMPLE 5: Access Active Claims Details")
print("-" * 70)

active_claims = agent.current_claims

if active_claims:
    print(f"Found {len(active_claims)} active claim(s):\n")
    
    for claim in active_claims[:3]:  # Show first 3
        print(f"  📋 {claim.title}")
        print(f"     Category: {claim.category}")
        print(f"     Amount: {claim.claim_amount}")
        print(f"     Deadline: {claim.filing_deadline.strftime('%Y-%m-%d')}")
        
        days_left = (claim.filing_deadline - datetime.now()).days
        if claim.is_expiring_soon(30):
            print(f"     ⚠️  EXPIRING SOON: {days_left} days left")
        else:
            print(f"     Days remaining: {days_left}")
        
        print(f"     URL: {claim.claim_url}")
        print()

print()

# ============================================================================
# EXAMPLE 6: Access Payout Information
# ============================================================================

print("EXAMPLE 6: Access Recent Payouts")
print("-" * 70)

recent_payouts = agent.current_payouts

if recent_payouts:
    print(f"Found {len(recent_payouts)} recent payout(s):\n")
    
    for payout in recent_payouts:
        print(f"  💰 {payout.title}")
        print(f"     Amount: {payout.amount}")
        print(f"     Announced: {payout.announcement_date.strftime('%Y-%m-%d')}")
        if payout.distribution_date:
            print(f"     Distribution: {payout.distribution_date.strftime('%Y-%m-%d')}")
        print(f"     Status: {payout.status}")
        print(f"     URL: {payout.payout_url}")
        print()
else:
    print("No recent payouts found.\n")

print()

# ============================================================================
# EXAMPLE 7: Filter Claims by Category
# ============================================================================

print("EXAMPLE 7: Filter Claims by Category")
print("-" * 70)

categories = agent.get_claims_by_category()

print("Claims by category:")
for category, count in sorted(categories.items()):
    category_claims = [c for c in agent.current_claims if c.category == category]
    print(f"\n  📁 {category}: {count} claim(s)")
    for claim in category_claims:
        print(f"     • {claim.title}")

print()
print()

# ============================================================================
# EXAMPLE 8: Custom Filtering - High Priority Claims
# ============================================================================

print("EXAMPLE 8: Find High Priority Claims (Expiring in 7 days)")
print("-" * 70)

high_priority = [
    claim for claim in agent.current_claims 
    if claim.is_expiring_soon(7)
]

if high_priority:
    print(f"Found {len(high_priority)} high priority claim(s):\n")
    
    for claim in high_priority:
        days_left = (claim.filing_deadline - datetime.now()).days
        print(f"  🚨 {claim.title}")
        print(f"     URGENT: {days_left} days remaining!")
        print(f"     Amount: {claim.claim_amount}")
        print(f"     Deadline: {claim.filing_deadline.strftime('%Y-%m-%d')}")
        print(f"     URL: {claim.claim_url}")
        print()
else:
    print("No high priority claims found.\n")

print()

# ============================================================================
# EXAMPLE 9: Simulating Daily Runs
# ============================================================================

print("EXAMPLE 9: Simulating Daily Run Behavior")
print("-" * 70)

print("""
On first run, the agent will:
  1. Fetch all active claims
  2. Identify claims expiring within 30 days
  3. Find recent payouts
  4. Send notifications for ALL findings
  5. Save state to class_action_state.json

On subsequent runs (daily), the agent will:
  1. Load previous state
  2. Fetch current claims and payouts
  3. Compare with previous state
  4. Only notify on CHANGES:
     • New claims becoming "expiring soon"
     • Claims that expired since last run
     • Newly announced payouts
  5. Update state file

To test this behavior:
  • Run the agent once (first run)
  • Run it again immediately (should show no notifications)
  • Delete class_action_state.json and run again (back to first run)
""")

print()

# ============================================================================
# EXAMPLE 10: Programmatic Usage in Your Application
# ============================================================================

print("EXAMPLE 10: Integration Example")
print("-" * 70)

print("""
Example integration with notification systems:

```python
from class_action_claims_agent import ClassActionClaimsAgent
import smtplib
from email.mime.text import MIMEText

def send_email_notification(notification):
    # Your email sending logic here
    pass

# Run agent
agent = ClassActionClaimsAgent()
summary = agent.run()

# Process notifications
for notif in summary['notifications']:
    if notif['severity'] == 'high':
        # Send urgent notification
        send_email_notification(notif)
    
    # Log to database
    # db.save_notification(notif)
    
    # Send to Slack/Discord
    # slack.post_message(notif['message'])
```

Other integration ideas:
  • Email alerts for expiring claims
  • SMS notifications for high-value payouts
  • Slack/Discord webhooks
  • Database logging
  • Dashboard visualization
  • Calendar integration
""")

print()
print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 70)
print("EXAMPLES COMPLETE!")
print("=" * 70)
print("""
You've now learned how to:
1. ✓ Create and run a ClassActionClaimsAgent
2. ✓ Access and display notifications
3. ✓ Generate formatted reports
4. ✓ Export data to JSON files
5. ✓ Access claims and payout details
6. ✓ Filter claims by category
7. ✓ Find high-priority claims
8. ✓ Understand daily run behavior
9. ✓ Integrate with your applications

Next Steps:
- Replace mock data with real API/scraper integration
- Set up daily cron job or scheduled task
- Add email/SMS notification delivery
- Integrate with your notification platform
- Customize expiration thresholds
- Add web dashboard for visualization

Resources:
- ClassAction.org API (if available)
- TopClassActions.com scraping
- JND Legal Administration updates
- Settlement website monitoring

Happy monitoring! 🔍
""")
