import random
from datetime import datetime as dt
import requests
from flight_data import FlightData


TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "SJTtfKN8yUQyVP_CUD137Qx7jFXmJdM7"
TIME_NOW = dt.now()
TODAY = TIME_NOW.date()


class FlightSearch:

    def obtain_iata_codes(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code
    
    def search_for_cheap_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        location_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        

        response = requests.get(url=location_endpoint, headers=headers, params=query)
        
        try:
            results = response.json()['data'][0]

        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None


        flight_data = FlightData(
            price=results["price"],
            origin_city=results["route"][0]["cityFrom"],
            origin_airport=results["route"][0]["flyFrom"],
            destination_city=results["route"][0]["cityTo"],
            destination_airport=results["route"][0]["flyTo"],
            out_date=results["route"][0]["local_departure"].split("T")[0],
            return_date=results["route"][1]["local_departure"].split("T")[0]
            )
            
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data
    