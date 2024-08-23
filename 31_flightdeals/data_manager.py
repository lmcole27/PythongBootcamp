import json
#import requests

secret_data = json.load(open('secrets.json'))

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    # load secret data 
    def __init__(self):
      self.sheety_url = "https://api.sheety.co/013e8bcbef9a46a3bbf81351a8a3b34f/lindasFlightDeals/prices"
      self.sheety_header = secret_data["sheety_auth"]
      self.data = self.get_destination_data()
    #   self.iata_params= {"keyword": "",
    #                      "max": "1"}

    def get_destination_data(self):
    # TODO replaced temporarily with data file as sheety max reached
    #   sheety_data = requests.get(url=sheety_url, headers=sheety_header).json()
        sheety_data = json.load(open('sheety_data.json'))
        return sheety_data
        
    def update_destination_codes(self, id_no, iataCode):
    # Use sheety to save iataCode code back to sheet

    #TODO TEMPORARILY DISABLED DUE TO SHEETY MAX API CALLS REACHED  
        # put_param = {"price":{"iataCode": iataCode}}
        # response = requests.put(url=("https://api.sheety.co/013e8bcbef9a46a3bbf81351a8a3b34f/lindasFlightDeals/prices/" + str(id_no)), headers=self.sheety_header, json=put_param)
        # print(response.raise_for_status())

        sheety_data = json.load(open('sheety_data.json'))
        
        for row in sheety_data["prices"]:
            if row["id"] == id_no:
                row["iataCode"] = iataCode
                updated_data = json.dumps(sheety_data, indent=4)
        with open("sheety_data.json", "w") as outfile:
            outfile.write(updated_data) 

        return updated_data
