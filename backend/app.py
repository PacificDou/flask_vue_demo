from flask import Flask
from flask_cors import CORS
import yfinance
import pandas as pd
import math
import threading
import time

app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

stock_names = ["GOOG", "AAPL", "MSFT"]
stock_prices = {}
DAYS_ONE_YEAR = 250
DAYS_ONE_YEAR_SQRT = math.sqrt(DAYS_ONE_YEAR)
PRICE_CHECK_INTERNAL = 3600 * 4 # four hours

def download_latest_prices():
    global stock_names, stock_prices, PRICE_CHECK_INTERNAL

    while True:
        time.sleep(PRICE_CHECK_INTERNAL)
        for name in stock_names:
            print("Download latest data for stock {}...".format(name), end="", flush=True)
            lastDate = stock_prices[name].index[-1]
            df = yfinance.download(name, start=lastDate.strftime("%Y-%m-%d"))
            print("DONE! :)", flush=True)

            if df.index[-1] > lastDate:
                print(stock_prices[name].index[-100:])
                stock_prices[name] = pd.concat([stock_prices[name], df[df.index > lastDate]])
                print("stock {0}: new data added {1}".format(name, len(df[df.index > lastDate])))
                print(stock_prices[name].index[-100:])


@app.route("/", methods=["GET", "POST"])
def hello_world():
    return "Hello World! :)"

@app.route("/stock/<string:start>", methods=["GET"])
def get_stock(start):
    start = pd.to_datetime(start, format="%Y-%m-%d")
    ret = []

    global stock_prices, DAYS_ONE_YEAR, DAYS_ONE_YEAR_SQRT

    for name, df in stock_prices.items():
        df = df[(df.index >= start)].reset_index(drop=False)
        if len(df) == 0:
            continue
        prices = df["Close"].tolist()
        dates = [d.strftime("%Y-%m-%d") for d in df["Date"].tolist()]

        # compute statistics
        cumulative_return = prices[-1] / prices[0] - 1.0
        annualized_return = pow(cumulative_return + 1.0, DAYS_ONE_YEAR / len(prices)) - 1.0
        annualized_volatility = DAYS_ONE_YEAR_SQRT * (pd.Series(prices[1:]) - pd.Series(prices[:-1])).std() if len(prices) > 1 else 0.0

        ret.append({"name": name, "dates": dates, "prices": prices, "cumulative_return": cumulative_return, \
                    "annualized_return": annualized_return, "annualized_volatility": annualized_volatility})

    return ret

if __name__ == "__main__":

    # download stock prices
    print("Downloading stock prices...", flush=True)
    for name in stock_names:
        stock_prices[name] = yfinance.download(name, start="2010-01-01", end=None)
    print("DONE! :)", flush=True)

    # init thread for downloading new prices
    print("Init thread for downloading newest prices...", end="", flush=True)
    t1 = threading.Thread(target=download_latest_prices, args=())
    t1.start()
    print("DONE! :)", flush=True)

    app.run(host='0.0.0.0', port=11280, debug=False)

