import re

linkedin_link = "https://www.linkedin.com/in/vladpallah/"

username_pattern = r"in\/([^\?\/]*)"

match = re.search(username_pattern, linkedin_link)

if match:
    username = match.group(1)
else:
    username = None

print(username)