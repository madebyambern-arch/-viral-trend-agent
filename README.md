# 🚀 Viral Trend Agent Suite

A collection of powerful automation agents for content creation and legal settlements monitoring.

## 📋 Overview

This repository contains multiple specialized agents:

### 1. 🎬 Productivity/Mindset Content Finder
Analyzes viral content patterns from top creators in the productivity and mindset space, then generates batch-ready content ideas that you can quickly create and post across multiple social media platforms.

### 2. ⚖️ Class Action Claims Agent (NEW!)
Monitors active class action claims and payouts, tracks expiration dates, and sends daily notifications only when there are changes (expiring claims or new payouts announced).

---

## ⚖️ Class Action Claims Agent

### Features

- 🔍 **Active Claims Search**: Automatically searches for all active class action claims
- ⏰ **Expiration Tracking**: Monitors claims approaching their filing deadline
- 💰 **Payout Monitoring**: Tracks newly announced settlements and payouts
- 📢 **Smart Notifications**: Only notifies when there are changes (no spam!)
- 💾 **State Persistence**: Remembers previous runs to detect changes
- 🗓️ **Daily Scheduling**: Designed to run as a daily automated task via GitHub Actions
- 📊 **Detailed Reports**: Generates comprehensive JSON reports
- 📧 **Email Notifications**: Built-in SMTP email support with STARTTLS
- 🛠️ **CLI Interface**: Configurable via command-line arguments

### Quick Start - Claims Agent

Run the claims agent with default settings:

```bash
python3 class_action_claims_agent.py
```

**First Run Output:**
- Lists all active claims
- Shows claims expiring within 30 days
- Displays recent payouts
- Saves state for future comparisons

**Subsequent Runs:**
- Only shows NEW notifications:
  - Claims newly entering the "expiring soon" window
  - Claims that expired since last run (notified once)
  - Newly announced payouts

### CLI Usage

The agent supports various command-line options:

```bash
# View all available options
python class_action_claims_agent.py --help

# Customize expiring window to 14 days
python class_action_claims_agent.py --expiring-days 14

# Use custom state file and report path
python class_action_claims_agent.py --state-file /tmp/state.json --report-path /tmp/report.json

# Skip writing report file (useful for cron jobs with email notifications)
python class_action_claims_agent.py --skip-report

# Enable email notifications (requires SMTP environment variables)
python class_action_claims_agent.py --notify-email

# Combine options
python class_action_claims_agent.py --expiring-days 14 --payout-days 7 --notify-email
```

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--state-file PATH` | Path to state file | `class_action_state.json` or `$CLASS_ACTION_STATE_FILE` |
| `--report-path PATH` | Path to write JSON report | `class_action_report_TIMESTAMP.json` |
| `--expiring-days N` | Days window for expiring claims | 30 |
| `--payout-days N` | Days window for recent payouts | 30 |
| `--skip-report` | Skip writing JSON report file | False |
| `--notify-email` | Send email notifications | False |

### Email Notifications

To enable email notifications, set the following environment variables:

```bash
# Required
export SMTP_HOST="smtp.gmail.com"           # SMTP server hostname
export SMTP_PORT="587"                       # SMTP port (default: 587)
export SMTP_FROM="alerts@example.com"        # From email address
export SMTP_TO="recipient@example.com"       # To email address

# Optional (for authenticated SMTP)
export SMTP_USERNAME="your-username"         # SMTP username
export SMTP_PASSWORD="your-password"         # SMTP password

# Run with email notifications
python class_action_claims_agent.py --notify-email
```

**Email Features:**
- Sends email only when there are changes (no empty notifications)
- Supports STARTTLS for secure connections
- Groups notifications by type (expiring, expired, new payouts)
- Includes all relevant details (deadlines, amounts, URLs)

**Example Email Notification:**
```
Subject: Class Action Claims Alert - 3 Update(s)

CLASS ACTION CLAIMS DAILY ALERT
======================================================================
Date: 2026-01-16 09:00:00
Total Updates: 3

⚠️  EXPIRING CLAIMS (2):
----------------------------------------------------------------------

• ABC Electronics Product Defect Settlement
  Claim expires in 14 days
  Deadline: 2026-01-31
  Amount: Up to $350 or replacement
  URL: https://example.com/abc-settlement

💰 NEW PAYOUTS (1):
----------------------------------------------------------------------

• MNO Bank Overdraft Fee Settlement Payout
  Amount: $87.5 million total fund
  Announced: 2026-01-14
  Distribution: 2026-02-15
  URL: https://example.com/mno-payout
```

### GitHub Actions Scheduling

The repository includes a GitHub Actions workflow that runs the agent daily at 9:00 AM UTC.

**Workflow File:** `.github/workflows/class-action-agent.yml`

**Features:**
- Runs daily via cron schedule: `0 9 * * *`
- Can be manually triggered via workflow_dispatch
- Uses only Python standard library (no external dependencies)
- Uploads JSON report as artifact (90-day retention)
- Uploads state file as artifact (7-day retention)

**Setting Up Email Notifications in GitHub Actions:**

1. Go to your repository Settings → Secrets and variables → Actions
2. Add repository secrets:
   - `SMTP_HOST`
   - `SMTP_PORT`
   - `SMTP_USERNAME`
   - `SMTP_PASSWORD`
   - `SMTP_FROM`
   - `SMTP_TO`
3. Uncomment the environment variables in the workflow file
4. The agent will automatically send email notifications on changes

**Manual Workflow Trigger:**
1. Go to Actions tab in your repository
2. Select "Class Action Claims Agent - Daily Run"
3. Click "Run workflow"

### Example Output

```
================================================================================
CLASS ACTION CLAIMS AGENT - DAILY REPORT
================================================================================
Run Date: 2026-01-16 09:00:00

📊 SUMMARY
--------------------------------------------------------------------------------
Total Active Claims: 5
Claims Expiring Soon (30 days): 2
Recent Payouts (30 days): 2
Notifications: 4

🔔 NOTIFICATIONS
--------------------------------------------------------------------------------

⚠️  EXPIRING CLAIMS:

  • ABC Electronics Product Defect Settlement
    Claim expires in 14 days
    Deadline: 2026-01-31
    Amount: Up to $350 or replacement
    URL: https://example.com/abc-settlement

  • GHI Auto Airbag Recall Settlement
    Claim expires in 5 days
    Deadline: 2026-01-21
    Amount: Up to $1,000
    URL: https://example.com/ghi-settlement

💰 NEW PAYOUTS:

  • MNO Bank Overdraft Fee Settlement Payout
    New payout announced: $87.5 million total fund
    Announced: 2026-01-14
    Distribution: 2026-02-15
    URL: https://example.com/mno-payout

  • PQR Retailer Price Fixing Settlement Payout
    New payout announced: $125 million total fund
    Announced: 2026-01-15
    Distribution: 2026-03-01
    URL: https://example.com/pqr-payout
```

### Daily Scheduling (Alternative to GitHub Actions)

**Linux/Mac (cron):**
```bash
# Run daily at 9 AM with email notifications
0 9 * * * cd /path/to/-viral-trend-agent && python3 class_action_claims_agent.py --notify-email
```

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9:00 AM
4. Action: Start a program
5. Program: `python3`
6. Arguments: `class_action_claims_agent.py --notify-email`
7. Start in: `C:\path\to\-viral-trend-agent`

### Claims Categories

The agent monitors claims in these categories:
- 📊 Data Breach
- 🛒 Consumer Products
- 💼 Securities
- ⚖️ Antitrust
- 👥 Employment
- 🏥 Insurance
- 🚗 Automotive
- 📱 Telecommunications

### Testing

Run the comprehensive test suite:

```bash
python -m unittest test_class_action_claims_agent.py -v
```

**Test Coverage:**
- Expiring claim detection (with deduplication)
- Expired claim detection between runs
- New payout detection
- Notification generation (changes only)
- State persistence
- Email notifications (mocked SMTP)

### Programmatic Usage

```python
from class_action_claims_agent import ClassActionClaimsAgent, EmailNotifier

# Option 1: Console notifications (default)
agent = ClassActionClaimsAgent(
    state_file="my_state.json",
    expiring_window_days=14,
    recent_payout_window_days=7
)
summary = agent.run()

# Option 2: Email notifications
email_notifier = EmailNotifier(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    smtp_from="alerts@example.com",
    smtp_to="recipient@example.com",
    smtp_username="username",
    smtp_password="password"
)

agent = ClassActionClaimsAgent(
    notifier=email_notifier,
    expiring_window_days=30
)
summary = agent.run()

# Access notifications
for notif in summary['notifications']:
    print(f"{notif['type']}: {notif['title']}")
```

### Advanced Usage

See `class_action_example_usage.py` for detailed examples including:
- Filtering claims by category
- Finding high-priority claims (expiring in 7 days)
- Exporting reports
- Custom integrations
- Simulating daily run behavior

### Production Setup

To use real data instead of mock data:

1. **Replace mock functions** in `class_action_claims_agent.py`:
   - `generate_mock_claims()` → Connect to real APIs/scrapers
   - `generate_mock_payouts()` → Connect to payout tracking systems

2. **Popular data sources to integrate:**
   - ClassAction.org
   - TopClassActions.com
   - JND Legal Administration
   - Settlement-specific websites

3. **Configure notifications:**
   - Set up SMTP environment variables for email
   - Or implement custom Notifier subclass for Slack/Discord/SMS

### How It Works

**Change Detection Logic:**

1. **Expiring Claims**: 
   - Detects claims entering the expiring window (default 30 days)
   - Only notifies once when a claim first enters the window
   - Won't re-notify if claim stays in the window across runs

2. **Expired Claims**:
   - Detects claims that crossed their filing deadline between runs
   - Handles both cases: claims still present or removed from fetch
   - Only notifies once per claim using tracked list in state file

3. **New Payouts**:
   - Detects payouts announced within window (default 30 days)
   - Compares against previous state to identify new announcements
   - First run treats all recent payouts as "new"

**State Persistence:**
- State saved in JSON file after each run
- Tracks: claims, payouts, last run time, notified expired claims
- Used to detect changes between runs
- Can be overridden via CLI or environment variable

---

## 🎬 Productivity/Mindset Content Finder

## ✨ Features

- 🔍 **Viral Content Analysis**: Analyzes trending posts to identify viral patterns
- 📊 **Category Performance**: Breaks down performance by content category (productivity, mindset, habits, etc.)
- 🎬 **Content Type Analysis**: Identifies which content types perform best (listicles, tutorials, transformations, etc.)
- 🚀 **Batch Content Generation**: Automatically generates 30+ content ideas based on viral patterns
- 📱 **Platform-Specific Formatting**: Formats posts for Instagram, TikTok, and YouTube
- 📅 **Posting Schedule**: Provides optimal posting times and frequencies
- 💾 **Export Functionality**: Exports all data to JSON for easy access

## 🎯 Supported Content Categories

1. **Productivity** - Morning routines, time management, productivity hacks
2. **Mindset** - Growth mindset, motivation, success principles
3. **Habits** - Habit building, tracking, atomic habits
4. **Goal Setting** - SMART goals, achievement strategies, planning
5. **Personal Development** - Life lessons, self-improvement, transformation

## 📦 Installation

### Prerequisites

- Python 3.7 or higher

### Setup

1. Clone this repository:
```bash
git clone https://github.com/madebyambern-arch/-viral-trend-agent.git
cd -viral-trend-agent
```

2. No external dependencies required! The script uses only Python standard library.

## 🚀 Quick Start

### Basic Usage

Run the main script to analyze viral content and generate batch ideas:

```bash
python3 productivity_mindset_agent.py
```

This will:
1. Analyze 12+ viral posts in the productivity/mindset niche
2. Identify patterns and top-performing content types
3. Generate 30 batch-ready content ideas
4. Export everything to a timestamped JSON file
5. Display platform-specific formatting examples

### Sample Output

```
================================================================================
VIRAL CONTENT FINDER - PRODUCTIVITY/MINDSET NICHE
================================================================================

📊 Loading trending productivity/mindset content...
✅ Analyzing 12 viral posts

🔍 Step 1: Finding viral posts...
✅ Found 12 viral posts

📈 Step 2: Finding trending posts...
✅ Found 12 trending posts
```

## 📊 What You Get

### 1. Viral Content Analysis
- Top 5 most viral posts with engagement metrics
- Creator information and hooks used
- Engagement rates and growth multipliers

### 2. Category Performance Metrics
- Posts count per category
- Average views and engagement
- Growth rates
- Popular content types

### 3. Content Type Analysis
- Performance by content type (listicle, tutorial, etc.)
- Real examples from viral posts
- Average metrics per type

### 4. Batch Content Ideas (30+)
Each content idea includes:
- **Title**: Proven viral title format
- **Category**: Content category
- **Content Type**: Format (listicle, tutorial, etc.)
- **Script Outline**: Step-by-step content structure
- **Platforms**: Instagram Reels, TikTok, YouTube Shorts
- **Production Time**: Estimated creation time
- **Batch Group**: For organizing production

Example content idea:
```json
{
  "id": "batch_001",
  "title": "5 Morning Habits That Changed My Life",
  "category": "productivity",
  "content_type": "listicle",
  "script_outline": [
    "Hook: Strong opening question or statement",
    "Point 1: First item with brief explanation",
    "Point 2: Second item with example",
    "Point 3: Third item with benefit",
    "Call-to-action: Follow for more"
  ],
  "posting_platform": ["Instagram Reels", "TikTok", "YouTube Shorts"],
  "estimated_production_time": "10-15 minutes",
  "batch_group": 1
}
```

### 5. Posting Schedule
Optimized weekly schedule with:
- Best posting times
- Recommended categories per day
- Strategic rationale

Example:
```
Monday: 9:00 AM - Productivity (Start week strong)
Tuesday: 7:00 PM - Mindset (Evening motivation)
Wednesday: 12:00 PM - Habits (Midweek check-in)
...
```

### 6. Platform-Specific Formatting
Automatically formatted posts for:
- **Instagram**: With spacing and hashtags
- **TikTok**: Optimized hashtag count
- **YouTube**: Full description with timestamps

## 🎨 Customization

### Adjust Batch Size

Generate more or fewer content ideas:

```python
from productivity_mindset_agent import ProductivityMindsetAgent, generate_productivity_mindset_trends

posts = generate_productivity_mindset_trends()
agent = ProductivityMindsetAgent(posts)
agent.find_viral_posts()

# Generate 50 ideas instead of 30
content_ideas = agent.generate_batch_content_ideas(count=50)
```

### Change Viral Thresholds

Modify the thresholds in `productivity_mindset_agent.py`:

```python
VIRAL_VIEWS = 50000        # Minimum views for viral
VIRAL_ENGAGEMENT = 5000    # Minimum total engagement
TRENDING_GROWTH = 2.0      # Minimum growth rate multiplier
```

### Add Your Own Data

Replace the mock data with real API data:

```python
def generate_productivity_mindset_trends():
    # Replace mock data with real social media API calls
    # Example: TikTok API, Instagram Graph API, YouTube Data API
    posts = fetch_from_api()  # Your API integration
    return posts
```

## 📁 Output Files

The script generates timestamped JSON files:

- `batch_content_YYYYMMDD_HHMMSS.json` - Complete batch content ideas

### JSON Structure

```json
{
  "generated_at": "20251211_224702",
  "total_ideas": 30,
  "content_ideas": [
    {
      "id": "batch_001",
      "title": "Content Title",
      "category": "productivity",
      "content_type": "listicle",
      "script_outline": ["Hook", "Point 1", "..."],
      "posting_platform": ["Instagram Reels", "TikTok", "YouTube Shorts"],
      "estimated_production_time": "10-15 minutes",
      "batch_group": 1
    }
  ]
}
```

## 🎬 Content Creation Workflow

### Step 1: Generate Ideas
```bash
python3 productivity_mindset_agent.py
```

### Step 2: Review Generated Content
Open the generated JSON file and review the 30 content ideas.

### Step 3: Batch Create Videos
Work through each batch group (10 ideas per group):
1. Set up your recording environment once
2. Record all 10 videos in the batch
3. Use the script outlines provided
4. Each video takes 10-15 minutes

### Step 4: Edit and Post
1. Batch edit all videos
2. Use the platform-specific formatting
3. Follow the posting schedule
4. Cross-post to all platforms

### Step 5: Track and Iterate
1. Monitor which content types perform best
2. Re-run the analysis tool weekly
3. Adjust strategy based on results

## 📈 Best Practices

### Content Creation
- ✅ Batch record 10+ videos at once
- ✅ Use proven hooks from viral posts
- ✅ Keep videos 30-60 seconds for Reels/TikTok
- ✅ Add captions/text overlays
- ✅ Use trending audio when possible

### Posting Strategy
- ✅ Post consistently (daily recommended)
- ✅ Engage with comments within first hour
- ✅ Cross-post to all platforms
- ✅ Track metrics and double down on winners
- ✅ Test different posting times

### Engagement Tips
- ✅ Strong hook in first 3 seconds
- ✅ Clear value proposition
- ✅ Call-to-action at the end
- ✅ Reply to all comments
- ✅ Use relevant hashtags

## 🔧 Advanced Usage

### Programmatic Access

```python
from productivity_mindset_agent import ProductivityMindsetAgent, generate_productivity_mindset_trends

# Load data
posts = generate_productivity_mindset_trends()
agent = ProductivityMindsetAgent(posts)

# Analyze
viral_posts = agent.find_viral_posts()
trending_posts = agent.find_trending_posts()
category_stats = agent.analyze_by_category()
type_stats = agent.analyze_by_content_type()

# Generate content
content_ideas = agent.generate_batch_content_ideas(count=30)

# Format for specific platform
instagram_post = agent.format_for_social_media(content_ideas[0], "instagram")
tiktok_post = agent.format_for_social_media(content_ideas[0], "tiktok")

# Get posting schedule
schedule = agent.get_posting_schedule()

# Export
agent.export_batch_content(content_ideas, "my_batch")
```

### Filter by Category

```python
# Get only productivity content ideas
productivity_ideas = [
    idea for idea in content_ideas 
    if idea['category'] == 'productivity'
]

# Get only listicle format
listicle_ideas = [
    idea for idea in content_ideas 
    if idea['content_type'] == 'listicle'
]
```

## 📚 Additional Resources

### Top Creators to Study
- **Productivity**: Ali Abdaal, Thomas Frank, Matt D'Avella
- **Mindset**: Jay Shetty, Tom Bilyeu, Alex Hormozi
- **Mixed**: Andrew Huberman, Diary Of A CEO, Tim Ferriss

### Recommended Tools
- **Video Editing**: CapCut, Adobe Premiere Rush
- **Text-to-Speech**: ElevenLabs, Murf AI
- **Stock Footage**: Pexels, Pixabay
- **Auto Captions**: CapCut, Descript
- **Scheduling**: Later, Buffer, Hootsuite

### Content Type Definitions

1. **Listicle**: Numbered list format (5 habits, 7 tips, etc.)
2. **Tutorial**: Step-by-step how-to guide
3. **Transformation**: Before/after personal story
4. **Experiment**: "I tried X for Y days" format
5. **Motivational**: Inspirational/encouraging content
6. **Framework**: System or method explanation
7. **Wisdom**: Life lessons and insights
8. **Contrarian**: Challenge common beliefs
9. **Science**: Research-backed content
10. **Insight**: Key realizations or questions

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new content templates
- Improve viral detection algorithms
- Add API integrations for real data
- Enhance formatting options
- Add more platforms

## 📄 License

This project is open source and available for personal and commercial use.

## ⚠️ Important Notes

### Mock Data
The current version uses mock trending data for demonstration. For production use, integrate with:
- TikTok Creator API
- Instagram Graph API
- YouTube Data API v3

### Rate Limits
When using real APIs, be mindful of rate limits and implement appropriate caching.

### Content Authenticity
While this tool generates ideas based on viral patterns, always add your unique perspective and authenticity to stand out.

## 🎯 Success Metrics

Track these KPIs:
- **Engagement Rate**: Likes + Comments + Shares / Views
- **Growth Rate**: Current period views / Previous period views
- **Follower Growth**: New followers per week
- **Watch Time**: Average video completion rate
- **Click-Through Rate**: Profile visits from videos

## 💡 Pro Tips

1. **Consistency > Perfection**: Post daily even if not perfect
2. **Hook is King**: First 3 seconds determine success
3. **Batch Everything**: Record 10+ videos at once
4. **Cross-Post**: Use same content across all platforms
5. **Engage Fast**: Reply to comments within first hour
6. **Track Winners**: Double down on what works
7. **Stay Current**: Re-run analysis weekly
8. **Add Value**: Always provide actionable insights
9. **Be Authentic**: Share personal experiences
10. **Test & Iterate**: Try different formats and times

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check existing documentation
- Review example outputs

## 🚀 Roadmap

Future enhancements:
- [ ] Real-time API integrations
- [ ] AI-powered script generation
- [ ] Auto-scheduling to social media
- [ ] Performance tracking dashboard
- [ ] A/B testing framework
- [ ] Competitor analysis
- [ ] Trend prediction using ML
- [ ] Multi-language support

---

**Happy Creating!** 🎬✨

Remember: The best time to start was yesterday. The second best time is now. Generate your batch content and start posting today!
