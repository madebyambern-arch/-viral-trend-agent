"""
Class Action Claims Administration and Payouts Agent

This agent searches for active class action claims and payouts, tracks changes,
and notifies when claims expire or new payouts are announced.

Features:
- Search for active class action claims
- Track claim expiration dates
- Monitor new payouts
- Daily notifications for changes only
- State persistence to track changes between runs
- CLI with configurable options
- Email notifications via SMTP
"""

import argparse
import json
import os
import smtplib
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict, Any, Optional


# ============================================================================
# CONFIGURATION
# ============================================================================

# Popular class action claims sources/categories
CLAIMS_CATEGORIES = [
    "data_breach",
    "consumer_products",
    "securities",
    "antitrust",
    "employment",
    "insurance",
    "automotive",
    "telecommunications"
]

# Default configuration
DEFAULT_STATE_FILE = "class_action_state.json"
DEFAULT_EXPIRING_WINDOW_DAYS = 30
DEFAULT_RECENT_PAYOUT_WINDOW_DAYS = 30


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class Claim:
    """Represents a class action claim."""
    
    def __init__(self, claim_id: str, title: str, description: str,
                 filing_deadline: datetime, claim_amount: Optional[str],
                 category: str, status: str, claim_url: str):
        self.claim_id = claim_id
        self.title = title
        self.description = description
        self.filing_deadline = filing_deadline
        self.claim_amount = claim_amount
        self.category = category
        self.status = status
        self.claim_url = claim_url
        self.discovered_date = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert claim to dictionary."""
        return {
            "claim_id": self.claim_id,
            "title": self.title,
            "description": self.description,
            "filing_deadline": self.filing_deadline.isoformat() if self.filing_deadline else None,
            "claim_amount": self.claim_amount,
            "category": self.category,
            "status": self.status,
            "claim_url": self.claim_url,
            "discovered_date": self.discovered_date.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Claim':
        """Create claim from dictionary."""
        claim = Claim(
            claim_id=data["claim_id"],
            title=data["title"],
            description=data["description"],
            filing_deadline=datetime.fromisoformat(data["filing_deadline"]) if data.get("filing_deadline") else None,
            claim_amount=data.get("claim_amount"),
            category=data["category"],
            status=data["status"],
            claim_url=data["claim_url"]
        )
        if data.get("discovered_date"):
            claim.discovered_date = datetime.fromisoformat(data["discovered_date"])
        return claim
    
    def is_expiring_soon(self, days: int = 30) -> bool:
        """Check if claim is expiring within specified days."""
        if not self.filing_deadline:
            return False
        days_until_deadline = (self.filing_deadline - datetime.now()).days
        return 0 < days_until_deadline <= days
    
    def is_expired(self) -> bool:
        """Check if claim has expired."""
        if not self.filing_deadline:
            return False
        return datetime.now() > self.filing_deadline


class Payout:
    """Represents a class action payout."""
    
    def __init__(self, payout_id: str, claim_id: str, title: str,
                 amount: str, announcement_date: datetime,
                 distribution_date: Optional[datetime], status: str,
                 payout_url: str):
        self.payout_id = payout_id
        self.claim_id = claim_id
        self.title = title
        self.amount = amount
        self.announcement_date = announcement_date
        self.distribution_date = distribution_date
        self.status = status
        self.payout_url = payout_url
        self.discovered_date = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert payout to dictionary."""
        return {
            "payout_id": self.payout_id,
            "claim_id": self.claim_id,
            "title": self.title,
            "amount": self.amount,
            "announcement_date": self.announcement_date.isoformat(),
            "distribution_date": self.distribution_date.isoformat() if self.distribution_date else None,
            "status": self.status,
            "payout_url": self.payout_url,
            "discovered_date": self.discovered_date.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Payout':
        """Create payout from dictionary."""
        payout = Payout(
            payout_id=data["payout_id"],
            claim_id=data["claim_id"],
            title=data["title"],
            amount=data["amount"],
            announcement_date=datetime.fromisoformat(data["announcement_date"]),
            distribution_date=datetime.fromisoformat(data["distribution_date"]) if data.get("distribution_date") else None,
            status=data["status"],
            payout_url=data["payout_url"]
        )
        if data.get("discovered_date"):
            payout.discovered_date = datetime.fromisoformat(data["discovered_date"])
        return payout


# ============================================================================
# MOCK DATA GENERATOR (Replace with real API/scraper in production)
# ============================================================================

def generate_mock_claims() -> List[Claim]:
    """
    Generate mock class action claims data.
    In production, this would connect to real claims databases or APIs.
    
    Popular sources to integrate:
    - ClassAction.org
    - TopClassActions.com
    - JND Legal Administration
    - Settlement websites
    """
    mock_claims = [
        Claim(
            claim_id="CAC-2024-001",
            title="XYZ Data Breach Settlement",
            description="Settlement for customers affected by 2023 data breach",
            filing_deadline=datetime.now() + timedelta(days=45),
            claim_amount="Up to $500",
            category="data_breach",
            status="active",
            claim_url="https://example.com/xyz-settlement"
        ),
        Claim(
            claim_id="CAC-2024-002",
            title="ABC Electronics Product Defect Settlement",
            description="Settlement for defective smartphone batteries",
            filing_deadline=datetime.now() + timedelta(days=15),
            claim_amount="Up to $350 or replacement",
            category="consumer_products",
            status="active",
            claim_url="https://example.com/abc-settlement"
        ),
        Claim(
            claim_id="CAC-2024-003",
            title="DEF Telecom Overcharging Settlement",
            description="Settlement for customers who were overcharged",
            filing_deadline=datetime.now() + timedelta(days=90),
            claim_amount="Estimated $50-150",
            category="telecommunications",
            status="active",
            claim_url="https://example.com/def-settlement"
        ),
        Claim(
            claim_id="CAC-2023-045",
            title="GHI Auto Airbag Recall Settlement",
            description="Settlement for vehicles with defective airbags",
            filing_deadline=datetime.now() + timedelta(days=5),
            claim_amount="Up to $1,000",
            category="automotive",
            status="active",
            claim_url="https://example.com/ghi-settlement"
        ),
        Claim(
            claim_id="CAC-2023-089",
            title="JKL Insurance Denial Settlement",
            description="Settlement for improperly denied insurance claims",
            filing_deadline=datetime.now() + timedelta(days=120),
            claim_amount="Varies by claim",
            category="insurance",
            status="active",
            claim_url="https://example.com/jkl-settlement"
        ),
    ]
    return mock_claims


def generate_mock_payouts() -> List[Payout]:
    """
    Generate mock payout data.
    In production, this would connect to real payout tracking systems.
    """
    mock_payouts = [
        Payout(
            payout_id="PAY-2024-001",
            claim_id="CAC-2023-025",
            title="MNO Bank Overdraft Fee Settlement Payout",
            amount="$87.5 million total fund",
            announcement_date=datetime.now() - timedelta(days=2),
            distribution_date=datetime.now() + timedelta(days=30),
            status="approved",
            payout_url="https://example.com/mno-payout"
        ),
        Payout(
            payout_id="PAY-2024-002",
            claim_id="CAC-2023-067",
            title="PQR Retailer Price Fixing Settlement Payout",
            amount="$125 million total fund",
            announcement_date=datetime.now() - timedelta(days=1),
            distribution_date=datetime.now() + timedelta(days=45),
            status="approved",
            payout_url="https://example.com/pqr-payout"
        ),
    ]
    return mock_payouts


# ============================================================================
# NOTIFIER INTERFACE AND IMPLEMENTATIONS
# ============================================================================

class Notifier(ABC):
    """Abstract base class for notification systems."""
    
    @abstractmethod
    def send(self, notifications: List[Dict[str, Any]], summary: Dict[str, Any]) -> bool:
        """Send notifications. Returns True if successful."""
        pass


class EmailNotifier(Notifier):
    """Email notifier using SMTP."""
    
    def __init__(self, 
                 smtp_host: Optional[str] = None,
                 smtp_port: Optional[int] = None,
                 smtp_username: Optional[str] = None,
                 smtp_password: Optional[str] = None,
                 smtp_from: Optional[str] = None,
                 smtp_to: Optional[str] = None,
                 use_starttls: bool = True):
        """
        Initialize email notifier with SMTP settings.
        Falls back to environment variables if parameters not provided.
        """
        self.smtp_host = smtp_host or os.environ.get('SMTP_HOST', '')
        self.smtp_port = smtp_port or int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_username = smtp_username or os.environ.get('SMTP_USERNAME', '')
        self.smtp_password = smtp_password or os.environ.get('SMTP_PASSWORD', '')
        self.smtp_from = smtp_from or os.environ.get('SMTP_FROM', '')
        self.smtp_to = smtp_to or os.environ.get('SMTP_TO', '')
        self.use_starttls = use_starttls
        
        # Validate configuration
        if not all([self.smtp_host, self.smtp_from, self.smtp_to]):
            raise ValueError("SMTP_HOST, SMTP_FROM, and SMTP_TO must be configured")
    
    def send(self, notifications: List[Dict[str, Any]], summary: Dict[str, Any]) -> bool:
        """Send email notification with summary of changes."""
        if not notifications:
            # No changes, no email
            return True
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Class Action Claims Alert - {len(notifications)} Update(s)"
            msg['From'] = self.smtp_from
            msg['To'] = self.smtp_to
            
            # Format email body
            body = self._format_email_body(notifications, summary)
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_starttls:
                    server.starttls()
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email notification: {e}")
            return False
    
    def _format_email_body(self, notifications: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
        """Format email body with notification details."""
        lines = []
        lines.append("CLASS ACTION CLAIMS DAILY ALERT")
        lines.append("=" * 70)
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Total Updates: {len(notifications)}")
        lines.append("")
        
        # Group notifications by type
        expiring = [n for n in notifications if n['type'] == 'expiring_claim']
        expired = [n for n in notifications if n['type'] == 'expired_claim']
        new_payouts = [n for n in notifications if n['type'] == 'new_payout']
        
        if expiring:
            lines.append(f"⚠️  EXPIRING CLAIMS ({len(expiring)}):")
            lines.append("-" * 70)
            for notif in expiring:
                lines.append(f"\n• {notif['title']}")
                lines.append(f"  {notif['message']}")
                lines.append(f"  Deadline: {notif['filing_deadline']}")
                lines.append(f"  Amount: {notif['amount']}")
                lines.append(f"  URL: {notif['url']}")
            lines.append("")
        
        if expired:
            lines.append(f"❌ EXPIRED CLAIMS ({len(expired)}):")
            lines.append("-" * 70)
            for notif in expired:
                lines.append(f"\n• {notif['title']}")
                lines.append(f"  Expired: {notif['filing_deadline']}")
                lines.append(f"  URL: {notif['url']}")
            lines.append("")
        
        if new_payouts:
            lines.append(f"💰 NEW PAYOUTS ({len(new_payouts)}):")
            lines.append("-" * 70)
            for notif in new_payouts:
                lines.append(f"\n• {notif['title']}")
                lines.append(f"  Amount: {notif['amount']}")
                lines.append(f"  Announced: {notif['announcement_date']}")
                lines.append(f"  Distribution: {notif['distribution_date']}")
                lines.append(f"  URL: {notif['url']}")
            lines.append("")
        
        lines.append("=" * 70)
        lines.append("This is an automated alert. Updates are sent only when changes occur.")
        
        return "\n".join(lines)


class ConsoleNotifier(Notifier):
    """Console notifier for testing and default behavior."""
    
    def send(self, notifications: List[Dict[str, Any]], summary: Dict[str, Any]) -> bool:
        """Print notifications to console."""
        if not notifications:
            print("✅ NO NEW NOTIFICATIONS - All claims unchanged since last run")
            return True
        
        print(f"\n🔔 {len(notifications)} NOTIFICATION(S):")
        print("=" * 70)
        
        for notif in notifications:
            print(f"\n[{notif['type'].upper()}] {notif['title']}")
            print(f"  {notif['message']}")
            if 'url' in notif:
                print(f"  {notif['url']}")
        
        print("\n" + "=" * 70)
        return True


# ============================================================================
# CLASS ACTION CLAIMS AGENT
# ============================================================================

class ClassActionClaimsAgent:
    """
    Agent to monitor class action claims and payouts.
    Tracks state between runs and notifies only on changes.
    """
    
    def __init__(self, 
                 state_file: Optional[str] = None,
                 expiring_window_days: int = DEFAULT_EXPIRING_WINDOW_DAYS,
                 recent_payout_window_days: int = DEFAULT_RECENT_PAYOUT_WINDOW_DAYS,
                 notifier: Optional[Notifier] = None):
        # Allow state file override via parameter or environment variable
        if state_file is None:
            state_file = os.environ.get('CLASS_ACTION_STATE_FILE', DEFAULT_STATE_FILE)
        
        self.state_file = state_file
        self.expiring_window_days = expiring_window_days
        self.recent_payout_window_days = recent_payout_window_days
        self.notifier = notifier or ConsoleNotifier()
        
        self.current_claims: List[Claim] = []
        self.current_payouts: List[Payout] = []
        self.previous_state: Optional[Dict[str, Any]] = None
        self.notifications: List[Dict[str, Any]] = []
    
    def load_previous_state(self) -> None:
        """Load previous run state from file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    self.previous_state = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load previous state: {e}")
                self.previous_state = None
        else:
            self.previous_state = None
    
    def save_current_state(self) -> None:
        """Save current state to file."""
        state = {
            "last_run": datetime.now().isoformat(),
            "claims": [claim.to_dict() for claim in self.current_claims],
            "payouts": [payout.to_dict() for payout in self.current_payouts],
            "notified_expired_claims": self.previous_state.get("notified_expired_claims", []) if self.previous_state else []
        }
        
        # Add newly expired claims to the notified list
        for notif in self.notifications:
            if notif['type'] == 'expired_claim' and notif['claim_id'] not in state['notified_expired_claims']:
                state['notified_expired_claims'].append(notif['claim_id'])
        
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save state: {e}")
    
    def fetch_active_claims(self) -> List[Claim]:
        """
        Fetch all active class action claims.
        In production, this would use real APIs or web scraping.
        """
        claims = generate_mock_claims()
        
        # Filter for active claims only (not expired)
        active_claims = [claim for claim in claims if not claim.is_expired()]
        
        self.current_claims = active_claims
        return active_claims
    
    def fetch_recent_payouts(self, days: Optional[int] = None) -> List[Payout]:
        """
        Fetch recent payouts announced within specified days.
        In production, this would use real payout tracking APIs.
        """
        if days is None:
            days = self.recent_payout_window_days
            
        payouts = generate_mock_payouts()
        
        # Filter for recent payouts
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_payouts = [
            payout for payout in payouts 
            if payout.announcement_date >= cutoff_date
        ]
        
        self.current_payouts = recent_payouts
        return recent_payouts
    
    def detect_expiring_claims(self, days: Optional[int] = None) -> List[Claim]:
        """Detect claims expiring within specified days."""
        if days is None:
            days = self.expiring_window_days
            
        expiring = []
        
        for claim in self.current_claims:
            if claim.is_expiring_soon(days):
                # Check if this is a newly detected expiring claim
                if self.previous_state:
                    prev_claims = [
                        Claim.from_dict(c) 
                        for c in self.previous_state.get("claims", [])
                    ]
                    prev_claim = next(
                        (c for c in prev_claims if c.claim_id == claim.claim_id),
                        None
                    )
                    
                    # Only notify if claim wasn't previously marked as expiring
                    # or if this is the first run
                    if prev_claim is None or not prev_claim.is_expiring_soon(days):
                        expiring.append(claim)
                else:
                    # First run, include all expiring claims
                    expiring.append(claim)
        
        return expiring
    
    def detect_expired_claims(self) -> List[Claim]:
        """
        Detect claims that have expired since last run.
        This includes:
        1. Claims that were in previous fetch but not current (removed because expired)
        2. Claims that are in current fetch but crossed their deadline since last run
        """
        if not self.previous_state:
            return []
        
        expired = []
        notified_expired = set(self.previous_state.get("notified_expired_claims", []))
        
        # Get previous claims
        prev_claims = [
            Claim.from_dict(c) 
            for c in self.previous_state.get("claims", [])
        ]
        
        # Create lookup dictionaries
        current_claims_by_id = {claim.claim_id: claim for claim in self.current_claims}
        prev_claims_by_id = {claim.claim_id: claim for claim in prev_claims}
        
        # Check all claims from previous state
        for prev_claim in prev_claims:
            # Skip if we already notified about this expiration
            if prev_claim.claim_id in notified_expired:
                continue
            
            # Case 1: Claim was not expired in previous run but is now expired
            if not prev_claim.is_expired() and datetime.now() > prev_claim.filing_deadline:
                expired.append(prev_claim)
            # Case 2: Claim is missing from current fetch and was expired
            elif prev_claim.claim_id not in current_claims_by_id and prev_claim.is_expired():
                expired.append(prev_claim)
        
        # Also check current claims that may have expired since last run
        for claim in self.current_claims:
            # Skip if already notified
            if claim.claim_id in notified_expired:
                continue
                
            # If claim exists in both but was not expired before and is now expired
            if claim.claim_id in prev_claims_by_id:
                prev_claim = prev_claims_by_id[claim.claim_id]
                if not prev_claim.is_expired() and claim.is_expired():
                    # Claim crossed deadline between runs
                    expired.append(claim)
        
        return expired
    
    def detect_new_payouts(self) -> List[Payout]:
        """Detect new payouts since last run."""
        if not self.previous_state:
            # First run, all current payouts are "new"
            return self.current_payouts
        
        new_payouts = []
        prev_payout_ids = {
            p["payout_id"] 
            for p in self.previous_state.get("payouts", [])
        }
        
        for payout in self.current_payouts:
            if payout.payout_id not in prev_payout_ids:
                new_payouts.append(payout)
        
        return new_payouts
    
    def generate_notifications(self) -> List[Dict[str, Any]]:
        """Generate notifications for changes."""
        notifications = []
        
        # Notify about expiring claims
        expiring = self.detect_expiring_claims()
        for claim in expiring:
            days_left = (claim.filing_deadline - datetime.now()).days
            notifications.append({
                "type": "expiring_claim",
                "severity": "high" if days_left <= 7 else "medium",
                "claim_id": claim.claim_id,
                "title": claim.title,
                "message": f"Claim expires in {days_left} days",
                "filing_deadline": claim.filing_deadline.strftime("%Y-%m-%d"),
                "amount": claim.claim_amount,
                "url": claim.claim_url
            })
        
        # Notify about expired claims
        expired = self.detect_expired_claims()
        for claim in expired:
            notifications.append({
                "type": "expired_claim",
                "severity": "info",
                "claim_id": claim.claim_id,
                "title": claim.title,
                "message": "Claim has expired",
                "filing_deadline": claim.filing_deadline.strftime("%Y-%m-%d"),
                "url": claim.claim_url
            })
        
        # Notify about new payouts
        new_payouts = self.detect_new_payouts()
        for payout in new_payouts:
            notifications.append({
                "type": "new_payout",
                "severity": "high",
                "payout_id": payout.payout_id,
                "title": payout.title,
                "message": f"New payout announced: {payout.amount}",
                "announcement_date": payout.announcement_date.strftime("%Y-%m-%d"),
                "distribution_date": payout.distribution_date.strftime("%Y-%m-%d") if payout.distribution_date else "TBD",
                "amount": payout.amount,
                "url": payout.payout_url
            })
        
        self.notifications = notifications
        return notifications
    
    def run(self, skip_report: bool = False) -> Dict[str, Any]:
        """
        Run the agent to check for updates.
        Returns summary of findings and notifications.
        
        Args:
            skip_report: If True, don't write JSON report file
        """
        # Load previous state
        self.load_previous_state()
        
        # Fetch current data
        active_claims = self.fetch_active_claims()
        recent_payouts = self.fetch_recent_payouts()
        
        # Generate notifications for changes
        notifications = self.generate_notifications()
        
        # Send notifications (only if there are changes)
        if notifications:
            self.notifier.send(notifications, {"notifications": notifications})
        
        # Save current state for next run
        self.save_current_state()
        
        # Generate summary
        summary = {
            "run_date": datetime.now().isoformat(),
            "total_active_claims": len(active_claims),
            "total_recent_payouts": len(recent_payouts),
            "notifications_count": len(notifications),
            "notifications": notifications,
            "claims_by_category": self.get_claims_by_category(),
            "expiring_soon": len([c for c in active_claims if c.is_expiring_soon(self.expiring_window_days)])
        }
        
        return summary
    
    def get_claims_by_category(self) -> Dict[str, int]:
        """Get count of claims by category."""
        category_counts = {}
        for claim in self.current_claims:
            category_counts[claim.category] = category_counts.get(claim.category, 0) + 1
        return category_counts
    
    def format_notification_report(self, summary: Dict[str, Any]) -> str:
        """Format notifications as a readable report."""
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("CLASS ACTION CLAIMS AGENT - DAILY REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Summary
        report_lines.append("📊 SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append(f"Total Active Claims: {summary['total_active_claims']}")
        report_lines.append(f"Claims Expiring Soon (30 days): {summary['expiring_soon']}")
        report_lines.append(f"Recent Payouts (30 days): {summary['total_recent_payouts']}")
        report_lines.append(f"Notifications: {summary['notifications_count']}")
        report_lines.append("")
        
        # Notifications
        if summary['notifications']:
            report_lines.append("🔔 NOTIFICATIONS")
            report_lines.append("-" * 80)
            
            # Group by type
            expiring = [n for n in summary['notifications'] if n['type'] == 'expiring_claim']
            expired = [n for n in summary['notifications'] if n['type'] == 'expired_claim']
            new_payouts = [n for n in summary['notifications'] if n['type'] == 'new_payout']
            
            if expiring:
                report_lines.append("\n⚠️  EXPIRING CLAIMS:")
                for notif in expiring:
                    report_lines.append(f"\n  • {notif['title']}")
                    report_lines.append(f"    {notif['message']}")
                    report_lines.append(f"    Deadline: {notif['filing_deadline']}")
                    report_lines.append(f"    Amount: {notif['amount']}")
                    report_lines.append(f"    URL: {notif['url']}")
            
            if expired:
                report_lines.append("\n\n❌ EXPIRED CLAIMS:")
                for notif in expired:
                    report_lines.append(f"\n  • {notif['title']}")
                    report_lines.append(f"    {notif['message']}")
                    report_lines.append(f"    Expired: {notif['filing_deadline']}")
            
            if new_payouts:
                report_lines.append("\n\n💰 NEW PAYOUTS:")
                for notif in new_payouts:
                    report_lines.append(f"\n  • {notif['title']}")
                    report_lines.append(f"    {notif['message']}")
                    report_lines.append(f"    Announced: {notif['announcement_date']}")
                    report_lines.append(f"    Distribution: {notif['distribution_date']}")
                    report_lines.append(f"    URL: {notif['url']}")
        else:
            report_lines.append("✅ NO NEW NOTIFICATIONS")
            report_lines.append("All claims and payouts are unchanged since last run.")
        
        report_lines.append("")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def export_report(self, summary: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Export report to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"class_action_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        return filename


# ============================================================================
# CLI PARSER
# ============================================================================

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Class Action Claims Agent - Monitor claims and payouts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings
  python class_action_claims_agent.py

  # Customize expiring window to 14 days
  python class_action_claims_agent.py --expiring-days 14

  # Use custom state file and report path
  python class_action_claims_agent.py --state-file /tmp/state.json --report-path /tmp/report.json

  # Skip writing report file
  python class_action_claims_agent.py --skip-report

  # Enable email notifications (requires SMTP env vars)
  python class_action_claims_agent.py --notify-email

Environment Variables:
  CLASS_ACTION_STATE_FILE  State file path (default: class_action_state.json)
  SMTP_HOST                SMTP server hostname
  SMTP_PORT                SMTP server port (default: 587)
  SMTP_USERNAME            SMTP username (optional)
  SMTP_PASSWORD            SMTP password (optional)
  SMTP_FROM                From email address
  SMTP_TO                  To email address
        """
    )
    
    parser.add_argument(
        '--state-file',
        type=str,
        default=None,
        help='Path to state file (default: env CLASS_ACTION_STATE_FILE or class_action_state.json)'
    )
    
    parser.add_argument(
        '--report-path',
        type=str,
        default=None,
        help='Path to write JSON report (default: class_action_report_TIMESTAMP.json)'
    )
    
    parser.add_argument(
        '--expiring-days',
        type=int,
        default=DEFAULT_EXPIRING_WINDOW_DAYS,
        help=f'Days window for expiring claims (default: {DEFAULT_EXPIRING_WINDOW_DAYS})'
    )
    
    parser.add_argument(
        '--payout-days',
        type=int,
        default=DEFAULT_RECENT_PAYOUT_WINDOW_DAYS,
        help=f'Days window for recent payouts (default: {DEFAULT_RECENT_PAYOUT_WINDOW_DAYS})'
    )
    
    parser.add_argument(
        '--skip-report',
        action='store_true',
        help='Skip writing JSON report file'
    )
    
    parser.add_argument(
        '--notify-email',
        action='store_true',
        help='Send email notifications (requires SMTP env vars)'
    )
    
    return parser.parse_args()


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main function to run the class action claims agent."""
    args = parse_args()
    
    print("=" * 80)
    print("CLASS ACTION CLAIMS AGENT")
    print("Monitoring Active Claims and Payouts")
    print("=" * 80)
    print()
    
    # Setup notifier
    notifier = None
    if args.notify_email:
        try:
            notifier = EmailNotifier()
            print("📧 Email notifications enabled")
        except ValueError as e:
            print(f"⚠️  Email notification setup failed: {e}")
            print("   Falling back to console notifications")
            notifier = ConsoleNotifier()
    else:
        notifier = ConsoleNotifier()
    
    # Initialize agent
    agent = ClassActionClaimsAgent(
        state_file=args.state_file,
        expiring_window_days=args.expiring_days,
        recent_payout_window_days=args.payout_days,
        notifier=notifier
    )
    
    print(f"📁 State file: {agent.state_file}")
    print(f"⏰ Expiring window: {args.expiring_days} days")
    print(f"💰 Payout window: {args.payout_days} days")
    print()
    
    # Run agent
    print("🔍 Scanning for active claims and payouts...")
    summary = agent.run(skip_report=args.skip_report)
    
    # Display report
    print()
    report = agent.format_notification_report(summary)
    print(report)
    
    # Export report
    if not args.skip_report and summary['notifications']:
        filename = agent.export_report(summary, args.report_path)
        print(f"\n📄 Report exported to: {filename}")
    
    # Display claims by category
    if summary['claims_by_category']:
        print("\n📂 CLAIMS BY CATEGORY")
        print("-" * 80)
        for category, count in sorted(summary['claims_by_category'].items()):
            print(f"  {category}: {count}")
    
    print("\n" + "=" * 80)
    print("✅ AGENT RUN COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
