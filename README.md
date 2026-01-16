# 🚀 Viral Trend Agent Repository

A collection of powerful automation tools for content creation and action tracking.

## 📋 Repository Overview

This repository contains multiple agent modules:

1. **Viral Content Finder** - Analyzes viral content patterns in the Productivity/Mindset niche and generates batch-ready content ideas
2. **Action Claims Agent** - Tracks action claims, monitors payouts, and sends notifications about expirations and changes

## 🎯 Modules

### 1. Viral Content Finder - Productivity/Mindset Niche

A powerful tool to find viral entertainment content in the Productivity/Mindset niche that can be batch created and posted to your social media pages.

This tool analyzes viral content patterns from top creators in the productivity and mindset space, then generates batch-ready content ideas that you can quickly create and post across multiple social media platforms.

### 2. Action Claims Agent

A lightweight Python agent for tracking action claims, monitoring payouts, and sending notifications about claim expirations and new payouts. Features include:
- Data models for claims and payouts
- Pluggable scraping/API integration interfaces
- State persistence with JSON storage
- Payout tracking and change detection
- Email/console notifications
- GitHub Actions scheduling support
- Comprehensive CLI interface

📖 **[Read the Action Claims Agent Documentation](ACTION_CLAIMS_README.md)**

## ✨ Viral Content Finder Features

- 🔍 **Viral Content Analysis**: Analyzes trending posts to identify viral patterns
- 📊 **Category Performance**: Breaks down performance by content category (productivity, mindset, habits, etc.)
- 🎬 **Content Type Analysis**: Identifies which content types perform best (listicles, tutorials, transformations, etc.)
- 🚀 **Batch Content Generation**: Automatically generates 30+ content ideas based on viral patterns
- 📱 **Platform-Specific Formatting**: Formats posts for Instagram, TikTok, and YouTube
- 📅 **Posting Schedule**: Provides optimal posting times and frequencies
- 💾 **Export Functionality**: Exports all data to JSON for easy access

## ✨ Action Claims Agent Features

- 📊 **Data Models**: Clean dataclasses for claims and payouts
- 🔌 **Pluggable Architecture**: Extensible scraping/API client interfaces  
- 💰 **Payout Tracking**: Automatic detection of new payouts
- ⏰ **Expiration Tracking**: Monitors claim expiration dates
- 💾 **State Persistence**: JSON-based state tracking with change detection
- 📧 **Notifications**: Email and console notification support
- 🤖 **Scheduling**: GitHub Actions integration for automated runs
- 🖥️ **CLI Interface**: Command-line interface for manual and scheduled runs
- ✅ **Tested**: Comprehensive test suite

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

### Viral Content Finder

Run the main script to analyze viral content and generate batch ideas:

```bash
python3 productivity_mindset_agent.py
```

### Action Claims Agent

Run the claims agent once:

```bash
python claims_cli.py run-once
```

Run on a schedule (every 24 hours):

```bash
python claims_cli.py scheduled --interval 86400
```

See [ACTION_CLAIMS_README.md](ACTION_CLAIMS_README.md) for complete documentation.
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
