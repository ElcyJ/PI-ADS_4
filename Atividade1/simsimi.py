import requests
import requests_cache

requests_cache.install_cache('cache')

headers = {
    'Content-Type': 'application/json',
    'x-api-key': '6bfti9994RIk7NqhRSlDAF8ZcACSPTvwqges5DBw',
}

data = '{"utext": "how are you?", "lang": "en"}'

response = requests.post('https://wsapi.simsimi.com/190410/talk', headers=headers, data=data).json()
print(response['atext'])