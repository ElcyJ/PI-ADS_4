import requests
import requests_cache

requests_cache.install_cache('cache')

data = {
    "target_id": 2,
    "author_id": 3
}

response = requests.post('http://localhost:8000/flag_survivor/', data=data).json()
print(response)

