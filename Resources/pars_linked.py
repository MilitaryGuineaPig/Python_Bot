from linkedin_api import Linkedin
import sys

# Authenticate using any Linkedin account credentials
api = Linkedin('vladosrevolucioner@gmail.com', '12345678Test!')

url = sys.argv[1]
parts = url.split("/")
username = parts[-2]

# GET a profile
profile = api.get_profile(username)
print(username)
# GET a profiles contact info
contact_info = api.get_profile_contact_info(username)
# GET all connected profiles (1st, 2nd and 3rd degree) of a given profile
connections = api.get_profile_connections('1234asc12304')

with open("Users_docs/user_info.txt", "w") as f:
    f.write(f"\t\t{profile['firstName']}'s dossier\n\n")
    f.write(f"Full Name: {profile['firstName']} {profile['lastName']}\n")
    f.write(f"Type of employment: {profile['headline']} \n")
    f.write(f"\t\tSkills:\n")
    counter = 0
    for edu in profile['skills']:
        if 'name' in edu:
            counter = counter + 1
            school_name = edu['name']
            f.write(f" {counter}) {school_name} \n")
        else:
            print("No school information available")
    counter = 0
    f.write(f"\t\tEducation:\n")
    for edu in profile['education']:
        if 'school' in edu:
            counter = counter + 1
            school_name = edu['school']['schoolName']
            f.write(f"#{counter}: {school_name} \n")
        else:
            print("No school information available")
    f.write(f"Location: {profile['locationName']} {profile['geoLocationName']}\n")
    f.write(f"\t\tBrief Information\n")
    f.write(f"{profile['summary']} \n")


    #f.write(f"GitHub was registered in {registration}, first contribution was pushed in august 2004. {full_name} has {followers_text} followers regarding to today’s date ({current_date}).\n")
    #f.write(f"Current user is considered active. Detailed information is shown on graphs bellow:\n")
    #f.write(f"\nGraph activity for last 3 month\n")

