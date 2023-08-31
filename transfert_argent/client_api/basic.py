import requests

endpoint = "http://127.0.0.1:8000/api/api_viewutilisateurs/"
response = requests.get(endpoint, params={'abc':1234} json={'query':'hello'})
print(response.json())
print(response.status_code)