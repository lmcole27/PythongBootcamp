import json
import requests

# load secret data 
secret_data = json.load(open('secrets.json'))

# Create a dictionary of flight_dst: flight_instance
# OR Save best flight back to sheety? What you need? 

class FlightSearch:
  def __init__(self, flight_params):
    self.amadeaus_oath_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    self.key_header = {"Content-Type": "application/x-www-form-urlencoded"}
    self.amadeaus_login_data = secret_data["amadeaus_auth"]
    self.token = self.get_token()
    
    self.amadeaus_iata_url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
    self.flight_params = flight_params
    self.bestFlight = {'itineraries': ''}

  def get_token(self):
    # get Oauth token
    oath_response = requests.post(url=self.amadeaus_oath_url, headers=self.key_header, data=self.amadeaus_login_data)
    access_token = oath_response.json()["access_token"]
    return {"Authorization": "Bearer " + access_token }

  def get_iata_code(self, iata_params):
     # Use amadeaus to find iataCode
    response = requests.get(url=self.amadeaus_iata_url, headers=self.token, params=iata_params).json()
    return print(response)
    #iataCode = response["data"][0]["iataCode"]
    #return iataCode

  def search_bestFlight(self):
    flights=requests.get(url="https://test.api.amadeus.com/v2/shopping/flight-offers", headers=self.token, params=self.flight_params).json()
    # bestPrice = float(self.flight_params["maxPrice"])
    return print(flights)
    # for flight in flights["data"]:
    #     if float(flight["price"]["total"]) < bestPrice:
    #         bestPrice = float(flight["price"]["total"])
    #         self.bestFlight = flight
    # if bestPrice < float(self.flight_params["maxPrice"]):
    #     return f"The lowest fare to {self.flight_params['destinationLocationCode']} is {flight['price']['total']} {flight['price']['currency']}.The best flight is {self.bestFlight['itineraries'][0]['segments']}"
    # else:
    #     return f"No flight to {self.flight_params['destinationLocationCode']} that meets your criteria is available."


