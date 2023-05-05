import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

open_weather_api_key = "69f04e4613056b159c2761a9d9e664d2"
account_sid = "AC7c357bb2c70d78979800071781270f39"
auth_token = "0549b71f9a1e07f77368c2e0bac53485"

client = Client(account_sid, auth_token)#, http_client=proxy_client)

response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params={"lat": 43.656980, "lon": -79.384230, "appid": open_weather_api_key, "exclude": "current, minutely daily"})
response.raise_for_status()
weather_data = response.json()

will_rain = False
weather_slice = weather_data["hourly"][:12]
for hour_data in weather_slice:
    condition_code = int(hour_data["weather"][0]["id"])

    if condition_code < 700:
        will_rain = True

if will_rain:
    # proxy_client = TwilioHttpClient()
    # proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    # client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔︰",
        from_='+12057362627',
        to='+12048135095'
        )
    print(message.status)

