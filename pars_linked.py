import requests
import sys
from bs4 import BeautifulSoup

url = sys.argv[1]
# Set headers to mimic a real user request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Send a GET request to the URL and store the response
response = requests.get(url, headers=headers)

# Parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the name of the LinkedIn user
name_elem = soup.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words')
name = name_elem.text.strip() if name_elem else None
print('Name:', name)

# Extract the headline of the LinkedIn user
headline_elem = soup.find('h2', class_='mt1 t-18 t-black t-normal break-words')
headline = headline_elem.text.strip() if headline_elem else None
print('Headline:', headline)

# Extract the location of the LinkedIn user
location_elem = soup.find('li', class_='t-16 t-black t-normal inline-block')
location = location_elem.text.strip() if location_elem else None
print('Location:', location)

# Extract the current job title of the LinkedIn user
job_elem = soup.find('h2', class_='mt1 t-18 t-black t-normal')
job_title = job_elem.text.strip() if job_elem else None
print('Job title:', job_title)

# Extract the current employer of the LinkedIn user
employer_elem = soup.find('span', class_='text-body-medium break-words')
employer = employer_elem.text.strip() if employer_elem else None
print('Employer:', employer)

# Extract the education of the LinkedIn user
education_elem = soup.find('section', {'id': 'education-section'})
education = education_elem.text.strip() if education_elem else None
print('Education:', education)

# Extract the skills of the LinkedIn user
skills_elem = soup.find('section', {'id': 'skills-section'})
skills = [skill.text.strip() for skill in skills_elem.find_all('span', {'class': 'pv-skill-category-entity__name-text'})] if skills_elem else None
print('Skills:', skills)
