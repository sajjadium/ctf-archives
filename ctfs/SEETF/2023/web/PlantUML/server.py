import requests

BASE_URL = "http://plantuml:8080/"

url = input(f"URL: {BASE_URL}")
requests.get(f"{BASE_URL}{url}")
