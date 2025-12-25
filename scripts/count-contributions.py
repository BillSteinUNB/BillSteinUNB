# Count Total Contributions Script
import os
import requests
from datetime import datetime, timedelta
import json

def count_contributions():
    token = os.getenv("GITHUB_TOKEN")
    username = "BillSteinUNB"  # Your username
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v4.idl"
    }
    
    # GraphQL query to get comprehensive contribution data
    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          totalPullRequestReviewContributions
          totalRepositoryContributions
          commitContributionsByRepository {
            repository {
              nameWithOwner
            }
            contributions {
              totalCount
            }
          }
        }
      }
    }
    """
    
    # Get data from the last year
    from_date = (datetime.now() - timedelta(days=365)).isoformat()
    to_date = datetime.now().isoformat()
    
    variables = {
        "username": username,
        "from": from_date,
        "to": to_date
    }
    
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        user_data = data.get("data", {}).get("user", {})
        contributions = user_data.get("contributionsCollection", {})
        
        # Calculate comprehensive total
        total_contributions = (
            contributions.get("totalCommitContributions", 0) +
            contributions.get("totalPullRequestContributions", 0) +
            contributions.get("totalIssueContributions", 0) +
            contributions.get("totalPullRequestReviewContributions", 0) +
            contributions.get("totalRepositoryContributions", 0)
        )
        
        # Save to file for the update script
        with open("total_contributions.txt", "w") as f:
            f.write(str(total_contributions))
        
        print(f"Total contributions counted: {total_contributions}")
        return total_contributions
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return 0

if __name__ == "__main__":
    count_contributions()
