import pandas as pd
from datetime import datetime, timedelta

try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

# ============================================================================
# UPDATED NICHE SETTINGS - Storytelling, AI/Automation, Nostalgia
# ============================================================================

ENTERTAINMENT_NICHES = {
    "storytelling": [
        "story time", "reddit story", "true story", "AITA", "am I the", 
        "plot twist", "confession", "relationship advice", "life update"
    ],
    "ai_automation": [
        "AI tutorial", "automation", "ChatGPT", "machine learning", 
        "coding", "tech review", "AI tools", "productivity hack", 
        "software development", "AI news"
    ],
    "nostalgia": [
        "90s", "2000s", "throwback", "remember when", "nostalgia", 
        "childhood", "retro", "blast from the past", "used to", "vintage"
    ]
}

# Top creators by updated niches
VIRAL_CREATORS = {
    "storytelling": [
        "MrBallen", "RSlash", "Charlotte Dobre", "Mark Narrations", 
        "Reddit Brew", "Lost Genre"
    ],
    "ai_automation": [
        "Tech With Tim", "Fireship", "NetworkChuck", "ThePrimeagen", 
        "Tsoding", "Programming with Mosh"
    ],
    "nostalgia": [
        "Defunctland", "Company Man", "Super Eyepatch Wolf", "Emplemon", 
        "Billiam", "Quinton Reviews"
    ]
}

VIRAL_VIEWS = 50000
VIRAL_ENGAGEMENT = 5000
TRENDING_GROWTH = 2.0


def generate_mock_trends():
    """
    Generate mock trending data for the three niches:
    Storytelling, AI/Automation, and Nostalgia
    """
    return [
        # ===== STORYTELLING POSTS =====
        {
            "id": "post_001",
            "title": "AITA For Refusing To Give Up My Seat On The Plane",
            "niche": "storytelling",
            "creator": "RSlash",
            "views": 145000,
            "likes": 10200,
            "comments": 1800,
            "shares": 2700,
            "timestamp": datetime.now() - timedelta(hours=6),
            "growth_rate": 4.3
        },
        {
            "id": "post_002",
            "title": "My Roommate Had No Idea I Knew Everything",
            "niche": "storytelling",
            "creator": "Charlotte Dobre",
            "views": 125000,
            "likes": 8900,
            "comments": 1500,
            "shares": 2300,
            "timestamp": datetime.now() - timedelta(hours=12),
            "growth_rate": 4.1
        },
        {
            "id": "post_003",
            "title": "This Wedding Story Will Make Your Jaw Drop",
            "niche": "storytelling",
            "creator": "Mark Narrations",
            "views": 98000,
            "likes": 7100,
            "comments": 1200,
            "shares": 1900,
            "timestamp": datetime.now() - timedelta(hours=8),
            "growth_rate": 3.7
        },
        {
            "id": "post_010",
            "title": "My Family Disowned Me For This Reason",
            "niche": "storytelling",
            "creator": "Reddit Brew",
            "views": 134000,
            "likes": 9800,
            "comments": 1700,
            "shares": 2500,
            "timestamp": datetime.now() - timedelta(hours=11),
            "growth_rate": 4.4
        },

        # ===== AI/AUTOMATION POSTS =====
        {
            "id": "post_201",
            "title": "I Built an AI That Does My Job For Me (And Saved $10K)",
            "niche": "ai_automation",
            "creator": "Tech With Tim",
            "views": 156000,
            "likes": 11200,
            "comments": 2100,
            "shares": 3200,
            "timestamp": datetime.now() - timedelta(hours=5),
            "growth_rate": 4.8
        },
        {
            "id": "post_202",
            "title": "ChatGPT Just Changed Everything (Here's Why)",
            "niche": "ai_automation",
            "creator": "Fireship",
            "views": 142000,
            "likes": 10100,
            "comments": 1900,
            "shares": 2800,
            "timestamp": datetime.now() - timedelta(hours=9),
            "growth_rate": 4.2
        },
        {
            "id": "post_203",
            "title": "How To Automate Your Entire Workflow in 10 Minutes",
            "niche": "ai_automation",
            "creator": "NetworkChuck",
            "views": 118000,
            "likes": 8600,
            "comments": 1400,
            "shares": 2100,
            "timestamp": datetime.now() - timedelta(hours=7),
            "growth_rate": 3.9
        },
        {
            "id": "post_204",
            "title": "The Future of Programming (AI is Taking Over)",
            "niche": "ai_automation",
            "creator": "ThePrimeagen",
            "views": 127000,
            "likes": 9300,
            "comments": 1600,
            "shares": 2400,
            "timestamp": datetime.now() - timedelta(hours=10),
            "growth_rate": 4.1
        },
        {
            "id": "post_205",
            "title": "I Tested 5 AI Tools - This One Blew My Mind",
            "niche": "ai_automation",
            "creator": "Programming with Mosh",
            "views": 109000,
            "likes": 7900,
            "comments": 1300,
            "shares": 1950,
            "timestamp": datetime.now() - timedelta(hours=6),
            "growth_rate": 3.7
        },

        # ===== NOSTALGIA POSTS =====
        {
            "id": "post_301",
            "title": "Remember When McDonald's Had These Wild Toys",
            "niche": "nostalgia",
            "creator": "Defunctland",
            "views": 89000,
            "likes": 6200,
            "comments": 920,
            "shares": 1400,
            "timestamp": datetime.now() - timedelta(hours=10),
            "growth_rate": 3.2
        },
        {
            "id": "post_302",
            "title": "90s Cartoons That Would Never Get Made Today",
            "niche": "nostalgia",
            "creator": "Super Eyepatch Wolf",
            "views": 112000,
            "likes": 8100,
            "comments": 1300,
            "shares": 2100,
            "timestamp": datetime.now() - timedelta(hours=15),
            "growth_rate": 3.8
        },
        {
            "id": "post_303",
            "title": "Things Only 2000s Kids Will Understand",
            "niche": "nostalgia",
            "creator": "Emplemon",
            "views": 76000,
            "likes": 5400,
            "comments": 780,
            "shares": 1200,
            "timestamp": datetime.now() - timedelta(hours=5),
            "growth_rate": 2.9
        },
        {
            "id": "post_304",
            "title": "The Rise And Fall Of This Iconic 90s Brand",
            "niche": "nostalgia",
            "creator": "Company Man",
            "views": 102000,
            "likes": 7300,
            "comments": 1100,
            "shares": 1800,
            "timestamp": datetime.now() - timedelta(hours=13),
            "growth_rate": 3.5
        },
    ]


class ViralTrendAgent:
    """
    Analyzes viral trends across three focused entertainment niches:
    - Storytelling (Reddit stories, AITA, confessions)
    - AI/Automation (Tech tutorials, AI tools, coding content)
    - Nostalgia (90s/2000s content, throwbacks, retro reviews)
    """

    def __init__(self, posts):
        self.posts = posts
        self.viral_posts = []
        self.trending_posts = []
        self.niche_performance = {}
        self.creator_performance = {}

    def find_viral_posts(self):
        """Find posts that meet viral engagement thresholds."""
        for post in self.posts:
            total_engagement = post["likes"] + post["comments"] + post["shares"]

            if post["views"] >= VIRAL_VIEWS or total_engagement >= VIRAL_ENGAGEMENT:
                post["total_engagement"] = total_engagement
                post["engagement_rate"] = round((total_engagement / post["views"]) * 100, 2)
                self.viral_posts.append(post)

        return self.viral_posts

    def find_trending_posts(self):
        """Find posts with strong growth momentum."""
        for post in self.posts:
            if post["growth_rate"] >= TRENDING_GROWTH:
                self.trending_posts.append(post)

        return self.trending_posts

    def analyze_by_niche(self):
        """Analyze performance metrics for each niche."""
        niche_stats = {}

        for post in self.viral_posts:
            niche = post["niche"]
            if niche not in niche_stats:
                niche_stats[niche] = {
                    "count": 0,
                    "total_views": 0,
                    "total_engagement": 0,
                    "avg_growth": [],
                    "top_creators": []
                }

            niche_stats[niche]["count"] += 1
            niche_stats[niche]["total_views"] += post["views"]
            niche_stats[niche]["total_engagement"] += post["total_engagement"]
            niche_stats[niche]["avg_growth"].append(post["growth_rate"])

            if post["creator"] not in niche_stats[niche]["top_creators"]:
                niche_stats[niche]["top_creators"].append(post["creator"])

        for niche, stats in niche_stats.items():
            if stats["count"] > 0:
                stats["avg_views"] = round(stats["total_views"] / stats["count"])
                stats["avg_engagement"] = round(stats["total_engagement"] / stats["count"])
                stats["avg_growth_rate"] = round(sum(stats["avg_growth"]) / len(stats["avg_growth"]), 2)
                del stats["avg_growth"]

        self.niche_performance = niche_stats
        return niche_stats

    def analyze_by_creator(self):
        """Analyze performance metrics for each creator."""
        creator_stats = {}

        for post in self.viral_posts:
            creator = post["creator"]
            if creator not in creator_stats:
                creator_stats[creator] = {
                    "niche": post["niche"],
                    "viral_count": 0,
                    "total_views": 0,
                    "total_engagement": 0,
                    "avg_growth": []
                }

            creator_stats[creator]["viral_count"] += 1
            creator_stats[creator]["total_views"] += post["views"]
            creator_stats[creator]["total_engagement"] += post["total_engagement"]
            creator_stats[creator]["avg_growth"].append(post["growth_rate"])

        for creator, stats in creator_stats.items():
            if stats["viral_count"] > 0:
                stats["avg_views"] = round(stats["total_views"] / stats["viral_count"])
                stats["avg_engagement"] = round(stats["total_engagement"] / stats["viral_count"])
                stats["avg_growth_rate"] = round(sum(stats["avg_growth"]) / len(stats["avg_growth"]), 2)
                del stats["avg_growth"]

        self.creator_performance = creator_stats
        return creator_stats

    def get_content_strategy(self):
        """Get recommended content strategy for each niche."""
        strategy = {
            "storytelling": {
                "posting_frequency": "3-4x per week (Mon, Wed, Fri, Sun)",
                "best_times": "Evening (7-9 PM)",
                "batch_size": "20-30 videos per session",
                "production_time": "10-15 min per video",
                "automation_level": "Very High",
                "tools": ["Text-to-speech", "Stock footage", "Auto-captions"],
                "content_ideas": [
                    "Reddit AITA compilations",
                    "Relationship advice stories",
                    "Confession compilations",
                    "Plot twist compilations"
                ]
            },
            "ai_automation": {
                "posting_frequency": "2-3x per week (Tue, Thu, Sat)",
                "best_times": "Morning (9-11 AM) & Evening (7-9 PM)",
                "batch_size": "10-15 videos per session",
                "production_time": "20-30 min per video",
                "automation_level": "Medium",
                "tools": ["Screen recording", "Code editor", "AI voice narration"],
                "content_ideas": [
                    "AI tool reviews & tutorials",
                    "ChatGPT use cases",
                    "Automation workflow guides",
                    "Coding tutorials",
                    "Tech news breakdowns"
                ]
            },
            "nostalgia": {
                "posting_frequency": "2-3x per week (Tue, Thu, Sat)",
                "best_times": "Afternoon (2-4 PM)",
                "batch_size": "15-20 videos per session",
                "production_time": "15-20 min per video",
                "automation_level": "High",
                "tools": ["Archive footage", "Image search", "Voiceover AI"],
                "content_ideas": [
                    "90s/2000s brand history",
                    "Retro product reviews",
                    "Throwback compilations",
                    "Childhood memories",
                    "Forgotten trends explained"
                ]
            }
        }
        return strategy

    def export_results(self, filename="viral_trends"):
        """Export analysis results to CSV files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if self.viral_posts:
            df_viral = pd.DataFrame(self.viral_posts)
            viral_file = f"{filename}_viral_{timestamp}.csv"
            df_viral.to_csv(viral_file, index=False)
            print(f"✅ Exported viral posts to: {viral_file}")

        if self.trending_posts:
            df_trending = pd.DataFrame(self.trending_posts)
            trending_file = f"{filename}_trending_{timestamp}.csv"
            df_trending.to_csv(trending_file, index=False)
            print(f"✅ Exported trending posts to: {trending_file}")

        if self.niche_performance:
            df_niches = pd.DataFrame.from_dict(self.niche_performance, orient='index')
            niches_file = f"{filename}_niches_{timestamp}.csv"
            df_niches.to_csv(niches_file)
            print(f"✅ Exported niche analysis to: {niches_file}")

        if self.creator_performance:
            df_creators = pd.DataFrame.from_dict(self.creator_performance, orient='index')
            creators_file = f"{filename}_creators_{timestamp}.csv"
            df_creators.to_csv(creators_file)
            print(f"✅ Exported creator analysis to: {creators_file}")


def run_trend_agent():
    """Main function to run the viral trend analysis."""
    print("=" * 70)
    print("FACELESS CONTENT STRATEGY - 3 UPDATED NICHES")
    print("Storytelling | AI/Automation | Nostalgia")
    print("=" * 70)
    print()

    print("Loading trending posts...")
    posts = generate_mock_trends()
    print(f"Analyzing {len(posts)} posts across 3 focused niches\n")

    agent = ViralTrendAgent(posts)

    print("Step 1: Finding viral posts...")
    viral = agent.find_viral_posts()
    print(f"Found {len(viral)} viral posts\n")

    print("Step 2: Finding trending posts...")
    trending = agent.find_trending_posts()
    print(f"Found {len(trending)} trending posts\n")

    print("=" * 70)
    print("VIRAL POSTS")
    print("=" * 70)
    for i, post in enumerate(viral, 1):
        print(f"\n{i}. {post['title']}")
        print(f"   Creator: {post['creator']} | Niche: {post['niche']}")
        print(f"   Views: {post['views']:,} | Engagement: {post['total_engagement']:,}")
        print(f"   Engagement Rate: {post['engagement_rate']}%")
        print(f"   Growth Rate: {post['growth_rate']}x")

    print("\n" + "=" * 70)
    print("NICHE PERFORMANCE ANALYSIS")
    print("=" * 70)
    niche_stats = agent.analyze_by_niche()

    for niche, stats in niche_stats.items():
        print(f"\n{niche.upper()}")
        print(f"  Viral Posts: {stats['count']}")
        print(f"  Avg Views: {stats['avg_views']:,}")
        print(f"  Avg Engagement: {stats['avg_engagement']:,}")
        print(f"  Avg Growth: {stats['avg_growth_rate']}x")
        print(f"  Active Creators: {', '.join(stats['top_creators'])}")

    print("\n" + "=" * 70)
    print("TOP VIRAL CREATORS")
    print("=" * 70)
    creator_stats = agent.analyze_by_creator()

    for creator, stats in sorted(creator_stats.items(),
                                  key=lambda x: x[1]['avg_engagement'],
                                  reverse=True):
        print(f"\n{creator}")
        print(f"  Niche: {stats['niche']}")
        print(f"  Viral Posts: {stats['viral_count']}")
        print(f"  Avg Views: {stats['avg_views']:,}")
        print(f"  Avg Engagement: {stats['avg_engagement']:,}")
        print(f"  Growth Rate: {stats['avg_growth_rate']}x")

    print("\n" + "=" * 70)
    print("RECOMMENDED CREATORS TO STUDY")
    print("=" * 70)
    for niche, creators in VIRAL_CREATORS.items():
        print(f"\n{niche.upper()}:")
        print(f"  {', '.join(creators)}")

    print("\n" + "=" * 70)
    print("CONTENT STRATEGY GUIDE")
    print("=" * 70)
    strategy = agent.get_content_strategy()

    for niche, guide in strategy.items():
        print(f"\n{niche.upper()}")
        print(f"  Frequency: {guide['posting_frequency']}")
        print(f"  Best Times: {guide['best_times']}")
        print(f"  Batch Size: {guide['batch_size']}")
        print(f"  Production Time: {guide['production_time']}")
        print(f"  Automation: {guide['automation_level']}")
        print(f"  Tools: {', '.join(guide['tools'])}")
        print(f"  Content Ideas:")
        for idea in guide['content_ideas']:
            print(f"    • {idea}")

    print("\n" + "=" * 70)
    print("WEEKLY CONTENT CALENDAR")
    print("=" * 70)
    print("\nMonday: Storytelling (AITA/Reddit)")
    print("Tuesday: AI/Automation (Tech tutorials)")
    print("Wednesday: Storytelling OR AI/Automation")
    print("Thursday: AI/Automation (Reviews/News)")
    print("Friday: Nostalgia (Throwbacks)")
    print("Saturday: AI/Automation OR Nostalgia")
    print("Sunday: Storytelling (High-engagement)")

    print("\n" + "=" * 70)
    print("EXPORTING RESULTS")
    print("=" * 70)
    agent.export_results("faceless_content_strategy")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE ✅")
    print("=" * 70)


if __name__ == "__main__":
    run_trend_agent()
