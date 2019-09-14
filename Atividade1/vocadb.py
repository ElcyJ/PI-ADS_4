import requests
import requests_cache

requests_cache.install_cache('cache')

headers = {
    'Content-Type': 'application/json'
}

params = {
    'fields': 'Names',
    'relations': 'LatestAlbums',
    'lang': 'English'
}

response = requests.get('https://vocadb.net/api/artists/1', headers=headers, params=params).json()
print(response['name'])