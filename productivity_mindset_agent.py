"""
Viral Productivity/Mindset Content Finder

This script finds viral entertainment content in the Productivity/Mindset niche
that can be batch created and posted to social media pages.

Features:
- Identifies viral content patterns in productivity/mindset space
- Generates batch-ready social media posts
- Provides content ideas and templates
- Analyzes top performing content types
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

# ============================================================================
# PRODUCTIVITY/MINDSET NICHE CONFIGURATION
# ============================================================================

PRODUCTIVITY_MINDSET_KEYWORDS = {
    "productivity": [
        "productivity hack", "time management", "morning routine", 
        "daily habits", "workflow optimization", "focus technique",
        "productivity tips", "get more done", "work smarter", "efficiency"
    ],
    "mindset": [
        "growth mindset", "positive thinking", "motivation", "self-improvement",
        "mental strength", "success mindset", "mindset shift", "limiting beliefs",
        "confidence", "discipline"
    ],
    "habits": [
        "atomic habits", "habit stacking", "build habits", "break bad habits",
        "consistent routine", "30-day challenge", "habit tracker", "daily practice"
    ],
    "goal_setting": [
        "goal setting", "vision board", "manifestation", "yearly goals",
        "smart goals", "action plan", "milestone", "achievement"
    ],
    "personal_development": [
        "self-development", "personal growth", "life lessons", "wisdom",
        "entrepreneur mindset", "success principles", "level up", "transformation"
    ]
}

# Top creators in Productivity/Mindset niche
TOP_CREATORS = {
    "productivity": [
        "Ali Abdaal", "Thomas Frank", "Matt D'Avella", "Nathaniel Drew",
        "Better Ideas", "Mike Dee", "Ruri Ohama"
    ],
    "mindset": [
        "Jay Shetty", "Tom Bilyeu", "Mel Robbins", "Tony Robbins",
        "Lewis Howes", "Ed Mylett", "Brendon Burchard"
    ],
    "mixed": [
        "Andrew Huberman", "Diary Of A CEO", "Tim Ferriss", "Gary Vee",
        "Alex Hormozi", "Cal Newport"
    ]
}

# Viral thresholds
VIRAL_VIEWS = 50000
VIRAL_ENGAGEMENT = 5000
TRENDING_GROWTH = 2.0


def generate_productivity_mindset_trends() -> List[Dict[str, Any]]:
    """
    Generate mock trending data for Productivity/Mindset niche.
    In production, this would connect to social media APIs.
    """
    return [
        # High-performing productivity content
        {
            "id": "prod_001",
            "title": "5 Morning Habits That Changed My Life",
            "category": "productivity",
            "creator": "Ali Abdaal",
            "views": 245000,
            "likes": 18200,
            "comments": 3400,
            "shares": 5100,
            "timestamp": datetime.now() - timedelta(hours=8),
            "growth_rate": 4.8,
            "content_type": "listicle",
            "hook": "I tried these 5 morning habits for 30 days..."
        },
        {
            "id": "prod_002",
            "title": "The 2-Minute Rule That Makes You Unstoppable",
            "category": "habits",
            "creator": "Thomas Frank",
            "views": 189000,
            "likes": 14500,
            "comments": 2800,
            "shares": 4200,
            "timestamp": datetime.now() - timedelta(hours=12),
            "growth_rate": 4.3,
            "content_type": "educational",
            "hook": "This simple rule changed everything..."
        },
        {
            "id": "prod_003",
            "title": "How I 10x'd My Productivity in 90 Days",
            "category": "productivity",
            "creator": "Matt D'Avella",
            "views": 167000,
            "likes": 12800,
            "comments": 2500,
            "shares": 3800,
            "timestamp": datetime.now() - timedelta(hours=15),
            "growth_rate": 4.1,
            "content_type": "personal_story",
            "hook": "3 months ago, I was burned out..."
        },
        
        # High-performing mindset content
        {
            "id": "mind_001",
            "title": "The Mindset Shift That Made Me a Millionaire",
            "category": "mindset",
            "creator": "Alex Hormozi",
            "views": 312000,
            "likes": 23400,
            "comments": 4200,
            "shares": 6800,
            "timestamp": datetime.now() - timedelta(hours=6),
            "growth_rate": 5.2,
            "content_type": "transformation",
            "hook": "I used to think success was about luck..."
        },
        {
            "id": "mind_002",
            "title": "Why 99% of People Stay Average (And How to Break Free)",
            "category": "mindset",
            "creator": "Jay Shetty",
            "views": 278000,
            "likes": 21100,
            "comments": 3900,
            "shares": 6200,
            "timestamp": datetime.now() - timedelta(hours=10),
            "growth_rate": 4.9,
            "content_type": "motivational",
            "hook": "The difference between successful people and average people..."
        },
        {
            "id": "mind_003",
            "title": "One Question That Changed My Entire Life",
            "category": "personal_development",
            "creator": "Tom Bilyeu",
            "views": 234000,
            "likes": 17800,
            "comments": 3200,
            "shares": 5400,
            "timestamp": datetime.now() - timedelta(hours=14),
            "growth_rate": 4.5,
            "content_type": "insight",
            "hook": "If you ask yourself this one question every day..."
        },
        
        # Goal setting and habit content
        {
            "id": "goal_001",
            "title": "How to Actually Achieve Your Goals (Not Just Set Them)",
            "category": "goal_setting",
            "creator": "Better Ideas",
            "views": 198000,
            "likes": 15200,
            "comments": 2900,
            "shares": 4500,
            "timestamp": datetime.now() - timedelta(hours=9),
            "growth_rate": 4.2,
            "content_type": "tutorial",
            "hook": "Most people set goals wrong..."
        },
        {
            "id": "habit_001",
            "title": "I Tracked My Habits for 365 Days - Here's What Happened",
            "category": "habits",
            "creator": "Nathaniel Drew",
            "views": 156000,
            "likes": 11900,
            "comments": 2300,
            "shares": 3600,
            "timestamp": datetime.now() - timedelta(hours=11),
            "growth_rate": 3.9,
            "content_type": "experiment",
            "hook": "One year ago, I started an experiment..."
        },
        {
            "id": "habit_002",
            "title": "The Habit Stack That Changed Everything",
            "category": "habits",
            "creator": "Mike Dee",
            "views": 142000,
            "likes": 10800,
            "comments": 2100,
            "shares": 3300,
            "timestamp": datetime.now() - timedelta(hours=7),
            "growth_rate": 3.7,
            "content_type": "framework",
            "hook": "Instead of trying to build multiple habits..."
        },
        
        # Personal development
        {
            "id": "dev_001",
            "title": "7 Life Lessons I Wish I Knew at 20",
            "category": "personal_development",
            "creator": "Diary Of A CEO",
            "views": 289000,
            "likes": 22300,
            "comments": 4100,
            "shares": 6500,
            "timestamp": datetime.now() - timedelta(hours=5),
            "growth_rate": 5.0,
            "content_type": "wisdom",
            "hook": "If I could go back in time..."
        },
        {
            "id": "prod_004",
            "title": "The Dark Side of Productivity No One Talks About",
            "category": "productivity",
            "creator": "Ruri Ohama",
            "views": 178000,
            "likes": 13600,
            "comments": 2700,
            "shares": 4100,
            "timestamp": datetime.now() - timedelta(hours=13),
            "growth_rate": 4.0,
            "content_type": "contrarian",
            "hook": "Everyone talks about being productive, but..."
        },
        {
            "id": "mind_004",
            "title": "This Mental Model Changed How I See Everything",
            "category": "mindset",
            "creator": "Andrew Huberman",
            "views": 267000,
            "likes": 20400,
            "comments": 3700,
            "shares": 5900,
            "timestamp": datetime.now() - timedelta(hours=4),
            "growth_rate": 4.7,
            "content_type": "science",
            "hook": "Our brains are wired to..."
        },
    ]


class ProductivityMindsetAgent:
    """
    Analyzes viral trends in Productivity/Mindset niche and generates
    batch content ideas for social media posting.
    """
    
    def __init__(self, posts: List[Dict[str, Any]]):
        self.posts = posts
        self.viral_posts = []
        self.trending_posts = []
        self.category_performance = {}
        self.content_type_performance = {}
        
    def find_viral_posts(self) -> List[Dict[str, Any]]:
        """Identify posts that meet viral engagement thresholds."""
        for post in self.posts:
            total_engagement = post["likes"] + post["comments"] + post["shares"]
            
            if post["views"] >= VIRAL_VIEWS or total_engagement >= VIRAL_ENGAGEMENT:
                post["total_engagement"] = total_engagement
                post["engagement_rate"] = round((total_engagement / post["views"]) * 100, 2)
                self.viral_posts.append(post)
        
        return self.viral_posts
    
    def find_trending_posts(self) -> List[Dict[str, Any]]:
        """Identify posts with strong growth momentum."""
        for post in self.posts:
            if post["growth_rate"] >= TRENDING_GROWTH:
                self.trending_posts.append(post)
        
        return self.trending_posts
    
    def analyze_by_category(self) -> Dict[str, Any]:
        """Analyze performance by content category."""
        category_stats = {}
        
        for post in self.viral_posts:
            category = post["category"]
            if category not in category_stats:
                category_stats[category] = {
                    "count": 0,
                    "total_views": 0,
                    "total_engagement": 0,
                    "avg_growth": [],
                    "content_types": set()
                }
            
            category_stats[category]["count"] += 1
            category_stats[category]["total_views"] += post["views"]
            category_stats[category]["total_engagement"] += post["total_engagement"]
            category_stats[category]["avg_growth"].append(post["growth_rate"])
            category_stats[category]["content_types"].add(post["content_type"])
        
        # Calculate averages
        for category, stats in category_stats.items():
            if stats["count"] > 0:
                stats["avg_views"] = round(stats["total_views"] / stats["count"])
                stats["avg_engagement"] = round(stats["total_engagement"] / stats["count"])
                stats["avg_growth_rate"] = round(sum(stats["avg_growth"]) / len(stats["avg_growth"]), 2)
                stats["content_types"] = list(stats["content_types"])
                del stats["avg_growth"]
        
        self.category_performance = category_stats
        return category_stats
    
    def analyze_by_content_type(self) -> Dict[str, Any]:
        """Analyze performance by content type."""
        type_stats = {}
        
        for post in self.viral_posts:
            content_type = post["content_type"]
            if content_type not in type_stats:
                type_stats[content_type] = {
                    "count": 0,
                    "total_views": 0,
                    "total_engagement": 0,
                    "examples": []
                }
            
            type_stats[content_type]["count"] += 1
            type_stats[content_type]["total_views"] += post["views"]
            type_stats[content_type]["total_engagement"] += post["total_engagement"]
            if len(type_stats[content_type]["examples"]) < 2:
                type_stats[content_type]["examples"].append(post["title"])
        
        # Calculate averages
        for content_type, stats in type_stats.items():
            if stats["count"] > 0:
                stats["avg_views"] = round(stats["total_views"] / stats["count"])
                stats["avg_engagement"] = round(stats["total_engagement"] / stats["count"])
        
        self.content_type_performance = type_stats
        return type_stats
    
    def generate_batch_content_ideas(self, count: int = 30) -> List[Dict[str, Any]]:
        """
        Generate batch content ideas based on viral patterns.
        
        Args:
            count: Number of content ideas to generate (default: 30)
        
        Returns:
            List of content ideas ready for batch creation
        """
        content_templates = []
        
        # Templates based on viral patterns
        productivity_templates = [
            {"title": "5 {topic} Habits That Will Change Your Life", "category": "productivity", "type": "listicle"},
            {"title": "How I {achievement} in {timeframe} (Step-by-Step)", "category": "productivity", "type": "tutorial"},
            {"title": "The {number}-Minute Rule for {goal}", "category": "productivity", "type": "framework"},
            {"title": "I Tried {challenge} for {days} Days - Here's What Happened", "category": "productivity", "type": "experiment"},
            {"title": "{number} Productivity Hacks That Actually Work", "category": "productivity", "type": "listicle"},
        ]
        
        mindset_templates = [
            {"title": "The Mindset Shift That Made Me {achievement}", "category": "mindset", "type": "transformation"},
            {"title": "Why Most People {struggle} (And How to Break Free)", "category": "mindset", "type": "motivational"},
            {"title": "One {thing} That Changed My Entire {aspect}", "category": "mindset", "type": "insight"},
            {"title": "The Mental Model That {benefit}", "category": "mindset", "type": "framework"},
            {"title": "{number} Mindset Shifts for {goal}", "category": "mindset", "type": "listicle"},
        ]
        
        habits_templates = [
            {"title": "How to Build {habit} in {timeframe}", "category": "habits", "type": "tutorial"},
            {"title": "The Habit Stack That {benefit}", "category": "habits", "type": "framework"},
            {"title": "I Tracked My {habit} for {days} Days - Results", "category": "habits", "type": "experiment"},
            {"title": "{number} Habits of {successful_people}", "category": "habits", "type": "listicle"},
        ]
        
        goal_templates = [
            {"title": "How to Actually Achieve Your {goal_type} Goals", "category": "goal_setting", "type": "tutorial"},
            {"title": "The Goal-Setting Framework That {benefit}", "category": "goal_setting", "type": "framework"},
            {"title": "{number} Steps to {achievement}", "category": "goal_setting", "type": "tutorial"},
        ]
        
        development_templates = [
            {"title": "{number} Life Lessons I Wish I Knew at {age}", "category": "personal_development", "type": "wisdom"},
            {"title": "The Dark Side of {topic} No One Talks About", "category": "personal_development", "type": "contrarian"},
            {"title": "{number} Things Successful People Do Differently", "category": "personal_development", "type": "listicle"},
        ]
        
        all_templates = (
            productivity_templates + mindset_templates + 
            habits_templates + goal_templates + development_templates
        )
        
        # Generate content ideas
        import random
        
        variables = {
            "topic": ["Morning", "Evening", "Daily", "Weekly", "Work", "Focus"],
            "achievement": ["10x My Productivity", "Doubled My Income", "Built a $1M Business"],
            "timeframe": ["30 Days", "90 Days", "6 Months", "1 Year"],
            "number": ["3", "5", "7", "10"],
            "goal": ["Maximum Focus", "Peak Performance", "Success", "Getting More Done"],
            "challenge": ["Waking Up at 5AM", "Cold Showers", "No Social Media"],
            "days": ["7", "14", "30", "60", "90"],
            "struggle": ["Stay Stuck", "Fail", "Give Up", "Stay Average"],
            "thing": ["Question", "Principle", "Habit", "Decision"],
            "aspect": ["Life", "Career", "Business", "Mindset"],
            "benefit": ["Changed Everything", "Doubled My Results", "Made Me Unstoppable"],
            "habit": ["Morning Routine", "Meditation", "Journaling", "Exercise"],
            "successful_people": ["Millionaires", "High Achievers", "Top Performers"],
            "goal_type": ["Career", "Business", "Life", "Financial"],
            "age": ["20", "25", "30"],
        }
        
        generated_ideas = []
        for i in range(min(count, len(all_templates) * 3)):
            template = random.choice(all_templates)
            title = template["title"]
            
            # Replace variables in template
            for var, options in variables.items():
                if f"{{{var}}}" in title:
                    title = title.replace(f"{{{var}}}", random.choice(options))
            
            idea = {
                "id": f"batch_{i+1:03d}",
                "title": title,
                "category": template["category"],
                "content_type": template["type"],
                "script_outline": self._generate_script_outline(template["type"]),
                "posting_platform": ["Instagram Reels", "TikTok", "YouTube Shorts"],
                "estimated_production_time": "10-15 minutes",
                "batch_group": (i // 10) + 1  # Group into batches of 10
            }
            generated_ideas.append(idea)
        
        return generated_ideas[:count]
    
    def _generate_script_outline(self, content_type: str) -> List[str]:
        """Generate a basic script outline based on content type."""
        outlines = {
            "listicle": [
                "Hook: Strong opening question or statement",
                "Point 1: First item with brief explanation",
                "Point 2: Second item with example",
                "Point 3: Third item with benefit",
                "Call-to-action: Follow for more"
            ],
            "tutorial": [
                "Hook: Promise transformation",
                "Problem: What people struggle with",
                "Solution: Your step-by-step method",
                "Results: What they can achieve",
                "CTA: Try it and tag me"
            ],
            "transformation": [
                "Hook: Where you started",
                "Journey: What changed",
                "Breakthrough: The key moment",
                "Results: Where you are now",
                "CTA: You can do this too"
            ],
            "experiment": [
                "Hook: The challenge you took",
                "Day 1-7: Initial struggles",
                "Day 8-21: Progress and insights",
                "Final Results: What you learned",
                "CTA: Would you try this?"
            ],
            "motivational": [
                "Hook: Bold statement",
                "The Truth: Reality check",
                "The Path: What to do instead",
                "The Promise: What's possible",
                "CTA: Start today"
            ],
            "framework": [
                "Hook: Introduce the concept",
                "Explain: How it works",
                "Example: Real-world application",
                "Benefits: Why it's powerful",
                "CTA: Apply this now"
            ],
            "default": [
                "Hook: Grab attention",
                "Body: Deliver value",
                "CTA: Engage audience"
            ]
        }
        
        return outlines.get(content_type, outlines["default"])
    
    def format_for_social_media(self, content_idea: Dict[str, Any], platform: str = "instagram") -> str:
        """
        Format content idea for specific social media platform.
        
        Args:
            content_idea: The content idea dictionary
            platform: Target platform (instagram, tiktok, youtube)
        
        Returns:
            Formatted post text
        """
        title = content_idea["title"]
        category = content_idea["category"]
        
        # Platform-specific formatting
        if platform.lower() == "instagram":
            hashtags = self._generate_hashtags(category, count=10)
            post = f"{title}\n\n"
            post += ".\n" * 3  # Spacing
            post += " ".join(hashtags)
            
        elif platform.lower() == "tiktok":
            hashtags = self._generate_hashtags(category, count=5)
            post = f"{title}\n\n"
            post += " ".join(hashtags)
            
        elif platform.lower() == "youtube":
            post = f"{title}\n\n"
            post += self._generate_youtube_description(category)
            
        else:
            post = title
        
        return post
    
    def _generate_hashtags(self, category: str, count: int = 10) -> List[str]:
        """Generate relevant hashtags for the category."""
        hashtag_pool = {
            "productivity": [
                "#productivity", "#productivityhacks", "#timemanagement",
                "#getthingsdone", "#efficency", "#worksmarter", "#focusmode",
                "#productivitytips", "#organize", "#planning"
            ],
            "mindset": [
                "#mindset", "#growthmindset", "#motivation", "#success",
                "#positivemindset", "#successmindset", "#mindsetcoach",
                "#personaldevelopment", "#selfimprovement", "#transformation"
            ],
            "habits": [
                "#habits", "#habittracker", "#dailyhabits", "#goodhabits",
                "#habitstacking", "#routine", "#consistency", "#discipline",
                "#atomichabits", "#habitbuilding"
            ],
            "goal_setting": [
                "#goals", "#goalsetting", "#goaldigger", "#achieveyourgoals",
                "#dreamgoals", "#goalgetter", "#smartgoals", "#vision",
                "#planning", "#success"
            ],
            "personal_development": [
                "#personaldevelopment", "#selfimprovement", "#growyourself",
                "#levelup", "#betterme", "#selfgrowth", "#development",
                "#lifecoach", "#personalgrowth", "#transformation"
            ]
        }
        
        tags = hashtag_pool.get(category, hashtag_pool["productivity"])
        return tags[:count]
    
    def _generate_youtube_description(self, category: str) -> str:
        """Generate YouTube video description."""
        description = "In this video, I share insights about {category}.\n\n".format(
            category=category.replace("_", " ").title()
        )
        description += "🔔 Subscribe for more productivity and mindset content!\n\n"
        description += "📱 Follow me on social media:\n"
        description += "Instagram: @youraccount\n"
        description += "TikTok: @youraccount\n\n"
        description += "⏰ Timestamps:\n"
        description += "0:00 - Introduction\n"
        description += "0:30 - Main Content\n"
        description += "2:00 - Key Takeaways\n\n"
        return description
    
    def export_batch_content(self, content_ideas: List[Dict[str, Any]], filename: str = "batch_content"):
        """Export batch content ideas to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{filename}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_at": timestamp,
                "total_ideas": len(content_ideas),
                "content_ideas": content_ideas
            }, f, indent=2, default=str)
        
        print(f"✅ Exported {len(content_ideas)} content ideas to: {output_file}")
        return output_file
    
    def get_posting_schedule(self, posts_per_week: int = 7) -> Dict[str, Any]:
        """Generate optimal posting schedule."""
        schedule = {
            "Monday": {
                "time": "9:00 AM",
                "category": "productivity",
                "rationale": "Start week strong with productivity content"
            },
            "Tuesday": {
                "time": "7:00 PM",
                "category": "mindset",
                "rationale": "Evening motivation after work"
            },
            "Wednesday": {
                "time": "12:00 PM",
                "category": "habits",
                "rationale": "Midweek habit check-in"
            },
            "Thursday": {
                "time": "9:00 AM",
                "category": "productivity",
                "rationale": "Productivity boost before weekend"
            },
            "Friday": {
                "time": "6:00 PM",
                "category": "goal_setting",
                "rationale": "Weekend planning and goals"
            },
            "Saturday": {
                "time": "10:00 AM",
                "category": "personal_development",
                "rationale": "Weekend self-improvement"
            },
            "Sunday": {
                "time": "8:00 PM",
                "category": "mindset",
                "rationale": "Sunday motivation for upcoming week"
            }
        }
        
        return schedule


def main():
    """Main function to run the Productivity/Mindset content finder."""
    print("=" * 80)
    print("VIRAL CONTENT FINDER - PRODUCTIVITY/MINDSET NICHE")
    print("Batch Content Creation for Social Media")
    print("=" * 80)
    print()
    
    # Load trending posts
    print("📊 Loading trending productivity/mindset content...")
    posts = generate_productivity_mindset_trends()
    print(f"✅ Analyzing {len(posts)} viral posts\n")
    
    # Initialize agent
    agent = ProductivityMindsetAgent(posts)
    
    # Find viral and trending content
    print("🔍 Step 1: Finding viral posts...")
    viral_posts = agent.find_viral_posts()
    print(f"✅ Found {len(viral_posts)} viral posts\n")
    
    print("📈 Step 2: Finding trending posts...")
    trending_posts = agent.find_trending_posts()
    print(f"✅ Found {len(trending_posts)} trending posts\n")
    
    # Analyze patterns
    print("=" * 80)
    print("📊 VIRAL CONTENT ANALYSIS")
    print("=" * 80)
    
    print("\n🔥 TOP 5 VIRAL POSTS:")
    for i, post in enumerate(sorted(viral_posts, key=lambda x: x["views"], reverse=True)[:5], 1):
        print(f"\n{i}. {post['title']}")
        print(f"   👤 Creator: {post['creator']}")
        print(f"   📁 Category: {post['category']} | Type: {post['content_type']}")
        print(f"   👁  Views: {post['views']:,} | 💬 Engagement: {post['total_engagement']:,}")
        print(f"   📊 Engagement Rate: {post['engagement_rate']}% | 📈 Growth: {post['growth_rate']}x")
        print(f"   🎣 Hook: {post['hook']}")
    
    # Category analysis
    print("\n" + "=" * 80)
    print("📂 CATEGORY PERFORMANCE")
    print("=" * 80)
    category_stats = agent.analyze_by_category()
    
    for category, stats in sorted(category_stats.items(), key=lambda x: x[1]["avg_engagement"], reverse=True):
        print(f"\n📁 {category.upper().replace('_', ' ')}")
        print(f"   Viral Posts: {stats['count']}")
        print(f"   Avg Views: {stats['avg_views']:,}")
        print(f"   Avg Engagement: {stats['avg_engagement']:,}")
        print(f"   Avg Growth: {stats['avg_growth_rate']}x")
        print(f"   Content Types: {', '.join(stats['content_types'])}")
    
    # Content type analysis
    print("\n" + "=" * 80)
    print("🎬 CONTENT TYPE PERFORMANCE")
    print("=" * 80)
    type_stats = agent.analyze_by_content_type()
    
    for content_type, stats in sorted(type_stats.items(), key=lambda x: x[1]["avg_views"], reverse=True):
        print(f"\n🎥 {content_type.upper().replace('_', ' ')}")
        print(f"   Count: {stats['count']}")
        print(f"   Avg Views: {stats['avg_views']:,}")
        print(f"   Avg Engagement: {stats['avg_engagement']:,}")
        print(f"   Examples:")
        for example in stats['examples']:
            print(f"     • {example}")
    
    # Generate batch content
    print("\n" + "=" * 80)
    print("🚀 GENERATING BATCH CONTENT IDEAS")
    print("=" * 80)
    
    batch_size = 30
    print(f"\n⚡ Generating {batch_size} content ideas based on viral patterns...")
    content_ideas = agent.generate_batch_content_ideas(count=batch_size)
    print(f"✅ Generated {len(content_ideas)} content ideas\n")
    
    # Show sample ideas
    print("📝 SAMPLE CONTENT IDEAS (First 5):")
    for i, idea in enumerate(content_ideas[:5], 1):
        print(f"\n{i}. {idea['title']}")
        print(f"   Category: {idea['category']} | Type: {idea['content_type']}")
        print(f"   Batch Group: {idea['batch_group']}")
        print(f"   Production Time: {idea['estimated_production_time']}")
        print(f"   Platforms: {', '.join(idea['posting_platform'])}")
    
    # Show posting schedule
    print("\n" + "=" * 80)
    print("📅 RECOMMENDED POSTING SCHEDULE")
    print("=" * 80)
    schedule = agent.get_posting_schedule()
    
    for day, details in schedule.items():
        print(f"\n{day}:")
        print(f"  ⏰ Time: {details['time']}")
        print(f"  📁 Category: {details['category']}")
        print(f"  💡 Why: {details['rationale']}")
    
    # Export batch content
    print("\n" + "=" * 80)
    print("💾 EXPORTING BATCH CONTENT")
    print("=" * 80)
    output_file = agent.export_batch_content(content_ideas)
    
    # Show platform-specific formatting example
    print("\n" + "=" * 80)
    print("📱 PLATFORM-SPECIFIC FORMATTING EXAMPLE")
    print("=" * 80)
    
    sample_idea = content_ideas[0]
    
    print("\n📸 INSTAGRAM FORMAT:")
    print("-" * 80)
    print(agent.format_for_social_media(sample_idea, "instagram"))
    
    print("\n\n🎵 TIKTOK FORMAT:")
    print("-" * 80)
    print(agent.format_for_social_media(sample_idea, "tiktok"))
    
    print("\n\n▶️  YOUTUBE FORMAT:")
    print("-" * 80)
    print(agent.format_for_social_media(sample_idea, "youtube"))
    
    # Final summary
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"""
📊 Summary:
  • Analyzed {len(posts)} trending posts
  • Identified {len(viral_posts)} viral posts
  • Found {len(trending_posts)} trending posts
  • Generated {len(content_ideas)} batch content ideas
  • Created posting schedule for 7 days/week
  • Exported data to: {output_file}

🎯 Next Steps:
  1. Review the generated content ideas in {output_file}
  2. Batch create videos using the script outlines
  3. Follow the posting schedule for optimal engagement
  4. Track performance and iterate on successful patterns
  5. Rerun this analysis weekly to stay current with trends

💡 Pro Tips:
  • Focus on content types with highest engagement
  • Use proven hooks from viral posts
  • Maintain consistency with daily posting
  • Engage with comments within first hour
  • Cross-post to all platforms for maximum reach

Happy creating! 🚀
""")


if __name__ == "__main__":
    main()
