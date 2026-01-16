"""
Tests for Action Claims Agent

Comprehensive test suite covering:
- Claim and payout data models
- State persistence and change detection
- Notification logic
- Expiration tracking
- Client interfaces
"""

import unittest
import json
import tempfile
import os
from datetime import datetime, timedelta
from pathlib import Path
from action_claims_agent import (
    Claim,
    Payout,
    StubClaimsClient,
    StateManager,
    ActionClaimsAgent,
    ConsoleNotifier,
    EmailNotifier
)


class TestPayoutModel(unittest.TestCase):
    """Test the Payout data model."""
    
    def test_payout_creation(self):
        """Test creating a payout."""
        payout = Payout(
            payout_id="PAY001",
            amount=100.50,
            currency="USD",
            status="pending"
        )
        self.assertEqual(payout.payout_id, "PAY001")
        self.assertEqual(payout.amount, 100.50)
        self.assertEqual(payout.currency, "USD")
        self.assertEqual(payout.status, "pending")
    
    def test_payout_to_dict(self):
        """Test converting payout to dictionary."""
        payout = Payout(
            payout_id="PAY001",
            amount=100.50,
            announced_date=datetime(2024, 1, 1, 12, 0, 0)
        )
        data = payout.to_dict()
        self.assertEqual(data['payout_id'], "PAY001")
        self.assertEqual(data['amount'], 100.50)
        self.assertEqual(data['announced_date'], "2024-01-01T12:00:00")
    
    def test_payout_from_dict(self):
        """Test creating payout from dictionary."""
        data = {
            'payout_id': "PAY001",
            'amount': 100.50,
            'currency': "USD",
            'announced_date': "2024-01-01T12:00:00",
            'processed_date': None,
            'status': "pending",
            'metadata': {}
        }
        payout = Payout.from_dict(data)
        self.assertEqual(payout.payout_id, "PAY001")
        self.assertEqual(payout.amount, 100.50)
        self.assertIsInstance(payout.announced_date, datetime)


class TestClaimModel(unittest.TestCase):
    """Test the Claim data model."""
    
    def test_claim_creation(self):
        """Test creating a claim."""
        claim = Claim(
            claim_id="CLAIM001",
            name="Test Claim",
            source="TestSource",
            status="active"
        )
        self.assertEqual(claim.claim_id, "CLAIM001")
        self.assertEqual(claim.name, "Test Claim")
        self.assertEqual(claim.source, "TestSource")
        self.assertTrue(claim.is_active)
    
    def test_claim_expiration_future(self):
        """Test claim with future expiration."""
        future_date = datetime.now() + timedelta(days=30)
        claim = Claim(
            claim_id="CLAIM001",
            name="Future Claim",
            source="TestSource",
            expiration_date=future_date
        )
        self.assertFalse(claim.is_expired())
    
    def test_claim_expiration_past(self):
        """Test claim with past expiration."""
        past_date = datetime.now() - timedelta(days=5)
        claim = Claim(
            claim_id="CLAIM001",
            name="Expired Claim",
            source="TestSource",
            expiration_date=past_date
        )
        self.assertTrue(claim.is_expired())
    
    def test_claim_add_payout(self):
        """Test adding payout to claim."""
        claim = Claim(
            claim_id="CLAIM001",
            name="Test Claim",
            source="TestSource"
        )
        payout = Payout(payout_id="PAY001", amount=100.0)
        claim.add_payout(payout)
        self.assertEqual(len(claim.payouts), 1)
        self.assertEqual(claim.payouts[0].payout_id, "PAY001")
    
    def test_claim_to_dict(self):
        """Test converting claim to dictionary."""
        claim = Claim(
            claim_id="CLAIM001",
            name="Test Claim",
            source="TestSource",
            expiration_date=datetime(2024, 12, 31, 23, 59, 59)
        )
        data = claim.to_dict()
        self.assertEqual(data['claim_id'], "CLAIM001")
        self.assertEqual(data['name'], "Test Claim")
        self.assertIn('expiration_date', data)
    
    def test_claim_from_dict(self):
        """Test creating claim from dictionary."""
        data = {
            'claim_id': "CLAIM001",
            'name': "Test Claim",
            'source': "TestSource",
            'status': "active",
            'is_active': True,
            'expiration_date': "2024-12-31T23:59:59",
            'created_date': datetime.now().isoformat(),
            'updated_date': datetime.now().isoformat(),
            'payouts': [],
            'metadata': {}
        }
        claim = Claim.from_dict(data)
        self.assertEqual(claim.claim_id, "CLAIM001")
        self.assertEqual(claim.name, "Test Claim")
        self.assertIsInstance(claim.expiration_date, datetime)


class TestStubClaimsClient(unittest.TestCase):
    """Test the stub claims client."""
    
    def test_fetch_claims(self):
        """Test fetching claims from stub client."""
        client = StubClaimsClient()
        claims = client.fetch_claims()
        self.assertGreater(len(claims), 0)
        self.assertIsInstance(claims[0], Claim)
    
    def test_filter_active_claims(self):
        """Test filtering for active claims."""
        client = StubClaimsClient()
        all_claims = client.fetch_claims()
        active_claims = client.filter_active_claims(all_claims)
        
        # All active claims should not be expired
        for claim in active_claims:
            self.assertTrue(claim.is_active)
            self.assertFalse(claim.is_expired())
    
    def test_normalize_data(self):
        """Test data normalization."""
        client = StubClaimsClient()
        raw_data = [{
            "id": "TEST001",
            "name": "Test Claim",
            "source": "TestSource",
            "expiration": (datetime.now() + timedelta(days=30)).isoformat(),
            "active": True,
            "payouts": []
        }]
        claims = client.normalize_data(raw_data)
        self.assertEqual(len(claims), 1)
        self.assertEqual(claims[0].claim_id, "TEST001")


class TestStateManager(unittest.TestCase):
    """Test state management and persistence."""
    
    def setUp(self):
        """Create temporary state file for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.temp_dir, "test_state.json")
    
    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
        os.rmdir(self.temp_dir)
    
    def test_load_state_new_file(self):
        """Test loading state when file doesn't exist."""
        manager = StateManager(self.state_file)
        state = manager.load_state()
        self.assertIsNotNone(state)
        self.assertIn('claims', state)
        self.assertIn('previous_claims', state)
    
    def test_save_and_load_state(self):
        """Test saving and loading state."""
        manager = StateManager(self.state_file)
        
        # Create test claims
        claims = [
            Claim(claim_id="CLAIM001", name="Test 1", source="Source1"),
            Claim(claim_id="CLAIM002", name="Test 2", source="Source2")
        ]
        
        # Save state
        manager.save_state(claims)
        self.assertTrue(os.path.exists(self.state_file))
        
        # Load state
        manager2 = StateManager(self.state_file)
        state = manager2.load_state()
        self.assertEqual(len(state['claims']), 2)
        self.assertIn('CLAIM001', state['claims'])
    
    def test_detect_new_claims(self):
        """Test detection of new claims."""
        manager = StateManager(self.state_file)
        
        # First run - no previous state
        claims1 = [
            Claim(claim_id="CLAIM001", name="Test 1", source="Source1")
        ]
        manager.save_state(claims1)
        
        # Second run - with new claim
        manager.load_state()
        claims2 = [
            Claim(claim_id="CLAIM001", name="Test 1", source="Source1"),
            Claim(claim_id="CLAIM002", name="Test 2", source="Source2")
        ]
        changes = manager.detect_changes(claims2)
        
        self.assertEqual(len(changes['new_claims']), 1)
        self.assertEqual(changes['new_claims'][0].claim_id, "CLAIM002")
    
    def test_detect_expired_claims(self):
        """Test detection of newly expired claims."""
        manager = StateManager(self.state_file)
        
        # First run - claim not expired
        future_date = datetime.now() + timedelta(days=1)
        claims1 = [
            Claim(
                claim_id="CLAIM001",
                name="Test 1",
                source="Source1",
                expiration_date=future_date
            )
        ]
        manager.save_state(claims1)
        
        # Second run - claim expired
        manager.load_state()
        past_date = datetime.now() - timedelta(days=1)
        claims2 = [
            Claim(
                claim_id="CLAIM001",
                name="Test 1",
                source="Source1",
                expiration_date=past_date
            )
        ]
        changes = manager.detect_changes(claims2)
        
        self.assertEqual(len(changes['expired_claims']), 1)
        self.assertEqual(changes['expired_claims'][0].claim_id, "CLAIM001")
    
    def test_detect_new_payouts(self):
        """Test detection of new payouts."""
        manager = StateManager(self.state_file)
        
        # First run - claim without payout
        claims1 = [
            Claim(claim_id="CLAIM001", name="Test 1", source="Source1")
        ]
        manager.save_state(claims1)
        
        # Second run - claim with new payout
        manager.load_state()
        claim_with_payout = Claim(
            claim_id="CLAIM001",
            name="Test 1",
            source="Source1"
        )
        claim_with_payout.add_payout(
            Payout(payout_id="PAY001", amount=100.0)
        )
        claims2 = [claim_with_payout]
        changes = manager.detect_changes(claims2)
        
        self.assertEqual(len(changes['new_payouts']), 1)


class TestNotifiers(unittest.TestCase):
    """Test notification systems."""
    
    def test_console_notifier(self):
        """Test console notifier."""
        notifier = ConsoleNotifier()
        result = notifier.send_notification(
            "Test Subject",
            "Test message"
        )
        self.assertTrue(result)
    
    def test_email_notifier_format_changes(self):
        """Test email notification formatting."""
        notifier = EmailNotifier()
        
        # Create test changes
        expired_claim = Claim(
            claim_id="CLAIM001",
            name="Expired Claim",
            source="TestSource",
            expiration_date=datetime.now() - timedelta(days=1)
        )
        
        claim_with_payout = Claim(
            claim_id="CLAIM002",
            name="Claim with Payout",
            source="TestSource"
        )
        new_payout = Payout(payout_id="PAY001", amount=100.0)
        claim_with_payout.metadata["new_payout"] = new_payout
        
        changes = {
            "expired_claims": [expired_claim],
            "new_payouts": [claim_with_payout]
        }
        
        subject, message = notifier.format_changes_notification(changes)
        
        self.assertIsNotNone(subject)
        self.assertIsNotNone(message)
        self.assertIn("2 Change(s)", subject)
        self.assertIn("Expired Claim", message)
        self.assertIn("Claim with Payout", message)
    
    def test_email_notifier_no_changes(self):
        """Test email notification with no changes."""
        notifier = EmailNotifier()
        changes = {
            "expired_claims": [],
            "new_payouts": []
        }
        
        subject, message = notifier.format_changes_notification(changes)
        self.assertIsNone(subject)
        self.assertIsNone(message)


class TestActionClaimsAgent(unittest.TestCase):
    """Test the main agent class."""
    
    def setUp(self):
        """Create temporary state file for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.state_file = os.path.join(self.temp_dir, "test_state.json")
    
    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
        os.rmdir(self.temp_dir)
    
    def test_agent_creation(self):
        """Test creating agent instance."""
        client = StubClaimsClient()
        agent = ActionClaimsAgent(
            data_client=client,
            state_file=self.state_file
        )
        self.assertIsNotNone(agent)
    
    def test_agent_run(self):
        """Test running the agent."""
        client = StubClaimsClient()
        notifier = ConsoleNotifier()
        agent = ActionClaimsAgent(
            data_client=client,
            state_file=self.state_file,
            notifier=notifier
        )
        
        results = agent.run()
        
        self.assertIn('timestamp', results)
        self.assertIn('total_claims', results)
        self.assertIn('active_claims', results)
        self.assertGreaterEqual(results['total_claims'], 0)
    
    def test_agent_multiple_runs(self):
        """Test running agent multiple times to detect changes."""
        # Note: Creating separate agents and state files to avoid race conditions
        client = StubClaimsClient()
        notifier = ConsoleNotifier()
        
        # First run with its own state file
        state_file1 = os.path.join(self.temp_dir, 'state1.json')
        agent1 = ActionClaimsAgent(
            data_client=client,
            state_file=state_file1,
            notifier=notifier
        )
        results1 = agent1.run()
        
        # Second run - reusing the first state file to test state persistence
        # Use a fresh agent instance
        agent2 = ActionClaimsAgent(
            data_client=StubClaimsClient(),  # Fresh client too
            state_file=state_file1,
            notifier=ConsoleNotifier()  # Fresh notifier
        )
        results2 = agent2.run()
        
        # Both runs should complete successfully
        self.assertIsNotNone(results1)
        self.assertIsNotNone(results2)
        self.assertIn('total_claims', results1)
        self.assertIn('total_claims', results2)


class TestExpirationTracking(unittest.TestCase):
    """Test expiration tracking functionality."""
    
    def test_expired_claim_detection(self):
        """Test that expired claims are properly detected."""
        past_date = datetime.now() - timedelta(days=5)
        claim = Claim(
            claim_id="CLAIM001",
            name="Expired",
            source="Test",
            expiration_date=past_date
        )
        self.assertTrue(claim.is_expired())
    
    def test_active_claim_detection(self):
        """Test that active claims are not marked as expired."""
        future_date = datetime.now() + timedelta(days=30)
        claim = Claim(
            claim_id="CLAIM001",
            name="Active",
            source="Test",
            expiration_date=future_date
        )
        self.assertFalse(claim.is_expired())
    
    def test_no_expiration_date(self):
        """Test claim with no expiration date."""
        claim = Claim(
            claim_id="CLAIM001",
            name="No Expiration",
            source="Test",
            expiration_date=None
        )
        self.assertFalse(claim.is_expired())


class TestPayoutTracking(unittest.TestCase):
    """Test payout tracking functionality."""
    
    def test_payout_association(self):
        """Test associating payouts with claims."""
        claim = Claim(
            claim_id="CLAIM001",
            name="Test Claim",
            source="Test"
        )
        
        payout1 = Payout(payout_id="PAY001", amount=100.0)
        payout2 = Payout(payout_id="PAY002", amount=200.0)
        
        claim.add_payout(payout1)
        claim.add_payout(payout2)
        
        self.assertEqual(len(claim.payouts), 2)
        self.assertEqual(claim.payouts[0].amount, 100.0)
        self.assertEqual(claim.payouts[1].amount, 200.0)
    
    def test_payout_status_tracking(self):
        """Test tracking payout status."""
        payout = Payout(
            payout_id="PAY001",
            amount=100.0,
            status="pending"
        )
        self.assertEqual(payout.status, "pending")
        
        payout.status = "completed"
        self.assertEqual(payout.status, "completed")


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit(run_tests())
