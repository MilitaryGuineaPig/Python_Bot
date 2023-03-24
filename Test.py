import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.widgets import Slider

# Replace with your own GitHub username
username = "MilitaryGuineaPig"

# Get the contributions activity for the user using the GitHub API
url = f"https://api.github.com/users/{username}/events"
response = requests.get(url)
events = response.json()

# Create a dictionary to count the number of contributions for each day
contributions_by_day = {}
for event in events:
    if event["type"] == "PushEvent":
        date = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        if date >= datetime.now() - timedelta(days=365):
            if date in contributions_by_day:
                contributions_by_day[date] += event["payload"]["size"]
            else:
                contributions_by_day[date] = event["payload"]["size"]

# Create a list of dates and corresponding contributions counts
dates = []
contributions_counts = []
for date, count in sorted(contributions_by_day.items()):
    dates.append(date)
    contributions_counts.append(count)

# Create the bar chart of the contributions activity over the last year
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.3)
bar_plot = ax.bar(dates, contributions_counts, color="#1f77b4", alpha=0.7)
ax.set_xlabel("Date", fontsize=16)
ax.set_ylabel("Contributions", fontsize=16)
ax.set_title(f"Contributions Activity for {username} (Last Year)", fontsize=20, fontweight="bold")

# Define the slider widget and its properties
ax_slider = plt.axes([0.2, 0.15, 0.6, 0.03])
slider = Slider(ax_slider, "Date", 0, len(dates) - 1, valinit=len(dates) - 1)

# Define the update function for the slider
def update(val):
    index = int(slider.val)
    date = dates[index]
    for i, bar in enumerate(bar_plot):
        if i == index:
            bar.set_color("#ff7f0e")
            bar.set_alpha(1)
        else:
            bar.set_color("#1f77b4")
            bar.set_alpha(0.7)
    ax.set_title(f"Contributions Activity for {username} on {date.strftime('%Y-%m-%d')} (Last Year)", fontsize=20, fontweight="bold")
    plt.draw()

# Connect the slider to the update function
slider.on_changed(update)

# Set the background color of the plot
fig.patch.set_facecolor("#f5f5f5")

# Display the plot
plt.show()
