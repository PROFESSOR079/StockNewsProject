from dotenv import load_dotenv
import os
import requests

load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

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
    print("Get News")

    news_parameters = {
        "q": COMPANY_NAME,
        "apikey": NEWS_API_KEY
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    first_three_news_data = news_data[:3]
    formatted_articles = [f"Headline: {item['title']}. \nBrief: {item['description']}" for item in first_three_news_data]










