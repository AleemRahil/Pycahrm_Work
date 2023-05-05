import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = "P7FEEGDXXECOBSTM"
NEWS_API_KEY = "0f2b8a9f8b8f4b8c8e7c8d7c8e8f9d0"
TWILIO_SID = "AC7c7b8c8e8f9d0"
TWILIO_AUTH_TOKEN = "a0b1c2d3e4f5g6"


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_response = requests.get(
    url="https://www.alphavantage.co/query",
    params={
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": STOCK,
        "apikey": STOCK_API_KEY
        }
    )
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]

stock_data_list = [value for (key, value) in stock_data.items()]
yesterday_data = stock_data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
day_before_yesterday_data = stock_data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])
difference = (yesterday_closing_price - day_before_yesterday_closing_price) / day_before_yesterday_closing_price * 100
up_down = None
if difference > 5:
    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    up_down = "🔺"
    print("Get News")
    news_response = requests.get(
        url="https://newsapi.org/v2/everything",
        params={
            "qInTitle": COMPANY_NAME,
            "apiKey": NEWS_API_KEY
            }
        )
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    three_articles = news_data[:3]
    formatted_articles = [f"{STOCK}: {up_down}{round(difference * 100, 2)}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
elif difference <-5:
    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    up_down = "🔻"
    print("Get News")
    news_response = requests.get(
        url="https://newsapi.org/v2/everything",
        params={
            "qInTitle": COMPANY_NAME,
            "apiKey": NEWS_API_KEY
        }
    )
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    three_articles = news_data[:3]
    formatted_articles = [f"{STOCK}: {up_down}{round(difference * 100, 2)}%\nHeadline: {article['title']}. \nBrief: {article['description']}"for article in three_articles]
else:
    print(f"No News since the difference is {difference}%.\n")


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN, http_client=proxy_client)
message = client.messages \
        .create(
        body=f"{formatted_articles[0]} \n{formatted_articles[1]} \n{formatted_articles[0]}",
        from_='+12057362627',
        to='+12048135095'
        )
print(message.status)

#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

