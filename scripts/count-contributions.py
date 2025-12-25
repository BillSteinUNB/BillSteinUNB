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
    
    # GraphQL query to get the contribution calendar total
    query = """
    query($username: String!, $from: DateTime, $to: DateTime) {
      user(login: $username) {
        createdAt
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """
    
    def get_contributions_for_range(start_date, end_date):
        variables = {
            "username": username,
            "from": start_date,
            "to": end_date
        }
        
        response = requests.post(
            "https://api.github.com/graphql",
            json={"query": query, "variables": variables},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print(f"GraphQL Errors: {data['errors']}")
                return None, 0
            
            user_data = data.get("data", {}).get("user", {})
            created_at = user_data.get("createdAt")
            
            # Use the calendar total which matches the profile graph exactly
            calendar = user_data.get("contributionsCollection", {}).get("contributionCalendar", {})
            total = calendar.get("totalContributions", 0)
            
            return created_at, total
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None, 0

    # 1. Get creation date and first year of contributions
    now = datetime.now()
    created_at_str, _ = get_contributions_for_range(
        (now - timedelta(days=1)).isoformat(), 
        now.isoformat()
    )
    
    if not created_at_str:
        print("Failed to fetch user creation date.")
        return 0

    created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
    total_all_time = 0
    
    # 2. Iterate through each year from creation until now
    current_year = created_at.year
    while current_year <= now.year:
        start_of_year = datetime(current_year, 1, 1)
        end_of_year = datetime(current_year, 12, 31, 23, 59, 59)
        
        # Adjust start/end for first and last years
        if current_year == created_at.year:
            start_of_year = created_at
        if current_year == now.year:
            end_of_year = now
            
        _, yearly_total = get_contributions_for_range(
            start_of_year.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end_of_year.strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        
        print(f"Year {current_year}: {yearly_total} contributions")
        total_all_time += yearly_total
        current_year += 1
        
    # Save to file for the update script
    with open("total_contributions.txt", "w") as f:
        f.write(str(total_all_time))
    
    print(f"Final total contributions (All Time): {total_all_time}")
    return total_all_time

if __name__ == "__main__":
    count_contributions()
