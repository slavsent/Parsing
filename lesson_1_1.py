import requests
import os
from dotenv import load_dotenv

load_dotenv()

access_token_vk = os.getenv('ACCESS_TOKEN_VK')
params = {
    'user_id': '287192158',
    'v': '5.131',
    'extended': '1',
    'access_token': access_token_vk
}

url = 'https://api.vk.com/method/groups.get?'
req = requests.get(url=url, params=params)
print(req.json())
