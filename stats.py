import requests
from bs4 import BeautifulSoup
import sys
from dateutil import parser
import datetime

# link = sys.argv[1]
link = "https://github.com/MilitaryGuineaPig"
response = requests.get(link)
soup = BeautifulSoup(response.content, 'html.parser')

# work correctly
full_name_elem = soup.find('span', class_='p-name vcard-fullname d-block overflow-hidden')
full_name = full_name_elem.text.strip() if full_name_elem else None

git_nickname = link.split("/")[-1]

url = f'https://api.github.com/users/{git_nickname}'
response = requests.get(url)
user_data = response.json()
registration_date = parser.parse(user_data['created_at']).date()
registration = registration_date if registration_date else None


education_elem = soup.find('div', class_='mb-3 js-user-profile-bio f4')
education = education_elem.text.strip() if education_elem else None
# does not work
followers_elem = soup.find('a', {'href': f'/{git_nickname}?tab=followers'})
followers_text = followers_elem.find('span', {'class': 'text-bold'}).text.strip() if followers_elem else None
# work
current_date = datetime.datetime.now().strftime("%Y-%m-%d")



print('Full Name:', full_name)
print('GitHub Nickname:', git_nickname)
print('Education:', education)
print('Number of Followers:', followers_text)
print('Current Date:', current_date)
# Create a new text file and write the information to it
with open("user_info.txt", "w") as f:
    f.write(f"\t\t{full_name}'s dossier\n\n")
    f.write(f"Full Name: {full_name}\n")
    f.write(f"Git nickname: {git_nickname}\n")
    f.write(f"Education: {education}\n")
    f.write(f"\t\tBrief Information\n")
    f.write(f"GitHub was registered in {registration}, first contribution was pushed in august 2004. {full_name} has {followers_text} followers regarding to today’s date ({current_date}).\n")
    f.write(f"Current user is considered active. Detailed information is shown on graphs bellow:\n")
    f.write(f"\nGraph activity for last 3 month\n")
