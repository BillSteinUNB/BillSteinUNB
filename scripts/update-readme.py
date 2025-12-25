# Update README with Total Contributions, Timestamp, and Cache Busting
import re
from datetime import datetime
import time

def update_readme():
    # Read the current total
    try:
        with open("total_contributions.txt", "r") as f:
            total_contributions = int(f.read().strip())
    except:
        print("Could not read total_contributions.txt")
        return
    
    # Read README
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Generate cache buster (Unix timestamp)
    cache_buster = int(time.time())
    
    # Generate human-readable timestamp
    timestamp = datetime.utcnow().strftime("%B %d, %Y at %I:%M %p UTC")
    
    # 1. Update total contributions
    pattern = r'(\*\*Total Contributions \(All Time\):\*\*) \d+'
    replacement = rf'\1 {total_contributions}'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print(f"Updated contributions to {total_contributions}")
    else:
        print(f"Warning: Could not find contributions line.")
        return
    
    # 2. Update "Last Updated" timestamp
    timestamp_pattern = r'<!-- last_updated starts -->.*?<!-- last_updated ends -->'
    timestamp_replacement = f'<!-- last_updated starts -->\n*Last Updated: {timestamp}*\n<!-- last_updated ends -->'
    content = re.sub(timestamp_pattern, timestamp_replacement, content, flags=re.DOTALL)
    print(f"Updated timestamp to {timestamp}")
    
    # 3. Update cache busters on image URLs
    # Match Vercel stats URLs and update/add cache parameter
    def add_cache_buster(match):
        url = match.group(0)
        # Remove old cache parameter if exists
        url = re.sub(r'&?cache=\d+', '', url)
        # Add new cache parameter
        if '?' in url:
            return f'{url}&cache={cache_buster}'
        else:
            return f'{url}?cache={cache_buster}'
    
    # Update Vercel URLs (github-readme-stats)
    content = re.sub(
        r'https://github-readme-stats-three-silk-96\.vercel\.app/api[^")\s]+',
        add_cache_buster,
        content
    )
    
    # Update Streak Stats URLs
    content = re.sub(
        r'https://github-readme-streak-stats\.herokuapp\.com/[^")\s]+',
        add_cache_buster,
        content
    )
    
    print(f"Added cache buster: {cache_buster}")
    
    # Write back
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"README updated successfully")

if __name__ == "__main__":
    update_readme()
