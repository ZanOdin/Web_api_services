import requests
from pprint import pprint
import json

API_KEY = '0e35ae86d28f097045670e4f78949d18'
LANG = 'ru-RU'
URL = 'https://api.themoviedb.org/3/movie/popular'

params = {
        'api_key': API_KEY,
        'language': LANG,
        'page': 1
        }

response = requests.get(URL, params=params)
tmdb_data = response.json().get('results')

try:
        with open('tmdb_popular.json', 'w', encoding='utf-8') as f:
                json.dump(tmdb_data, f, ensure_ascii=False, indent=4)
except:
        print("Failed")
# pprint(j_data)
for movie in tmdb_data:
        pprint(movie["original_title"])
# pprint(f"{j_data.get('results')}")



