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
    with open("README.md", "r") as f:
        content = f.read()
    
    # Pattern to find and replace the total contributions line
    pattern = r'Total Contributions \(All Time\): \d+'
    replacement = f'Total Contributions (All Time): {total_contributions}'
    
    # Update if pattern exists, otherwise add it
    if re.search(pattern, content):
        updated_content = re.sub(pattern, replacement, content)
        print(f"Updated existing total to {total_contributions}")
    else:
        # Add the section after the header
        header_pattern = r'---\n\n## About Me'
        replacement_section = f'---\n\n## 📊 GitHub Activity\n\n- **Total Contributions (All Time):** {total_contributions}\n\n## About Me'
        updated_content = re.sub(header_pattern, replacement_section, content)
        print(f"Added new section with {total_contributions} contributions")
    
    # Write back
    with open("README.md", "w") as f:
        f.write(updated_content)
    
    print(f"README updated successfully")

if __name__ == "__main__":
    update_readme()
