"""
Unit tests for Class Action Claims Agent

Tests cover:
- Expiring claim detection
- Expired claim detection between runs
- New payout detection
- Notification generation (changes only)
- State persistence
- Email notifications (mocked)
"""

import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from class_action_claims_agent import (
    Claim,
    Payout,
    ClassActionClaimsAgent,
    EmailNotifier,
    ConsoleNotifier,
    DEFAULT_EXPIRING_WINDOW_DAYS,
    DEFAULT_RECENT_PAYOUT_WINDOW_DAYS
)


class TestClaim(unittest.TestCase):
    """Test Claim class functionality."""
    
    def test_claim_creation(self):
        """Test creating a claim."""
        claim = Claim(
            claim_id="TEST-001",
            title="Test Claim",
            description="Test description",
            filing_deadline=datetime.now() + timedelta(days=30),
            claim_amount="$100",
            category="test",
            status="active",
            claim_url="https://example.com"
        )
        self.assertEqual(claim.claim_id, "TEST-001")
        self.assertEqual(claim.title, "Test Claim")
    
    def test_claim_is_expiring_soon(self):
        """Test expiring soon detection."""
        # Claim expiring in 15 days
        claim = Claim(
            claim_id="TEST-001",
            title="Test",
            description="Test",
            filing_deadline=datetime.now() + timedelta(days=15),
            claim_amount="$100",
            category="test",
            status="active",
            claim_url="https://example.com"
        )
        self.assertTrue(claim.is_expiring_soon(30))
        self.assertFalse(claim.is_expiring_soon(7))
    
    def test_claim_is_expired(self):
        """Test expired detection."""
        # Expired claim
        claim = Claim(
            claim_id="TEST-001",
            title="Test",
            description="Test",
            filing_deadline=datetime.now() - timedelta(days=1),
            claim_amount="$100",
            category="test",
            status="expired",
            claim_url="https://example.com"
        )
        self.assertTrue(claim.is_expired())
    
    def test_claim_to_dict_from_dict(self):
        """Test serialization and deserialization."""
        claim = Claim(
            claim_id="TEST-001",
            title="Test Claim",
            description="Test description",
            filing_deadline=datetime.now() + timedelta(days=30),
            claim_amount="$100",
            category="test",
            status="active",
            claim_url="https://example.com"
        )
        
        claim_dict = claim.to_dict()
        restored_claim = Claim.from_dict(claim_dict)
        
        self.assertEqual(claim.claim_id, restored_claim.claim_id)
        self.assertEqual(claim.title, restored_claim.title)


class TestPayout(unittest.TestCase):
    """Test Payout class functionality."""
    
    def test_payout_creation(self):
        """Test creating a payout."""
        payout = Payout(
            payout_id="PAY-001",
            claim_id="TEST-001",
            title="Test Payout",
            amount="$1M",
            announcement_date=datetime.now(),
            distribution_date=datetime.now() + timedelta(days=30),
            status="approved",
            payout_url="https://example.com"
        )
        self.assertEqual(payout.payout_id, "PAY-001")
        self.assertEqual(payout.title, "Test Payout")
    
    def test_payout_to_dict_from_dict(self):
        """Test serialization and deserialization."""
        payout = Payout(
            payout_id="PAY-001",
            claim_id="TEST-001",
            title="Test Payout",
            amount="$1M",
            announcement_date=datetime.now(),
            distribution_date=datetime.now() + timedelta(days=30),
            status="approved",
            payout_url="https://example.com"
        )
        
        payout_dict = payout.to_dict()
        restored_payout = Payout.from_dict(payout_dict)
        
        self.assertEqual(payout.payout_id, restored_payout.payout_id)
        self.assertEqual(payout.title, restored_payout.title)


class TestClassActionClaimsAgent(unittest.TestCase):
    """Test ClassActionClaimsAgent functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.temp_dir, "test_state.json")
        self.agent = ClassActionClaimsAgent(state_file=self.state_file)
    
    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
        os.rmdir(self.temp_dir)
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.state_file, self.state_file)
        self.assertEqual(self.agent.expiring_window_days, DEFAULT_EXPIRING_WINDOW_DAYS)
        self.assertEqual(self.agent.recent_payout_window_days, DEFAULT_RECENT_PAYOUT_WINDOW_DAYS)
        self.assertIsInstance(self.agent.notifier, ConsoleNotifier)
    
    def test_state_persistence(self):
        """Test state file save and load."""
        # Create mock claims
        self.agent.current_claims = [
            Claim(
                claim_id="TEST-001",
                title="Test Claim",
                description="Test",
                filing_deadline=datetime.now() + timedelta(days=30),
                claim_amount="$100",
                category="test",
                status="active",
                claim_url="https://example.com"
            )
        ]
        
        # Save state
        self.agent.save_current_state()
        self.assertTrue(os.path.exists(self.state_file))
        
        # Load state in new agent
        new_agent = ClassActionClaimsAgent(state_file=self.state_file)
        new_agent.load_previous_state()
        
        self.assertIsNotNone(new_agent.previous_state)
        self.assertEqual(len(new_agent.previous_state['claims']), 1)
        self.assertEqual(new_agent.previous_state['claims'][0]['claim_id'], "TEST-001")
    
    def test_detect_expiring_claims_first_run(self):
        """Test expiring claim detection on first run."""
        # First run - no previous state
        self.agent.current_claims = [
            Claim(
                claim_id="TEST-001",
                title="Test Claim",
                description="Test",
                filing_deadline=datetime.now() + timedelta(days=15),
                claim_amount="$100",
                category="test",
                status="active",
                claim_url="https://example.com"
            )
        ]
        
        expiring = self.agent.detect_expiring_claims()
        self.assertEqual(len(expiring), 1)
        self.assertEqual(expiring[0].claim_id, "TEST-001")
    
    def test_detect_expiring_claims_no_duplicates(self):
        """Test that expiring claims are only notified once."""
        # Create a claim expiring in 15 days
        claim = Claim(
            claim_id="TEST-001",
            title="Test Claim",
            description="Test",
            filing_deadline=datetime.now() + timedelta(days=15),
            claim_amount="$100",
            category="test",
            status="active",
            claim_url="https://example.com"
        )
        
        # First run - should detect as expiring
        self.agent.current_claims = [claim]
        expiring1 = self.agent.detect_expiring_claims()
        self.assertEqual(len(expiring1), 1)
        
        # Save state
        self.agent.save_current_state()
        
        # Second run - claim still expiring but already notified
        new_agent = ClassActionClaimsAgent(state_file=self.state_file)
        new_agent.load_previous_state()
        new_agent.current_claims = [claim]
        expiring2 = new_agent.detect_expiring_claims()
        
        # Should not detect again
        self.assertEqual(len(expiring2), 0)
    
    def test_detect_expired_claims_crossing_deadline(self):
        """Test detecting claims that crossed deadline between runs."""
        # First run - claim not expired yet (deadline in future)
        claim_deadline = datetime.now() + timedelta(days=1)
        claim = Claim(
            claim_id="TEST-001",
            title="Test Claim",
            description="Test",
            filing_deadline=claim_deadline,
            claim_amount="$100",
            category="test",
            status="active",
            claim_url="https://example.com"
        )
        
        self.agent.current_claims = [claim]
        self.agent.save_current_state()
        
        # Second run - claim now expired (simulate deadline passed)
        new_agent = ClassActionClaimsAgent(state_file=self.state_file)
        new_agent.load_previous_state()
        
        # Create claim with past deadline
        expired_claim = Claim(
            claim_id="TEST-001",
            title="Test Claim",
            description="Test",
            filing_deadline=datetime.now() - timedelta(days=1),  # Now expired
            claim_amount="$100",
            category="test",
            status="active",
            claim_url="https://example.com"
        )
        new_agent.current_claims = [expired_claim]
        
        expired = new_agent.detect_expired_claims()
        self.assertEqual(len(expired), 1)
        self.assertEqual(expired[0].claim_id, "TEST-001")
    
    def test_detect_expired_claims_no_duplicates(self):
        """Test that expired claims are only notified once."""
        # First run - claim expires
        claim = Claim(
            claim_id="TEST-001",
            title="Test Claim",
            description="Test",
            filing_deadline=datetime.now() - timedelta(days=1),
            claim_amount="$100",
            category="test",
            status="expired",
            claim_url="https://example.com"
        )
        
        self.agent.current_claims = [claim]
        expired1 = self.agent.detect_expired_claims()
        # First run has no previous state, so no expired detected
        self.assertEqual(len(expired1), 0)
        
        # Generate notifications and save (this marks as notified)
        self.agent.notifications = [{
            'type': 'expired_claim',
            'claim_id': 'TEST-001',
            'title': 'Test Claim'
        }]
        self.agent.save_current_state()
        
        # Second run - should not notify again
        new_agent = ClassActionClaimsAgent(state_file=self.state_file)
        new_agent.load_previous_state()
        new_agent.current_claims = []  # Claim removed from feed
        
        expired2 = new_agent.detect_expired_claims()
        self.assertEqual(len(expired2), 0)  # Already notified
    
    def test_detect_new_payouts(self):
        """Test new payout detection."""
        # First run - one payout
        payout1 = Payout(
            payout_id="PAY-001",
            claim_id="TEST-001",
            title="Payout 1",
            amount="$1M",
            announcement_date=datetime.now(),
            distribution_date=None,
            status="approved",
            payout_url="https://example.com"
        )
        
        self.agent.current_payouts = [payout1]
        new_payouts1 = self.agent.detect_new_payouts()
        
        # First run - all payouts are "new"
        self.assertEqual(len(new_payouts1), 1)
        
        # Save state
        self.agent.save_current_state()
        
        # Second run - add another payout
        payout2 = Payout(
            payout_id="PAY-002",
            claim_id="TEST-002",
            title="Payout 2",
            amount="$2M",
            announcement_date=datetime.now(),
            distribution_date=None,
            status="approved",
            payout_url="https://example.com"
        )
        
        new_agent = ClassActionClaimsAgent(state_file=self.state_file)
        new_agent.load_previous_state()
        new_agent.current_payouts = [payout1, payout2]
        
        new_payouts2 = new_agent.detect_new_payouts()
        self.assertEqual(len(new_payouts2), 1)
        self.assertEqual(new_payouts2[0].payout_id, "PAY-002")
    
    def test_generate_notifications_changes_only(self):
        """Test that notifications are only generated for changes."""
        # First run
        claim = Claim(
            claim_id="TEST-001",
            title="Test Claim",
            description="Test",
            filing_deadline=datetime.now() + timedelta(days=15),
            claim_amount="$100",
            category="test",
            status="active",
            claim_url="https://example.com"
        )
        
        self.agent.current_claims = [claim]
        self.agent.current_payouts = []
        notifications1 = self.agent.generate_notifications()
        
        # Should have notifications on first run
        self.assertGreater(len(notifications1), 0)
        
        # Save state
        self.agent.save_current_state()
        
        # Second run - same data
        new_agent = ClassActionClaimsAgent(state_file=self.state_file)
        new_agent.load_previous_state()
        new_agent.current_claims = [claim]
        new_agent.current_payouts = []
        notifications2 = new_agent.generate_notifications()
        
        # Should have no notifications (no changes)
        self.assertEqual(len(notifications2), 0)


class TestEmailNotifier(unittest.TestCase):
    """Test EmailNotifier functionality."""
    
    def test_email_notifier_initialization(self):
        """Test email notifier initialization."""
        with patch.dict(os.environ, {
            'SMTP_HOST': 'smtp.example.com',
            'SMTP_PORT': '587',
            'SMTP_FROM': 'from@example.com',
            'SMTP_TO': 'to@example.com'
        }):
            notifier = EmailNotifier()
            self.assertEqual(notifier.smtp_host, 'smtp.example.com')
            self.assertEqual(notifier.smtp_port, 587)
            self.assertEqual(notifier.smtp_from, 'from@example.com')
            self.assertEqual(notifier.smtp_to, 'to@example.com')
    
    def test_email_notifier_missing_config(self):
        """Test email notifier fails with missing config."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                EmailNotifier()
    
    @patch('smtplib.SMTP')
    def test_email_notifier_send(self, mock_smtp):
        """Test sending email notifications."""
        # Setup mock SMTP
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        with patch.dict(os.environ, {
            'SMTP_HOST': 'smtp.example.com',
            'SMTP_PORT': '587',
            'SMTP_FROM': 'from@example.com',
            'SMTP_TO': 'to@example.com',
            'SMTP_USERNAME': 'user',
            'SMTP_PASSWORD': 'pass'
        }):
            notifier = EmailNotifier()
            
            notifications = [{
                'type': 'expiring_claim',
                'severity': 'high',
                'title': 'Test Claim',
                'message': 'Expiring soon',
                'filing_deadline': '2026-02-01',
                'amount': '$100',
                'url': 'https://example.com'
            }]
            
            result = notifier.send(notifications, {'notifications': notifications})
            
            # Should succeed
            self.assertTrue(result)
            
            # Verify SMTP was called
            mock_smtp.assert_called_once_with('smtp.example.com', 587)
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with('user', 'pass')
            mock_server.send_message.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_email_notifier_no_send_on_empty(self, mock_smtp):
        """Test that no email is sent when there are no notifications."""
        with patch.dict(os.environ, {
            'SMTP_HOST': 'smtp.example.com',
            'SMTP_FROM': 'from@example.com',
            'SMTP_TO': 'to@example.com'
        }):
            notifier = EmailNotifier()
            result = notifier.send([], {'notifications': []})
            
            # Should return True but not send email
            self.assertTrue(result)
            mock_smtp.assert_not_called()


class TestConsoleNotifier(unittest.TestCase):
    """Test ConsoleNotifier functionality."""
    
    def test_console_notifier_send(self):
        """Test console notifier."""
        notifier = ConsoleNotifier()
        
        notifications = [{
            'type': 'expiring_claim',
            'title': 'Test Claim',
            'message': 'Expiring soon',
            'url': 'https://example.com'
        }]
        
        result = notifier.send(notifications, {'notifications': notifications})
        self.assertTrue(result)
    
    def test_console_notifier_empty(self):
        """Test console notifier with no notifications."""
        notifier = ConsoleNotifier()
        result = notifier.send([], {'notifications': []})
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
