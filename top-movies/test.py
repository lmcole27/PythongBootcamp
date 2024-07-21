import requests
import json

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzOGIwMGIxM2UyZWU5ODViNThlMzAxNTMwYTdiZTg4MyIsInN1YiI6IjY0ZGMxYjZhZjQ5NWVlMDI5MjUxMjJjNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.sG_C7QcHr2XTEvNqjDewkwW14aB8CbChPd5EJk8eUKg"
}


movie_title = "Dirty Dancing"
url = "https://api.themoviedb.org/3/search/movie"
API_KEY = "38b00b13e2ee985b58e301530a7be883"
#response = requests.get(url_string, headers=headers).text   
response = requests.get(url, params={"api_key": API_KEY, "query": movie_title})
data = response.json()["results"]


for movie in data:
    print(movie["id"], movie["title"], movie["release_date"])
#print(response.json()["page"])
#print(response.title)