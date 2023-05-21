# Single Page App for comparing stocks using Vue.js and Flask

This simple app illustrates how to retrieve stock data (JSON format) from a backend server, and then show the graph and statistics data at frontend site. 


## Backend (Python 3)

* Flask is used as the backend framework.  
* [yfinance](https://github.com/ranaroussi/yfinance) is used for downloading daily stock prices.  
* Currently, only 3 stocks are supported: GOOG, AAPL, MSFT. However, it's easy to add more stocks by appending stock codes to **stock_names** in **app.py**.  
* Backend has a dedicated thread for downloading stock data (current interval: 4 hours).
* For simplicity, database is NOT used. Each time you restart the server, it will download the stock data again and store them in the memory.

### ULR entries
* /: only for test purpose, return a message "Hello World! :)".
* /stock/<start_date>: start_date has the format YYYY-MM-DD.  
  It returns a list of stock objects with fields: name (string), dates (list of string), prices (list of float), cumulative_return (float), annualized_return (float), annualized_volatility (float)

#### Formulas for stock statistics
* [cumulative_return](https://www.investopedia.com/terms/c/cumulativereturn.asp) = end_price / start_price - 1.0
* [annualized_return](https://www.investopedia.com/terms/a/annual-return.asp) = (end_price / start_price) ^ (1 / years_from_start_date) - 1.0
* [annualized_volatility](https://www.fool.com/knowledge-center/how-to-calculate-annualized-volatility.aspx) = standard_deviation(price_1/price_0 - 1.0, price_2/price_1 - 1.0, price_3/price_2 - 1.0, ...) * sqrt(250)

### Installation guide

1. Install dependencies (better to run in a new virtual env)
```sh
cd backend
pip install -r requirements.txt
```

2. Try
```sh
python app.py
curl http://localhost:11280/stock/2023-05-01
```




## Frontend (Vue 3)

* Vue is used as the frontend framework.
* Each time user select a new start date and click "Reload", it will talk with the backend to get latest data. (Yes, as you noticed, we can improve the performance by client cache).
* [canvasJS](https://canvasjs.com/) is used for drawing the graph.


## Installation guide

1. Install dependencies
```sh
cd frontend
npm install
```

2. Try (make sure the backend server is running)
```sh
npm run dev -- --host 0.0.0.0
```
Now use your browser to access http://localhost:12801/


