"""
Example Usage Guide for Viral Trend Agent

This file demonstrates how to use the ViralTrendAgent and CSVHandler
in practical scenarios. Each example is beginner-friendly with comments.
"""

from viral_trend_agent import ViralTrendAgent, generate_mock_trends
from csv_handler import CSVHandler, get_csv_handler

print("=" * 70)
print("VIRAL TREND AGENT - EXAMPLE USAGE")
print("=" * 70)
print()

# ============================================================================
# EXAMPLE 1: Basic Usage - Run the Agent
# ============================================================================

print("EXAMPLE 1: Basic Usage - Run the Trend Agent")
print("-" * 70)

# Step 1: Generate mock trending data
posts = generate_mock_trends()
print(f"✓ Generated {len(posts)} mock posts\n")

# Step 2: Create an agent instance
agent = ViralTrendAgent(posts)
print("✓ Created ViralTrendAgent instance\n")

# Step 3: Find viral posts
viral_posts = agent.find_viral_posts()
print(f"✓ Found {len(viral_posts)} viral posts")
print(f"  Sample: {viral_posts[0]['title']}\n")

# Step 4: Find trending posts
trending_posts = agent.find_trending_posts()
print(f"✓ Found {len(trending_posts)} trending posts")
print(f"  Sample growth rate: {trending_posts[0]['growth_rate']}x\n")

print()

# ============================================================================
# EXAMPLE 2: Analyze Performance by Niche
# ============================================================================

print("EXAMPLE 2: Analyze Performance by Niche")
print("-" * 70)

niche_performance = agent.analyze_by_niche()

for niche, stats in niche_performance.items():
    print(f"\n📊 {niche.upper()}")
    print(f"   Viral Posts: {stats['count']}")
    print(f"   Average Views: {stats['avg_views']:,}")
    print(f"   Average Engagement: {stats['avg_engagement']:,}")
    print(f"   Average Growth Rate: {stats['avg_growth_rate']}x")
    print(f"   Top Creators: {', '.join(stats['top_creators'])}")

print()
print()

# ============================================================================
# EXAMPLE 3: Analyze Performance by Creator
# ============================================================================

print("EXAMPLE 3: Analyze Performance by Creator")
print("-" * 70)

creator_performance = agent.analyze_by_creator()

# Sort creators by engagement
sorted_creators = sorted(creator_performance.items(),
                        key=lambda x: x[1]['avg_engagement'],
                        reverse=True)

for creator, stats in sorted_creators[:3]:  # Show top 3
    print(f"\n👤 {creator}")
    print(f"   Niche: {stats['niche']}")
    print(f"   Viral Posts: {stats['viral_count']}")
    print(f"   Average Views: {stats['avg_views']:,}")
    print(f"   Average Engagement: {stats['avg_engagement']:,}")
    print(f"   Average Growth Rate: {stats['avg_growth_rate']}x")

print()
print()

# ============================================================================
# EXAMPLE 4: Get Content Strategy Recommendations
# ============================================================================

print("EXAMPLE 4: Content Strategy Recommendations")
print("-" * 70)

strategy = agent.get_content_strategy()

for niche, guide in strategy.items():
    print(f"\n📝 {niche.upper()} Strategy:")
    print(f"   Posting Frequency: {guide['posting_frequency']}")
    print(f"   Best Times: {guide['best_times']}")
    print(f"   Batch Size: {guide['batch_size']}")
    print(f"   Production Time: {guide['production_time']}")
    print(f"   Automation Level: {guide['automation_level']}")
    print(f"   Tools: {', '.join(guide['tools'][:2])}...")  # Show first 2 tools
    print(f"   Content Ideas:")
    for idea in guide['content_ideas'][:2]:  # Show first 2 ideas
        print(f"     • {idea}")

print()
print()

# ============================================================================
# EXAMPLE 5: Export Results to CSV
# ============================================================================

print("EXAMPLE 5: Export Results to CSV Files")
print("-" * 70)

# Method 1: Using the agent's built-in export
print("\nExporting results using agent.export_results()...")
agent.export_results("example_output")
print("✓ Files exported successfully!")

print()
print()

# ============================================================================
# EXAMPLE 6: Using the CSV Handler
# ============================================================================

print("EXAMPLE 6: Using the CSV Handler")
print("-" * 70)

# Create a CSV handler instance
handler = get_csv_handler()

# Get the viral posts and prepare for CSV export
viral_data = agent.viral_posts

print(f"\nPreparing to save {len(viral_data)} viral posts to CSV...")

try:
    # Write viral posts to CSV
    handler.write_csv(
        file_path="viral_posts_export.csv",
        data=viral_data,
        overwrite=True
    )
    print("✓ Successfully saved viral posts to: viral_posts_export.csv")
except Exception as e:
    print(f"✗ Error saving file: {e}")

print()

# ============================================================================
# EXAMPLE 7: Reading CSV Data Back
# ============================================================================

print("EXAMPLE 7: Reading CSV Data Back")
print("-" * 70)

try:
    # Read the CSV file we just created
    read_data = handler.read_csv("viral_posts_export.csv")
    print(f"✓ Successfully read {len(read_data)} rows from CSV")
    
    if read_data:
        first_post = read_data[0]
        print(f"\nFirst post in CSV:")
        print(f"  Title: {first_post.get('title', 'N/A')}")
        print(f"  Creator: {first_post.get('creator', 'N/A')}")
        print(f"  Views: {first_post.get('views', 'N/A')}")
except Exception as e:
    print(f"✗ Error reading file: {e}")

print()
print()

# ============================================================================
# EXAMPLE 8: Validate CSV Data
# ============================================================================

print("EXAMPLE 8: Validate CSV Data")
print("-" * 70)

try:
    is_valid, errors = handler.validate_csv("viral_posts_export.csv")
    
    if is_valid:
        print("✓ CSV file is valid and well-formed!")
    else:
        print("✗ CSV file has validation errors:")
        for error in errors:
            print(f"  - {error}")
except Exception as e:
    print(f"✗ Error validating file: {e}")

print()
print()

# ============================================================================
# EXAMPLE 9: Working with Multiple Niches
# ============================================================================

print("EXAMPLE 9: Filter Posts by Niche")
print("-" * 70)

for niche in ["storytelling", "ai_automation", "nostalgia"]:
    niche_posts = [p for p in viral_posts if p['niche'] == niche]
    print(f"\n{niche.upper()}: {len(niche_posts)} viral posts")
    if niche_posts:
        print(f"  Example: {niche_posts[0]['title']}")

print()
print()

# ============================================================================
# EXAMPLE 10: Create a Custom Report
# ============================================================================

print("EXAMPLE 10: Create a Custom Report")
print("-" * 70)

report = {
    "report_date": "2025-12-11",
    "total_posts_analyzed": len(posts),
    "total_viral_posts": len(viral_posts),
    "total_trending_posts": len(trending_posts),
    "top_niche": max(niche_performance.items(), key=lambda x: x[1]['count'])[0],
    "top_creator": sorted_creators[0][0] if sorted_creators else "N/A",
    "niches_analyzed": len(niche_performance),
    "creators_analyzed": len(creator_performance)
}

print("\n📋 ANALYSIS REPORT")
print("-" * 70)
for key, value in report.items():
    print(f"{key}: {value}")

# Save report to CSV
report_list = [report]  # Convert to list for CSV handler
try:
    handler.write_csv("analysis_report.csv", report_list)
    print("\n✓ Report saved to: analysis_report.csv")
except Exception as e:
    print(f"\n✗ Error saving report: {e}")

print()
print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 70)
print("EXAMPLES COMPLETE!")
print("=" * 70)
print("""
You've now learned how to:
1. ✓ Create and run a ViralTrendAgent
2. ✓ Find viral and trending posts
3. ✓ Analyze performance by niche and creator
4. ✓ Get content strategy recommendations
5. ✓ Export results to CSV files
6. ✓ Create and use a CSVHandler
7. ✓ Read CSV files back into Python
8. ✓ Validate CSV data
9. ✓ Filter data by niche
10. ✓ Create custom reports

Next Steps:
- Modify the mock data to use your own social media data
- Create your own analysis functions
- Build custom reports for your specific needs
- Automate data collection and analysis

Happy analyzing! 🚀
""")
