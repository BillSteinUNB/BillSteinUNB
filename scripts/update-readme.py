# Update README with Total Contributions
import re

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
    
    # Pattern to find and replace the total contributions number
    # This matches the exact line format: "- **Total Contributions (All Time):** <number>"
    pattern = r'(\*\*Total Contributions \(All Time\):\*\*) \d+'
    replacement = rf'\1 {total_contributions}'
    
    if re.search(pattern, content):
        updated_content = re.sub(pattern, replacement, content)
        print(f"Updated existing total to {total_contributions}")
    else:
        # Section doesn't exist - this shouldn't happen with our clean README
        # but as a fallback, add it after the title
        print(f"Warning: Could not find contributions line. Please check README format.")
        return
    
    # Write back
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print(f"README updated successfully")

if __name__ == "__main__":
    update_readme()
