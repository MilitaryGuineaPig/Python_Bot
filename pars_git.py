import requests
from bs4 import BeautifulSoup
import sys

# Define the URL of the GitHub page to parse
link = sys.argv[1]
# Send a GET request to the URL and store the response
response = requests.get(link)
# Parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the name of the GitHub user or organization
name_elem = soup.find('span', class_='p-name vcard-fullname d-block overflow-hidden')
name = name_elem.text.strip() if name_elem else None
print('Name:', name)

# Extract the bio of the GitHub user or organization
bio_elem = soup.find('div', class_='p-note user-profile-bio mb-3 js-user-profile-bio f4')
bio = bio_elem.text.strip() if bio_elem else None
print('Bio:', bio)

# Find the element that contains the number of followers and extract the text
followers_elem = soup.find('a', {'href': '/openai?tab=followers'})
followers_text = followers_elem.find('span', {'class': 'text-bold'}).text.strip() if followers_elem else None
print('Number of followers:', followers_text)

# Extract the number of repositories
num_repos_elem = soup.find('span', class_='Counter')
num_repos = num_repos_elem.text.strip() if num_repos_elem else None
print('Number of repositories:', num_repos)

# Extract the location of the GitHub user or organization
location_elem = soup.find('span', class_='p-label')
location = location_elem.text.strip() if location_elem else None
print('Location:', location)

# Extract the LinkedIn link of the GitHub user or organization
linkedin_elem = soup.find('a', href=lambda href: href and 'linkedin' in href)
linkedin = linkedin_elem['href'] if linkedin_elem else None
print('LinkedIn:', linkedin)
