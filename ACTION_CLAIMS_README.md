# Action Claims Agent

A lightweight Python agent for tracking action claims, monitoring payouts, and sending notifications about claim expirations and new payouts.

## 📋 Overview

The Action Claims Agent is designed to automate the monitoring of action claims, track associated payouts, and notify you when claims expire or new payouts are announced. It uses JSON-based state persistence to track changes over time and can be scheduled to run automatically via GitHub Actions.

## ✨ Features

- **📊 Data Models**: Clean dataclasses for claims and payouts with full serialization support
- **🔌 Pluggable Architecture**: Extensible scraping/API client interfaces
- **💰 Payout Tracking**: Automatic detection of new payouts associated with claims
- **⏰ Expiration Tracking**: Monitors claim expiration dates and alerts on expired claims
- **💾 State Persistence**: JSON-based state tracking with change detection
- **📧 Notifications**: Email and console notification support for changes
- **🤖 Scheduling**: GitHub Actions integration for automated daily runs
- **🖥️ CLI Interface**: Command-line interface for manual and scheduled runs
- **✅ Tested**: Comprehensive test suite covering all functionality

## 🚀 Quick Start

### Basic Usage

Run the agent once:

```bash
python claims_cli.py run-once
```

### Run on a Schedule

Run the agent every 24 hours:

```bash
python claims_cli.py scheduled --interval 86400
```

### Run in GitHub Actions Mode

```bash
python claims_cli.py github-actions
```

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- No external dependencies (uses Python standard library only)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/madebyambern-arch/-viral-trend-agent.git
cd -viral-trend-agent
```

2. The module is ready to use! No installation required.

## 🎯 Usage Guide

### Command-Line Interface

The agent provides three main commands:

#### 1. Run Once

Execute the agent a single time:

```bash
python claims_cli.py run-once
```

With email notifications:

```bash
python claims_cli.py run-once \
  --sender-email sender@example.com \
  --sender-password "your-password" \
  --recipient-email recipient@example.com
```

#### 2. Scheduled Mode

Run the agent continuously on a schedule:

```bash
# Run every 24 hours (86400 seconds)
python claims_cli.py scheduled --interval 86400

# Run every hour
python claims_cli.py scheduled --interval 3600

# Exit on first error
python claims_cli.py scheduled --interval 86400 --exit-on-error
```

#### 3. GitHub Actions Mode

Optimized for running in GitHub Actions:

```bash
python claims_cli.py github-actions
```

This mode:
- Reads configuration from environment variables
- Outputs results to GitHub Actions outputs
- Prints GitHub Actions environment info

### Configuration

#### Environment Variables

The agent can be configured via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `STATE_FILE` | Path to JSON state file | `claims_state.json` |
| `RUN_INTERVAL` | Interval in seconds for scheduled mode | `86400` (24 hours) |
| `SMTP_HOST` | SMTP server host | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SENDER_EMAIL` | Email sender address | (none) |
| `SENDER_PASSWORD` | Email sender password | (none) |
| `RECIPIENT_EMAIL` | Email recipient address | (none) |

Example:

```bash
export STATE_FILE="claims_state.json"
export SENDER_EMAIL="your-email@example.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="notifications@example.com"

python claims_cli.py run-once
```

#### Command-Line Arguments

All environment variables can also be set via command-line arguments:

```bash
python claims_cli.py run-once \
  --state-file custom_state.json \
  --smtp-host smtp.example.com \
  --smtp-port 465 \
  --sender-email sender@example.com \
  --sender-password "password" \
  --recipient-email recipient@example.com
```

### Email Configuration

To use email notifications, you need to configure SMTP settings.

#### Gmail Example

1. Enable 2-factor authentication on your Google account
2. Generate an app-specific password: https://myaccount.google.com/apppasswords
3. Use the app password in your configuration:

```bash
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="notifications@example.com"
```

#### Other SMTP Providers

For other providers, update `SMTP_HOST` and `SMTP_PORT`:

- **Outlook/Office365**: `smtp.office365.com`, port `587`
- **Yahoo**: `smtp.mail.yahoo.com`, port `587`
- **Custom SMTP**: Use your provider's settings

## 🤖 GitHub Actions Setup

### Automated Daily Runs

The repository includes a GitHub Actions workflow that runs the agent daily.

#### Setup Instructions

1. **Add Secrets to Repository**

   Go to your repository Settings → Secrets and variables → Actions, and add:

   - `SENDER_EMAIL`: Your email address
   - `SENDER_PASSWORD`: Your email password or app-specific password
   - `RECIPIENT_EMAIL`: Where to send notifications
   - `SMTP_HOST` (optional): SMTP server (defaults to `smtp.gmail.com`)
   - `SMTP_PORT` (optional): SMTP port (defaults to `587`)

2. **Enable Workflow**

   The workflow is located at `.github/workflows/claims-agent-daily.yml` and will:
   - Run automatically every day at 9:00 AM UTC
   - Can be triggered manually from the Actions tab
   - Cache the state file between runs
   - Upload state as an artifact for backup

3. **Manual Trigger**

   To run manually:
   - Go to Actions tab in your repository
   - Select "Action Claims Agent - Daily Run"
   - Click "Run workflow"

### Customizing the Schedule

Edit `.github/workflows/claims-agent-daily.yml` and modify the cron schedule:

```yaml
on:
  schedule:
    # Run daily at 9:00 AM UTC
    - cron: '0 9 * * *'
```

Examples:
- Every 12 hours: `'0 */12 * * *'`
- Every Monday at 8 AM: `'0 8 * * 1'`
- Twice daily (8 AM and 8 PM): `'0 8,20 * * *'`

## 🔧 Extending the Agent

### Creating Custom Data Sources

The agent uses a pluggable architecture for data sources. To create your own:

```python
from action_claims_agent import BaseClaimsClient, Claim, Payout
from datetime import datetime

class MyCustomClient(BaseClaimsClient):
    """Custom claims data source."""
    
    def fetch_claims(self) -> List[Claim]:
        """Fetch claims from your data source."""
        # Fetch from API, scrape website, read file, etc.
        raw_data = self._fetch_from_source()
        return self.normalize_data(raw_data)
    
    def normalize_data(self, raw_data: Any) -> List[Claim]:
        """Convert raw data to Claim objects."""
        claims = []
        for item in raw_data:
            claim = Claim(
                claim_id=item['id'],
                name=item['name'],
                source=item['source'],
                expiration_date=datetime.fromisoformat(item['expires']),
                # ... other fields
            )
            claims.append(claim)
        return claims
    
    def _fetch_from_source(self):
        """Your custom data fetching logic."""
        # Example: API call
        import requests
        response = requests.get("https://api.example.com/claims")
        return response.json()
```

Then use your custom client:

```python
from action_claims_agent import ActionClaimsAgent, ConsoleNotifier

client = MyCustomClient()
agent = ActionClaimsAgent(
    data_client=client,
    state_file="claims_state.json",
    notifier=ConsoleNotifier()
)

results = agent.run()
```

### Creating Custom Notifiers

You can create custom notification handlers:

```python
from action_claims_agent import Notifier

class SlackNotifier(Notifier):
    """Send notifications to Slack."""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send_notification(self, subject: str, message: str) -> bool:
        """Send notification to Slack."""
        import requests
        payload = {
            "text": f"*{subject}*\n{message}"
        }
        response = requests.post(self.webhook_url, json=payload)
        return response.status_code == 200
```

Use it in your agent:

```python
notifier = SlackNotifier("https://hooks.slack.com/services/YOUR/WEBHOOK/URL")
agent = ActionClaimsAgent(
    data_client=client,
    notifier=notifier
)
```

## 📊 Data Models

### Claim

Represents an action claim with tracking information.

```python
@dataclass
class Claim:
    claim_id: str                           # Unique identifier
    name: str                               # Claim name/title
    source: str                             # Data source
    status: str = "active"                  # active, expired, completed
    is_active: bool = True                  # Active flag
    expiration_date: Optional[datetime]     # When claim expires
    created_date: datetime                  # When claim was created
    updated_date: datetime                  # Last update time
    payouts: List[Payout]                   # Associated payouts
    metadata: Dict[str, Any]                # Additional data
```

### Payout

Represents a payout associated with a claim.

```python
@dataclass
class Payout:
    payout_id: str                          # Unique identifier
    amount: float                           # Payout amount
    currency: str = "USD"                   # Currency code
    announced_date: Optional[datetime]      # When payout was announced
    processed_date: Optional[datetime]      # When payout was processed
    status: str = "pending"                 # pending, processing, completed
    metadata: Dict[str, Any]                # Additional data
```

## 🧪 Testing

Run the test suite:

```bash
python test_action_claims_agent.py
```

Test coverage includes:
- ✅ Data model creation and serialization
- ✅ State persistence and loading
- ✅ Change detection (new claims, expired claims, new payouts)
- ✅ Notification formatting
- ✅ Expiration tracking
- ✅ Payout tracking
- ✅ Client interfaces
- ✅ Agent execution

## 📁 State File Format

The agent stores state in JSON format:

```json
{
  "last_run": "2024-01-15T10:30:00",
  "claims": {
    "CLAIM001": {
      "claim_id": "CLAIM001",
      "name": "Action Claim Alpha",
      "source": "SourceA",
      "status": "active",
      "is_active": true,
      "expiration_date": "2024-02-15T23:59:59",
      "created_date": "2024-01-01T00:00:00",
      "updated_date": "2024-01-15T10:30:00",
      "payouts": [
        {
          "payout_id": "PAY001",
          "amount": 100.0,
          "currency": "USD",
          "announced_date": "2024-01-15T10:00:00",
          "processed_date": null,
          "status": "pending",
          "metadata": {}
        }
      ],
      "metadata": {}
    }
  },
  "previous_claims": {
    // Previous run's claims for change detection
  }
}
```

## 📧 Notification Format

Email notifications are sent only when changes are detected:

**Subject:** `Action Claims Alert: 2 Change(s) Detected`

**Body:**
```
Action Claims Agent - Change Detection Report
============================================================

🔴 EXPIRED CLAIMS (1):
------------------------------------------------------------
  • Action Claim Alpha (ID: CLAIM001)
    Source: SourceA
    Expired: 2024-01-15 10:30

💰 NEW PAYOUTS (1):
------------------------------------------------------------
  • Action Claim Beta (ID: CLAIM002)
    Payout: $100.00 USD
    Announced: 2024-01-15 10:30

============================================================
Report generated: 2024-01-15 10:30:00
```

## 🔍 Example Workflows

### Local Development

```bash
# First run (initializes state)
python claims_cli.py run-once

# Check state file
cat claims_state.json

# Second run (detects changes)
python claims_cli.py run-once

# Run with email notifications
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="notifications@example.com"
python claims_cli.py run-once
```

### Production Deployment

```bash
# Set up environment
export STATE_FILE="/data/claims_state.json"
export SENDER_EMAIL="bot@company.com"
export SENDER_PASSWORD="secure-password"
export RECIPIENT_EMAIL="team@company.com"

# Run in scheduled mode
python claims_cli.py scheduled --interval 86400
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY action_claims_agent.py claims_cli.py ./
ENV STATE_FILE=/data/claims_state.json
VOLUME /data
CMD ["python", "claims_cli.py", "scheduled"]
```

Run:

```bash
docker build -t claims-agent .
docker run -d \
  -v $(pwd)/data:/data \
  -e SENDER_EMAIL="your-email@example.com" \
  -e SENDER_PASSWORD="password" \
  -e RECIPIENT_EMAIL="notifications@example.com" \
  claims-agent
```

## 🐛 Troubleshooting

### Email Not Sending

- Check SMTP credentials are correct
- For Gmail, use an app-specific password (not your regular password)
- Verify SMTP_HOST and SMTP_PORT are correct
- Check firewall/network allows SMTP connections

### State File Issues

- Ensure directory exists and is writable
- Check file permissions
- Verify JSON format is valid
- Delete state file to reset (will lose change detection for one run)

### GitHub Actions Not Running

- Check workflow is enabled in Actions settings
- Verify secrets are set correctly
- Check cron syntax is valid
- Ensure repository has Actions enabled

## 📝 Best Practices

1. **Backup State File**: The state file is critical for change detection. Back it up regularly.

2. **Email Configuration**: Use environment variables or secrets for email credentials, never commit them.

3. **Testing**: Run locally first with console notifier before enabling email notifications.

4. **Monitoring**: Check GitHub Actions runs regularly to ensure agent is working.

5. **Custom Clients**: When creating custom data sources, handle errors gracefully and validate data.

6. **Rate Limiting**: If scraping websites, respect rate limits and add delays.

## 📄 License

This project is open source and available under the same license as the parent repository.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional notification channels (Slack, Discord, SMS)
- More sophisticated change detection
- Database backend option
- Web dashboard for monitoring
- Additional data source implementations

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review test cases for examples

---

**Happy Monitoring!** 📊✨
