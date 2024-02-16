import requests
from bs4 import BeautifulSoup

url = "https://getbootstrap.com/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the desired information from the parsed HTML
    title = soup.find('h1', class_='mb-3 fw-semibold lh-1').text.strip()
    print("Title:", title)
else:
    print("Failed to fetch the page:", response.status_code)
