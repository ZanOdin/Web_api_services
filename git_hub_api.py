import requests
from pprint import pprint
import json

username = 'ZanOdin'
URL = f"https://api.github.com/users/{username}/repos"


response = requests.get(URL)
gh_data = response.json()

try:
        with open('gh_repos.json', 'w', encoding='utf-8') as f:
                json.dump(gh_data, f, ensure_ascii=False, indent=4)
        print("Successfully")
except:
        print("Failed")