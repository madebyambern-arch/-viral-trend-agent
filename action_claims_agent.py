"""
Action Claims Agent Module

A lightweight agent for tracking action claims, monitoring payouts, and sending
notifications about claim expirations and new payouts.

Features:
- Data models for claims and payouts
- Pluggable scraping/API integration interfaces
- State persistence with JSON storage
- Payout tracking and change detection
- Notification system with email support
- Scheduling capability for GitHub Actions
- CLI interface for manual and scheduled runs
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Protocol, Tuple
from abc import ABC, abstractmethod
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Payout:
    """Represents a payout associated with a claim."""
    payout_id: str
    amount: float
    currency: str = "USD"
    announced_date: Optional[datetime] = None
    processed_date: Optional[datetime] = None
    status: str = "pending"  # pending, processing, completed
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with datetime handling."""
        data = asdict(self)
        if self.announced_date:
            data['announced_date'] = self.announced_date.isoformat()
        if self.processed_date:
            data['processed_date'] = self.processed_date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Payout':
        """Create from dictionary with datetime parsing."""
        if 'announced_date' in data and data['announced_date']:
            data['announced_date'] = datetime.fromisoformat(data['announced_date'])
        if 'processed_date' in data and data['processed_date']:
            data['processed_date'] = datetime.fromisoformat(data['processed_date'])
        return cls(**data)


@dataclass
class Claim:
    """Represents an action claim with tracking information."""
    claim_id: str
    name: str
    source: str
    status: str = "active"  # active, expired, completed
    is_active: bool = True
    expiration_date: Optional[datetime] = None
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)
    payouts: List[Payout] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if claim has expired."""
        if not self.expiration_date:
            return False
        return datetime.now() > self.expiration_date
    
    def add_payout(self, payout: Payout) -> None:
        """Add a payout to this claim."""
        self.payouts.append(payout)
        self.updated_date = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with datetime handling."""
        data = asdict(self)
        if self.expiration_date:
            data['expiration_date'] = self.expiration_date.isoformat()
        data['created_date'] = self.created_date.isoformat()
        data['updated_date'] = self.updated_date.isoformat()
        data['payouts'] = [p.to_dict() for p in self.payouts]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Claim':
        """Create from dictionary with datetime parsing."""
        if 'expiration_date' in data and data['expiration_date']:
            data['expiration_date'] = datetime.fromisoformat(data['expiration_date'])
        if 'created_date' in data:
            data['created_date'] = datetime.fromisoformat(data['created_date'])
        if 'updated_date' in data:
            data['updated_date'] = datetime.fromisoformat(data['updated_date'])
        
        # Convert payouts
        payouts_data = data.get('payouts', [])
        data['payouts'] = [Payout.from_dict(p) for p in payouts_data]
        
        return cls(**data)


# ============================================================================
# SCRAPING/API INTERFACES
# ============================================================================

class ClaimsDataSource(Protocol):
    """Protocol for claims data sources (scrapers, API clients)."""
    
    def fetch_claims(self) -> List[Claim]:
        """Fetch claims from the data source."""
        ...
    
    def normalize_data(self, raw_data: Any) -> List[Claim]:
        """Normalize raw data into Claim objects."""
        ...


class BaseClaimsClient(ABC):
    """Abstract base class for claims data clients."""
    
    @abstractmethod
    def fetch_claims(self) -> List[Claim]:
        """Fetch claims from the data source."""
        pass
    
    @abstractmethod
    def normalize_data(self, raw_data: Any) -> List[Claim]:
        """Normalize raw data into Claim objects."""
        pass
    
    def filter_active_claims(self, claims: List[Claim]) -> List[Claim]:
        """Filter for only active, non-expired claims."""
        return [
            claim for claim in claims
            if claim.is_active and not claim.is_expired()
        ]


class StubClaimsClient(BaseClaimsClient):
    """Stub implementation of claims client for testing/demonstration."""
    
    def __init__(self):
        self.mock_data = self._generate_mock_data()
    
    def _generate_mock_data(self) -> List[Dict[str, Any]]:
        """Generate mock claims data."""
        return [
            {
                "id": "CLAIM001",
                "name": "Action Claim Alpha",
                "source": "SourceA",
                "expiration": (datetime.now() + timedelta(days=30)).isoformat(),
                "active": True,
                "payouts": [
                    {
                        "id": "PAY001",
                        "amount": 100.00,
                        "date": datetime.now().isoformat()
                    }
                ]
            },
            {
                "id": "CLAIM002",
                "name": "Action Claim Beta",
                "source": "SourceB",
                "expiration": (datetime.now() + timedelta(days=15)).isoformat(),
                "active": True,
                "payouts": []
            },
            {
                "id": "CLAIM003",
                "name": "Action Claim Gamma",
                "source": "SourceA",
                "expiration": (datetime.now() - timedelta(days=5)).isoformat(),
                "active": True,
                "payouts": [
                    {
                        "id": "PAY002",
                        "amount": 250.00,
                        "date": (datetime.now() - timedelta(days=10)).isoformat()
                    }
                ]
            },
        ]
    
    def fetch_claims(self) -> List[Claim]:
        """Fetch mock claims data."""
        return self.normalize_data(self.mock_data)
    
    def normalize_data(self, raw_data: List[Dict[str, Any]]) -> List[Claim]:
        """Normalize raw mock data into Claim objects."""
        claims = []
        for item in raw_data:
            # Parse payouts
            payouts = []
            for payout_data in item.get("payouts", []):
                payout = Payout(
                    payout_id=payout_data["id"],
                    amount=payout_data["amount"],
                    announced_date=datetime.fromisoformat(payout_data["date"]),
                    status="completed"
                )
                payouts.append(payout)
            
            # Create claim
            claim = Claim(
                claim_id=item["id"],
                name=item["name"],
                source=item["source"],
                is_active=item["active"],
                expiration_date=datetime.fromisoformat(item["expiration"]),
                payouts=payouts
            )
            
            # Update status based on expiration
            if claim.is_expired():
                claim.status = "expired"
                claim.is_active = False
            
            claims.append(claim)
        
        return claims


# ============================================================================
# STATE TRACKING
# ============================================================================

class StateManager:
    """Manages state persistence for claims tracking."""
    
    def __init__(self, state_file: str = "claims_state.json"):
        self.state_file = Path(state_file)
        self.state: Dict[str, Any] = {}
    
    def load_state(self) -> Dict[str, Any]:
        """Load state from JSON file."""
        if not self.state_file.exists():
            self.state = {
                "last_run": None,
                "claims": {},
                "previous_claims": {}
            }
            return self.state
        
        try:
            with open(self.state_file, 'r') as f:
                data = json.load(f)
                self.state = data
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading state: {e}")
            self.state = {
                "last_run": None,
                "claims": {},
                "previous_claims": {}
            }
            return self.state
    
    def save_state(self, claims: List[Claim]) -> None:
        """Save current state to JSON file."""
        # Move current claims to previous
        current_claims = self.state.get("claims", {})
        
        # Create new state
        new_state = {
            "last_run": datetime.now().isoformat(),
            "claims": {claim.claim_id: claim.to_dict() for claim in claims},
            "previous_claims": current_claims
        }
        
        self.state = new_state
        
        # Ensure directory exists
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file
        with open(self.state_file, 'w') as f:
            json.dump(new_state, f, indent=2)
    
    def get_previous_claims(self) -> Dict[str, Claim]:
        """Get claims from previous run (from loaded 'claims' field)."""
        # Previous claims are what were in 'claims' field when state was loaded
        previous = self.state.get("claims", {})
        return {
            claim_id: Claim.from_dict(data)
            for claim_id, data in previous.items()
        }
    
    def detect_changes(self, current_claims: List[Claim]) -> Dict[str, Any]:
        """Detect changes between current and previous claims."""
        previous_claims = self.get_previous_claims()
        current_claims_dict = {claim.claim_id: claim for claim in current_claims}
        
        changes = {
            "new_claims": [],
            "expired_claims": [],
            "new_payouts": []  # Will be list of tuples (claim, payout_dict)
        }
        
        # Check for new claims
        for claim_id, claim in current_claims_dict.items():
            if claim_id not in previous_claims:
                changes["new_claims"].append(claim)
        
        # Check for expired claims and new payouts
        for claim_id, previous_claim in previous_claims.items():
            current_claim = current_claims_dict.get(claim_id)
            
            if not current_claim:
                continue
            
            # Check if newly expired
            if not previous_claim.is_expired() and current_claim.is_expired():
                changes["expired_claims"].append(current_claim)
            
            # Check for new payouts
            previous_payout_ids = {p.payout_id for p in previous_claim.payouts}
            for payout in current_claim.payouts:
                if payout.payout_id not in previous_payout_ids:
                    # Store tuple of (claim, payout_dict) to avoid serialization issues
                    changes["new_payouts"].append((current_claim, payout.to_dict()))
        
        return changes


# ============================================================================
# NOTIFICATION SYSTEM
# ============================================================================

class Notifier(ABC):
    """Abstract base class for notification systems."""
    
    @abstractmethod
    def send_notification(self, subject: str, message: str) -> bool:
        """Send a notification."""
        pass


class EmailNotifier(Notifier):
    """Email notification implementation."""
    
    def __init__(
        self,
        smtp_host: str = "smtp.gmail.com",
        smtp_port: int = 587,
        sender_email: str = "",
        sender_password: str = "",
        recipient_email: str = ""
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email
    
    def send_notification(self, subject: str, message: str) -> bool:
        """Send an email notification."""
        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            print("Email configuration incomplete. Skipping email notification.")
            print(f"Would send: {subject}")
            print(message)
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✓ Email notification sent: {subject}")
            return True
        
        except Exception as e:
            print(f"✗ Failed to send email notification: {e}")
            return False
    
    def format_changes_notification(self, changes: Dict[str, List[Claim]]) -> Tuple[Optional[str], Optional[str]]:
        """Format changes into email subject and body."""
        # Count changes
        total_changes = (
            len(changes.get("expired_claims", [])) +
            len(changes.get("new_payouts", []))
        )
        
        if total_changes == 0:
            return None, None
        
        # Create subject
        subject = f"Action Claims Alert: {total_changes} Change(s) Detected"
        
        # Create body
        body_parts = ["Action Claims Agent - Change Detection Report\n"]
        body_parts.append("=" * 60)
        body_parts.append("")
        
        # Expired claims
        expired = changes.get("expired_claims", [])
        if expired:
            body_parts.append(f"🔴 EXPIRED CLAIMS ({len(expired)}):")
            body_parts.append("-" * 60)
            for claim in expired:
                body_parts.append(f"  • {claim.name} (ID: {claim.claim_id})")
                body_parts.append(f"    Source: {claim.source}")
                body_parts.append(f"    Expired: {claim.expiration_date.strftime('%Y-%m-%d %H:%M')}")
                body_parts.append("")
        
        # New payouts
        new_payouts = changes.get("new_payouts", [])
        if new_payouts:
            body_parts.append(f"💰 NEW PAYOUTS ({len(new_payouts)}):")
            body_parts.append("-" * 60)
            for item in new_payouts:
                # new_payouts is now a list of tuples (claim, payout_dict)
                if isinstance(item, tuple):
                    claim, payout_data = item
                else:
                    # Backwards compatibility: claim with metadata
                    claim = item
                    payout_data = claim.metadata.get("new_payout")
                
                if payout_data:
                    # Handle both dict and Payout object
                    if isinstance(payout_data, dict):
                        amount = payout_data.get('amount', 0)
                        currency = payout_data.get('currency', 'USD')
                        announced_date_str = payout_data.get('announced_date')
                        if announced_date_str and isinstance(announced_date_str, str):
                            announced_date = datetime.fromisoformat(announced_date_str)
                        else:
                            announced_date = None
                    else:
                        amount = payout_data.amount
                        currency = payout_data.currency
                        announced_date = payout_data.announced_date
                    
                    body_parts.append(f"  • {claim.name} (ID: {claim.claim_id})")
                    body_parts.append(f"    Payout: ${amount:.2f} {currency}")
                    body_parts.append(f"    Announced: {announced_date.strftime('%Y-%m-%d %H:%M') if announced_date else 'N/A'}")
                    body_parts.append("")
        
        body_parts.append("=" * 60)
        body_parts.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return subject, "\n".join(body_parts)


class ConsoleNotifier(Notifier):
    """Console notification implementation (for testing)."""
    
    def send_notification(self, subject: str, message: str) -> bool:
        """Print notification to console."""
        print("\n" + "=" * 80)
        print(f"NOTIFICATION: {subject}")
        print("=" * 80)
        print(message)
        print("=" * 80 + "\n")
        return True


# ============================================================================
# MAIN AGENT CLASS
# ============================================================================

class ActionClaimsAgent:
    """
    Main agent class for tracking action claims and payouts.
    
    Coordinates data fetching, state management, change detection,
    and notifications.
    """
    
    def __init__(
        self,
        data_client: BaseClaimsClient,
        state_file: str = "claims_state.json",
        notifier: Optional[Notifier] = None
    ):
        self.data_client = data_client
        self.state_manager = StateManager(state_file)
        self.notifier = notifier or ConsoleNotifier()
    
    def run(self) -> Dict[str, Any]:
        """
        Execute a single run of the claims agent.
        
        Returns:
            Dictionary containing run results and statistics.
        """
        print("=" * 80)
        print("ACTION CLAIMS AGENT - RUN STARTED")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Load previous state
        print("📂 Loading previous state...")
        self.state_manager.load_state()
        print("✓ State loaded\n")
        
        # Fetch current claims
        print("🔍 Fetching claims data...")
        all_claims = self.data_client.fetch_claims()
        print(f"✓ Fetched {len(all_claims)} total claims\n")
        
        # Filter for active claims
        print("🔎 Filtering active claims...")
        active_claims = self.data_client.filter_active_claims(all_claims)
        print(f"✓ Found {len(active_claims)} active claims\n")
        
        # Detect changes
        print("🔄 Detecting changes...")
        changes = self.state_manager.detect_changes(all_claims)
        print(f"✓ Detected changes:")
        print(f"  • New claims: {len(changes['new_claims'])}")
        print(f"  • Expired claims: {len(changes['expired_claims'])}")
        print(f"  • New payouts: {len(changes['new_payouts'])}\n")
        
        # Send notifications if there are changes
        expired_count = len(changes['expired_claims'])
        payout_count = len(changes['new_payouts'])
        
        if expired_count > 0 or payout_count > 0:
            print("📧 Preparing notifications...")
            
            if isinstance(self.notifier, EmailNotifier):
                subject, message = self.notifier.format_changes_notification(changes)
                if subject and message:
                    self.notifier.send_notification(subject, message)
            else:
                # Console notifier
                if expired_count > 0:
                    exp_msg = f"Expired Claims: {', '.join(c.name for c in changes['expired_claims'])}"
                    self.notifier.send_notification("Expired Claims Detected", exp_msg)
                
                if payout_count > 0:
                    # Extract claim names from tuples
                    claim_names = []
                    for item in changes['new_payouts']:
                        if isinstance(item, tuple):
                            claim_names.append(item[0].name)
                        else:
                            claim_names.append(item.name)
                    payout_msg = f"New Payouts: {', '.join(claim_names)}"
                    self.notifier.send_notification("New Payouts Detected", payout_msg)
        else:
            print("ℹ️  No changes detected, skipping notifications\n")
        
        # Save current state
        print("💾 Saving state...")
        self.state_manager.save_state(all_claims)
        print(f"✓ State saved to: {self.state_manager.state_file}\n")
        
        # Prepare results
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_claims": len(all_claims),
            "active_claims": len(active_claims),
            "expired_claims": len(changes['expired_claims']),
            "new_payouts": len(changes['new_payouts']),
            "changes": changes
        }
        
        print("=" * 80)
        print("ACTION CLAIMS AGENT - RUN COMPLETED")
        print("=" * 80)
        
        return results


if __name__ == "__main__":
    # Example usage
    print("Action Claims Agent - Example Run\n")
    
    # Create stub client
    client = StubClaimsClient()
    
    # Create agent with console notifier
    agent = ActionClaimsAgent(
        data_client=client,
        state_file="claims_state.json",
        notifier=ConsoleNotifier()
    )
    
    # Run the agent
    results = agent.run()
    
    print("\n📊 SUMMARY:")
    print(f"  Total Claims: {results['total_claims']}")
    print(f"  Active Claims: {results['active_claims']}")
    print(f"  Expired Claims: {results['expired_claims']}")
    print(f"  New Payouts: {results['new_payouts']}")
