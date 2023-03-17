import requests
from bs4 import BeautifulSoup

# Define the URL of the YouTube channel to parse
url = "https://www.youtube.com/channel/UCBR8-60-B28hp2BmDPdntcQ"

# Send a GET request to the URL and store the response
response = requests.get(url)

# Parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the name of the YouTube channel
name_elem = soup.find('yt-formatted-string', class_='style-scope ytd-channel-name')
name = name_elem.text.strip() if name_elem else None
print('Channel Name:', name)

# Extract the description of the YouTube channel
description_elem = soup.find('yt-formatted-string', {'class': 'style-scope ytd-channel-about-metadata-renderer'})
description = description_elem.text.strip() if description_elem else None
print('Channel Description:', description)

# Extract the number of subscribers of the YouTube channel
subscribers_elem = soup.find('yt-formatted-string', {'class': 'style-scope ytd-c4-tabbed-header-renderer', 'id': 'subscriber-count'})
subscribers = subscribers_elem.text.strip() if subscribers_elem else None
print('Number of Subscribers:', subscribers)

# Extract the number of videos on the YouTube channel
videos_elem = soup.find_all('span', {'class': 'style-scope ytd-grid-video-renderer'})
videos = len(videos_elem)
print('Number of Videos:', videos)

# Extract the location of the YouTube channel
location_elem = soup.find('span', {'class': 'style-scope ytd-channel-about-metadata-renderer', 'itemprop': 'addressLocality'})
location = location_elem.text.strip() if location_elem else None
print('Location:', location)

# Extract the link to the YouTube channel's homepage
homepage_elem = soup.find('a', {'class': 'yt-simple-endpoint style-scope ytd-channel-about-metadata-renderer', 'href': lambda href: href and '/channel/' not in href})
homepage = homepage_elem['href'] if homepage_elem else None
print('Homepage:', homepage)
