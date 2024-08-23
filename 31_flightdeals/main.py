#import requests
#import json
#import datetime as dt
import flight_search
import data_manager

#from twilio.rest import Client
#print(dt.date.today())

# Load destination data
lynns_destinations=data_manager.DataManager()
sheety_data =lynns_destinations.data
print(sheety_data)

#TODO search for flights by caLLing a function from the flight search class 

iata_params= {"keyword": "",
              "max": "1"}

for row in sheety_data["prices"]:

    flight_id = row['id']
    flight_info = {
                 "originLocationCode": "NYC",
                 "destinationLocationCode": row['iataCode'],
                 "maxPrice": row["lowestPrice"],
                 "adults": "1",
                 "departureDate": "2024-09-06",
                 "max": "10"
                 }   
    
    flight = flight_search.FlightSearch(flight_params=flight_info)
    
    if row["iataCode"] == "":
        iata_params["keyword"] = row["city"]
        flight.flight_params["destinationLocationCode"] = flight.get_iata_code(iata_params=iata_params)
        
        # Update Data in Sheet
        lynns_destinations.update_destination_codes(id_no=flight_id, iataCode=flight.flight_params["destinationLocationCode"])

    #Search for best priced flight
    flight.search_bestFlight()


# #Populate flight_params from each row in sheety. Repeat the search for each row in sheety.
# for row in sheety_data["prices"]:
#     flight_info = {
#                  "originLocationCode": "NYC",
#                  "destinationLocationCode": row['iataCode'],
#                  "maxPrice": row["lowestPrice"],
#                  "adults": "1",
#                  "departureDate": "2024-09-06",
#                  "max": "10"
#                  }    
#     flight = flight_search.FlightSearch(flight_params=flight_info)

#     flight.search_bestFlight()
    


print("Complete")
