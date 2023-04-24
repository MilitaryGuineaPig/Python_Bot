import requests
from datetime import datetime, timedelta

# User details
username = "MilitaryGuineaPig"

# GitHub API endpoint for retrieving user repositories
endpoint = f"https://api.github.com/users/{username}/repos"

# Make request to the GitHub API
response = requests.get(endpoint)

if response.status_code == 200:
    # Parse the response JSON
    repos = response.json()

    # Create a map to store the commit activity by week
    commit_activity = {}

    # Iterate through the repositories
    for repo in repos:
        # Get the name of the repository
        repo_name = repo["name"]

        # Get the GitHub API endpoint for retrieving commit activity for this repository
        repo_endpoint = f"https://api.github.com/repos/{username}/{repo_name}/stats/commit_activity"

        # Make request to the GitHub API for this repository
        repo_response = requests.get(repo_endpoint)

        if repo_response.status_code == 200:
            # Parse the response JSON
            repo_data = repo_response.json()

            # Iterate through the weekly commit activity data for this repository
            for weekly_commit_data in repo_data:
                # Calculate the start date of this week
                week_start_date = datetime.fromtimestamp(weekly_commit_data["week"])

                # Calculate the end date of this week
                week_end_date = week_start_date + timedelta(days=6)

                # Generate a key for this week
                week_key = f"{week_start_date.strftime('%Y-%m-%d')} to {week_end_date.strftime('%Y-%m-%d')}"

                # Get the number of commits for this week
                weekly_commit_count = weekly_commit_data["total"]

                # Add the weekly commit count to the commit activity map
                if week_key not in commit_activity:
                    commit_activity[week_key] = 0
                commit_activity[week_key] += weekly_commit_count
        else:
            print(f"Failed to retrieve commit activity for {username}/{repo_name}")

    # Output the commit activity map
    print("Week\tCommits")
    for week_key, commit_count in commit_activity.items():
        print(f"{week_key}\t{commit_count}")

    # Make a decision about the user's overall activity
    total_commits = sum(commit_activity.values())
    weeks_since_first_commit = (datetime.now() - datetime.fromtimestamp(repos[-1]["created_at"])).days / 7
    commits_per_week = total_commits / weeks_since_first_commit
    if commits_per_week >= 1:
        print("Active user")
    else:
        print("Inactive user")

else:
    print(response.status_code)
    print(f"Failed to retrieve repository information for {username}")
