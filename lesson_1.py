import requests


url = 'https://api.github.com/users/slavsent/repos?callbaxk=abc'
req = requests.get(url)
print(req.json())
