import data_manager
import flight_search

lynns_destinations=data_manager.DataManager()
sheety_data =lynns_destinations.data
print(sheety_data)

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
        flight_info["destinationLocationCode"] = "LAX"
        
        # Update Data in Sheet
        print(lynns_destinations.update_destination_codes(id_no=flight_id, iataCode="LAX"))

    
