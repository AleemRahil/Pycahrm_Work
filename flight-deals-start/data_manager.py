import os
import random
import requests
from pprint import pprint

SHEETY_ENDPOINT = "https://api.sheety.co/50c19efe6fd03071a2c8f395e166d0b4/flightDeals/prices"
SHEETY_BEARER = {
            "Authorization": "Bearer " + "43785hfdsf74t5bfnd7845t4ui487r5"
        }

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.your_sheet_data = {}
        
    
    def obtain_sheet_data(self):
        sheety_response = requests.get(url=SHEETY_ENDPOINT, headers=SHEETY_BEARER)
        sheet_data = sheety_response.json()                
        self.your_sheet_data = sheet_data["prices"]
        return self.your_sheet_data
        
        
    def edit_sheet_data(self):        
        for row in self.your_sheet_data:            
            sheet_input = {                    
                    'price' : {
                        'iataCode' : row['iataCode']
                    }
                  
                }
            
            edit_sheety_response = requests.put(url=f"{SHEETY_ENDPOINT}/{row['id']}",
                                                     json=sheet_input,
                                                     headers=SHEETY_BEARER)
            print(edit_sheety_response.text)
        
        # self.updated_sheet_data = self.edit_sheety_response.json()["prices"]
        # return self.updated_sheet_data

