#import requests
import json
#import datetime as dt
import flight_search
import data_manager

#from twilio.rest import Client
#print(dt.date.today())

# load secret data 
secret_data = json.load(open('secrets.json'))
sheety_url = "https://api.sheety.co/013e8bcbef9a46a3bbf81351a8a3b34f/lindasFlightDeals/prices"
sheety_header = secret_data["sheety_auth"]

# TODO replaced temporarily with data file as sheety max reached
# # load google sheet data using sheety

# def loadSheet():
# #   sheety_data = requests.get(url=sheety_url, headers=sheety_header).json()
#     sheety_data = json.load(open('sheety_data.json'))
#     return sheety_data

# sheety_data = loadSheet()
x=data_manager.DataManager()
sheety_data = data_manager.DataManager.get_destination_data(self=x)
print(sheety_data)

#TODO MAKE THIS INTO A CLASS? 
#TODO TEMPORARILY DISABLED DUE TO SHEETY MAX API CALLS REACHED

# # for row in google sheet retrieve city, find city airport code (iataCode) and save back to sheet using sheety 
# amadeaus_iata_url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
# iata_params= {"keyword": "",
#          "max": "1"}

# for row in sheety_data["prices"]:
#     if row["iataCode"] == "":
#         iata_params["keyword"]= row["city"]

#         # Use amadeaus to find iataCode
#         response = requests.get(url=amadeaus_iata_url, headers=token_header, params=iata_params).json()
#         iataCode = response["data"][0]["iataCode"]
        
#         # Use sheety to save iataCode code back to sheet
#         id_no = row["id"]
#         put_param = {"price":{
#             "iataCode": iataCode
#             }
#         }
#         response = requests.put(url=("https://api.sheety.co/013e8bcbef9a46a3bbf81351a8a3b34f/lindasFlightDeals/prices/" + str(id_no)), headers=sheety_header, json=put_param)
#         #print(response.raise_for_status())
#         #print(row["city"], iataCode)
#         #print(row)


#TODO search for flights by caLLing a function from the flight search class 

# Reload sheet with iataCodes complete
#sheety_data = loadSheet()
print(sheety_data['prices'])

#Populate flight_params from each row in sheety. Repeat the search for each row in sheety.
for row in sheety_data["prices"]:
    flight_info = {
                 "originLocationCode": "NYC",
                 "destinationLocationCode": row['iataCode'],
                 "maxPrice": row["lowestPrice"],
                 "adults": "1",
                 "departureDate": "2024-09-06",
                 "max": "10"
                 }    
    flight = flight_search.FlightSearch(flight_params=flight_info)

    flight.search_bestFlight()
    


print("Complete")
