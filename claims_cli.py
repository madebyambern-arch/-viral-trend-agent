"""
Command-Line Interface for Action Claims Agent

Provides CLI for running the agent manually, on a schedule, or in loop mode.
Supports configuration via environment variables and command-line arguments.
"""

import argparse
import os
import sys
import time
import signal
from datetime import datetime
from typing import Optional
from action_claims_agent import (
    ActionClaimsAgent,
    StubClaimsClient,
    EmailNotifier,
    ConsoleNotifier
)


class ClaimsCLI:
    """Command-line interface for the Action Claims Agent."""
    
    def __init__(self):
        self.running = True
        self.agent: Optional[ActionClaimsAgent] = None
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print("\n\n⚠️  Shutdown signal received. Stopping agent...")
        self.running = False
        sys.exit(0)
    
    def _create_notifier(self, args) -> Notifier:
        """Create notifier based on configuration."""
        # Check if email configuration is provided
        smtp_host = args.smtp_host or os.getenv('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(args.smtp_port or os.getenv('SMTP_PORT', '587'))
        sender_email = args.sender_email or os.getenv('SENDER_EMAIL', '')
        sender_password = args.sender_password or os.getenv('SENDER_PASSWORD', '')
        recipient_email = args.recipient_email or os.getenv('RECIPIENT_EMAIL', '')
        
        if sender_email and sender_password and recipient_email:
            print(f"📧 Using email notifier (to: {recipient_email})")
            return EmailNotifier(
                smtp_host=smtp_host,
                smtp_port=smtp_port,
                sender_email=sender_email,
                sender_password=sender_password,
                recipient_email=recipient_email
            )
        else:
            print("📝 Using console notifier (email not configured)")
            return ConsoleNotifier()
    
    def _create_agent(self, args) -> ActionClaimsAgent:
        """Create and configure the agent."""
        # Create data client (stub for now, can be extended)
        client = StubClaimsClient()
        
        # Create notifier
        notifier = self._create_notifier(args)
        
        # Get state file path
        state_file = args.state_file or os.getenv('STATE_FILE', 'claims_state.json')
        
        # Create agent
        agent = ActionClaimsAgent(
            data_client=client,
            state_file=state_file,
            notifier=notifier
        )
        
        return agent
    
    def run_once(self, args):
        """Run the agent once and exit."""
        print("🚀 Running Action Claims Agent (single run mode)\n")
        
        agent = self._create_agent(args)
        results = agent.run()
        
        print("\n✅ Run completed successfully!")
        return 0
    
    def run_scheduled(self, args):
        """Run the agent on a schedule (loop mode)."""
        interval = args.interval or int(os.getenv('RUN_INTERVAL', '86400'))  # Default: 24 hours
        
        print(f"🔄 Running Action Claims Agent in scheduled mode")
        print(f"📅 Interval: {interval} seconds ({interval / 3600:.1f} hours)\n")
        
        agent = self._create_agent(args)
        run_count = 0
        
        while self.running:
            run_count += 1
            print(f"\n{'=' * 80}")
            print(f"RUN #{run_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'=' * 80}\n")
            
            try:
                results = agent.run()
                print(f"\n✅ Run #{run_count} completed successfully!")
            except Exception as e:
                print(f"\n❌ Run #{run_count} failed: {e}")
                if args.exit_on_error:
                    print("Exiting due to error (--exit-on-error flag set)")
                    return 1
            
            if self.running:
                next_run = datetime.now().timestamp() + interval
                next_run_str = datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')
                print(f"\n⏰ Next run scheduled for: {next_run_str}")
                print(f"💤 Sleeping for {interval} seconds...\n")
                
                # Sleep in small chunks to allow for graceful shutdown
                sleep_remaining = interval
                while sleep_remaining > 0 and self.running:
                    sleep_time = min(sleep_remaining, 10)  # Check every 10 seconds
                    time.sleep(sleep_time)
                    sleep_remaining -= sleep_time
        
        print("\n👋 Agent stopped gracefully")
        return 0
    
    def run_github_actions(self, args):
        """Run in GitHub Actions mode (single run with environment variables)."""
        print("🤖 Running Action Claims Agent (GitHub Actions mode)\n")
        
        # GitHub Actions environment
        print("📋 GitHub Actions Environment:")
        print(f"  Repository: {os.getenv('GITHUB_REPOSITORY', 'N/A')}")
        print(f"  Workflow: {os.getenv('GITHUB_WORKFLOW', 'N/A')}")
        print(f"  Run ID: {os.getenv('GITHUB_RUN_ID', 'N/A')}")
        print(f"  Run Number: {os.getenv('GITHUB_RUN_NUMBER', 'N/A')}\n")
        
        agent = self._create_agent(args)
        results = agent.run()
        
        # Output for GitHub Actions
        if os.getenv('GITHUB_OUTPUT'):
            with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
                f.write(f"total_claims={results['total_claims']}\n")
                f.write(f"active_claims={results['active_claims']}\n")
                f.write(f"expired_claims={results['expired_claims']}\n")
                f.write(f"new_payouts={results['new_payouts']}\n")
        
        print("\n✅ GitHub Actions run completed successfully!")
        return 0
    
    def main(self):
        """Main entry point for the CLI."""
        parser = argparse.ArgumentParser(
            description="Action Claims Agent - Track claims, payouts, and send notifications",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Run once
  python claims_cli.py run-once
  
  # Run on a schedule (every 24 hours)
  python claims_cli.py scheduled --interval 86400
  
  # Run in GitHub Actions mode
  python claims_cli.py github-actions
  
  # Run with email notifications
  python claims_cli.py run-once \\
    --sender-email sender@example.com \\
    --sender-password "password" \\
    --recipient-email recipient@example.com

Environment Variables:
  STATE_FILE         Path to JSON state file (default: claims_state.json)
  RUN_INTERVAL       Interval in seconds for scheduled mode (default: 86400)
  SMTP_HOST          SMTP server host (default: smtp.gmail.com)
  SMTP_PORT          SMTP server port (default: 587)
  SENDER_EMAIL       Email sender address
  SENDER_PASSWORD    Email sender password
  RECIPIENT_EMAIL    Email recipient address
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Command to run')
        
        # Run-once command
        run_once_parser = subparsers.add_parser('run-once', help='Run the agent once')
        run_once_parser.add_argument('--state-file', help='Path to state file')
        run_once_parser.add_argument('--sender-email', help='Email sender address')
        run_once_parser.add_argument('--sender-password', help='Email sender password')
        run_once_parser.add_argument('--recipient-email', help='Email recipient address')
        run_once_parser.add_argument('--smtp-host', help='SMTP server host')
        run_once_parser.add_argument('--smtp-port', help='SMTP server port')
        
        # Scheduled command
        scheduled_parser = subparsers.add_parser('scheduled', help='Run the agent on a schedule')
        scheduled_parser.add_argument('--interval', type=int, help='Run interval in seconds')
        scheduled_parser.add_argument('--state-file', help='Path to state file')
        scheduled_parser.add_argument('--sender-email', help='Email sender address')
        scheduled_parser.add_argument('--sender-password', help='Email sender password')
        scheduled_parser.add_argument('--recipient-email', help='Email recipient address')
        scheduled_parser.add_argument('--smtp-host', help='SMTP server host')
        scheduled_parser.add_argument('--smtp-port', help='SMTP server port')
        scheduled_parser.add_argument('--exit-on-error', action='store_true',
                                     help='Exit if a run fails')
        
        # GitHub Actions command
        github_parser = subparsers.add_parser('github-actions', 
                                             help='Run in GitHub Actions mode')
        github_parser.add_argument('--state-file', help='Path to state file')
        github_parser.add_argument('--sender-email', help='Email sender address')
        github_parser.add_argument('--sender-password', help='Email sender password')
        github_parser.add_argument('--recipient-email', help='Email recipient address')
        github_parser.add_argument('--smtp-host', help='SMTP server host')
        github_parser.add_argument('--smtp-port', help='SMTP server port')
        
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return 1
        
        # Route to appropriate handler
        if args.command == 'run-once':
            return self.run_once(args)
        elif args.command == 'scheduled':
            return self.run_scheduled(args)
        elif args.command == 'github-actions':
            return self.run_github_actions(args)
        else:
            print(f"Unknown command: {args.command}")
            return 1


if __name__ == "__main__":
    cli = ClaimsCLI()
    sys.exit(cli.main())
