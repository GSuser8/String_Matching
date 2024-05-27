import requests
url = 'http://localhost:5000/search'
data = {'query': 'sample', 'text': 'This is a different sample text for demonstration purposes. Sample is repeated twice.'}
response = requests.post(url, json=data)
print(response.json())