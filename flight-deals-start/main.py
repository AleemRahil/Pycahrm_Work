#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_data import FlightData
from notification_manager import NotificationManager
from pprint import pprint


data_manager = DataManager()
sheet_data = data_manager.obtain_sheet_data()



if sheet_data[0]["iataCode"] == "":
    from flight_search import FlightSearch
    flight_search = FlightSearch()
    
    for row in sheet_data:
    
        row['iataCode'] = flight_search.obtain_iata_codes(row['city'])
    
    data_manager.your_sheet_data = sheet_data
    data_manager.edit_sheet_data()





