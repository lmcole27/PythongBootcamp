import requests
import json

secret_data = json.load(open('secrets.json'))
amadeaus_oath_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
key_header = {"Content-Type": "application/x-www-form-urlencoded"}
amadeaus_login_data = secret_data["amadeaus_auth"]
oath_response = requests.post(url=amadeaus_oath_url, headers=key_header, data=amadeaus_login_data)
access_token = oath_response.json()["access_token"]
token = {"Authorization": "Bearer " + access_token }
print(token)
    

flight_params =  {
                 "originLocationCode": "NYC",
                 "destinationLocationCode": "LAX",
                 "maxPrice": 400,
                 "adults": "1",
                 "departureDate": "2024-09-06",
                 "max": "10"
                 }   
bestFlight = {'itineraries': ''}

flights=requests.get(url="https://test.api.amadeus.com/v2/shopping/flight-offers", headers=token, params=flight_params).json()

print(flights)