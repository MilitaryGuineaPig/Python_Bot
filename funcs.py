import datetime
import requests
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def get_all_commits_by_user(username):
    # Get the list of repositories for the user
    url = f"https://api.github.com/users/{username}/repos"
    repos = requests.get(url).json()

    # Initialize a list to store the commits by week
    commits_by_week = [0] * 53
    # Iterate through the repositories
    for repo in repos:
        # Get the name of the repository
        repo_name = repo["name"]
        # Get the list of commits for the repository
        url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
        commits = requests.get(url).json()

        # Iterate through the commits
        for commit in commits:
            # Get the commit date and week number
            commit_date = datetime.datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
            week_number = int(commit_date.strftime("%U"))

            # Increment the commit count for the week
            commits_by_week[week_number] += 1

    # Set up the plot
    fig, ax = plt.subplots(figsize=(18, 8))

    # Add a background image
    bg_image = Image.open("Old_Docs/s.jpeg")
    ax.imshow(bg_image, extent=[0, 54, 0, max(commits_by_week)], aspect="auto", alpha=0.5)
    # Add the bar chart of commit counts by week
    ax.bar(range(1, 53), commits_by_week[1:], color='red', alpha=0.5, width=0.5, edgecolor="white", linewidth=0.5)
    # Set the x-axis labels to the week numbers and rotate them 45 degrees
    ax.set_xticks(range(1, 53))
    ax.set_xticklabels(range(1, 53), rotation=45, fontsize=14)

    # Add a title and axis labels
    ax.set_title("Commits by week in this year", fontsize=25)
    ax.set_xlabel("Week", fontsize=25)
    ax.set_ylabel("Number of commits", fontsize=25)

    # Save the plot
    plt.savefig(f"Users_docs/Im_Stat_{username}.png", dpi=300, bbox_inches="tight")
