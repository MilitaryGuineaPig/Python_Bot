import requests
from bs4 import BeautifulSoup
import sys
import datetime

# link = sys.argv[1]
link = "https://www.linkedin.com/in/vladpallah/"
response = requests.get(link)
soup = BeautifulSoup(response.content, 'html.parser')

full_name_elem = soup.find('span', class_='p-name vcard-fullname d-block overflow-hidden')
full_name = full_name_elem.text.strip() if full_name_elem else None

git_nickname = link.split("/")[-1]

url = f'https://api.github.com/users/{git_nickname}'
response = requests.get(url)
user_data = response.json()
registration_date = user_data['created_at']
registration_date = registration_date.text.strip() if registration_date else None


education_elem = soup.find('div', class_='mb-3 js-user-profile-bio f4')
education = education_elem.text.strip() if education_elem else None

followers_elem = soup.find('a', {'href': f'/{git_nickname}?tab=followers'})
followers_text = followers_elem.find('span', {'class': 'text-bold'}).text.strip() if followers_elem else None

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

cv_elem = soup.find('a', href=lambda href: href and 'resume' in href)
cv_link = cv_elem['href'] if cv_elem else None

print('Full Name:', full_name)
print('GitHub Nickname:', git_nickname)
print('Education:', education)
print('Number of Followers:', followers_text)
print('Current Date:', current_date)
print('CV Link:', cv_link)
# Create a new text file and write the information to it
with open("user_info.txt", "w") as f:
    f.write(f"{full_name}'s dossier\n\n")
    f.write(f"Full Name: {full_name}\n")
    f.write(f"Git nickname: {git_nickname}\n")
    f.write(f"Education: {education}\n")
    f.write(f"Brief Information: \n")
    f.write(f"GitHub was registered in {registration_date}, first contribution was pushed in august 2004. {full_name} has {followers_text} followers regarding to today’s date ({current_date}).\n")
    f.write(f"Current user is considered active. Detailed information is shown on graphs bellow:\n")
    f.write(f"\nGraph activity for last 3 month\n")
    f.write(f"\nCV: {cv_link}")