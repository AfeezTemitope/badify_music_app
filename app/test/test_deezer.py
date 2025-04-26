import requests

try:
    response = requests.get('https://api.deezer.com/search?q=wizkid')
    response.raise_for_status()
    print(response.json())
except requests.RequestException as e:
    print(f"Error: {e}")