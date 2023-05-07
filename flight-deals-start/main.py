#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager

from notification_manager import NotificationManager
from pprint import pprint
from flight_search import FlightSearch
from datetime import datetime as dt, timedelta as td

data_manager = DataManager()
sheet_data = data_manager.obtain_sheet_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA='YTO'

tomorrow = dt.now() + td(days=1)
six_month_from_today = dt.now() + td(days=(6 * 30))

if sheet_data[0]["iataCode"] == "":
        
    for row in sheet_data:
    
        row['iataCode'] = flight_search.obtain_iata_codes(row['city'])
    
    data_manager.your_sheet_data = sheet_data
    data_manager.edit_sheet_data()
else:
    pass

for destination in sheet_data:
    flight = flight_search.search_for_cheap_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    
    if sheet_data[0]["lowestPrice"] > flight.price:
        notification_manager.send_sms(
            message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        )