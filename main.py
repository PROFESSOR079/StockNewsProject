from dotenv import load_dotenv
import os
import requests
from twilio.rest import Client

load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

TWILIO_ACC_SID = os.environ.get("TWILIO_SID", "")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE = os.environ.get("TWILIO_PHONE", "")
MY_PHONE = os.environ.get("MY_PHONE", "")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")


stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
data = stock_response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_stock_price = float(yesterday_data["4. close"])

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_stock_price = float(day_before_yesterday_data["4. close"])

difference = abs(yesterday_closing_stock_price - day_before_yesterday_closing_stock_price)
diff_percent = (difference / day_before_yesterday_closing_stock_price) * 100

if diff_percent > 5:
    news_parameters = {
        "q": COMPANY_NAME,
        "apikey": NEWS_API_KEY
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    first_three_news_data = news_data[:3]

    up_down = ""
    if yesterday_closing_stock_price > day_before_yesterday_closing_stock_price:
        up_down = "🔺"
    else:
        up_down = "🔻"

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {item['title']}. \nBrief: {item['description']}" for item in first_three_news_data]

    client = Client(TWILIO_ACC_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        print(f"Sending: {article}")
        message = client.messages.create(
            to=MY_PHONE,
            from_=TWILIO_PHONE,
            body=article
        )
    print("Message sent successfully!!!!!!!!")






