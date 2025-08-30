import requests
import datetime
import cairosvg

USERNAME = "Elango-Kannan-00"   # <-- your GitHub username
TOKEN = None  # Optional: add a GitHub token for private repos (use secrets)

# GitHub GraphQL query for contributions
query = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
variables = {"login": USERNAME}

response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
data = response.json()

# Flatten contribution days
days = []
for week in data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
    days.extend(week["contributionDays"])

# Calculate current streak
streak = 0
today = datetime.date.today()
for d in reversed(days):
    date = datetime.date.fromisoformat(d["date"])
    if d["contributionCount"] > 0 and (today - date).days == streak:
        streak += 1
    else:
        if streak > 0:
            break

# Generate SVG of streak ring
svg = f"""
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="90" stroke="gray" stroke-width="15" fill="none" />
  <circle cx="100" cy="100" r="90" stroke="yellow" stroke-width="15" fill="none"
          stroke-dasharray="{streak*6}, 565" stroke-linecap="round"
          transform="rotate(-90 100 100)" />
  <text x="100" y="110" text-anchor="middle" font-size="36" fill="yellow">{streak}</text>
  <text x="100" y="150" text-anchor="middle" font-size="14" fill="white">Day Streak</text>
</svg>
"""

# Save SVG
with open("streak-ring.svg", "w") as f:
    f.write(svg)

print(f"✅ Generated streak ring with {streak} days")
