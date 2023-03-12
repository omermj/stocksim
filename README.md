# StockSim
StockSim is a web based stock trading simulator, which enables users to create virtual stock trading accounts and trade the US Equity markets with virtual money. Users can test their trading skills and strategies on live markets and keep a record of their trading performance.

## Technologies Used
- Frontend: Javascript, JQuery, AJAX, Bootstrap CSS
- Backend: Python (Flask), SQLAlchemy, PostgreSQL, WTForms, Bcrypt, Jinja2
- Deployment: Heroku


## Stock Quotes API
The API used to get real-time stock quotes is Alpaca Data API - https://alpaca.markets/data


## How it works
Users create their personal trading profile by signing up. Every user starts with $50,000 in virtual funds. Virtual deposits and withdrawals can be made to adjust the account balance after signing up.

Once registered, users can enter trades in any list US stock by using the stock symbol. The most recent price of the stock will be used to determine the purchase price. Subsequently, the trade can be closed at the current market price as well.

StockSim allows users to enter both Buy (Long) and Sell (Short) positions. In a short position, the user profits when the stock price falls.

The app tracks the profitability of all user trades with latest stock prices at individual trade level as well as aggregate account level. This enables the user to quickly view the total gain and loss on the overall portfolio.

The user can also create multiple stock watchlists. Each watchlist can contain multiple stocks, which the user can track and trade.


## User Flow and Main Features

- Home page gives the user option to either login with an existing account or signup
  
  ![Home Page](/screenshots/main.png)

- Signup form asks for basic user details

  ![Signup](/screenshots/signup.png)

- After signup/login, user can view the dashboard
  
  ![Dashboard](/screenshots/dashboard.png)

- New Trade can be entered in any listed US stock by using stock symbol

  ![New Trade](/screenshots/newtrade.png)

- Trade confirmation after a trade is placed successfully

  ![Trade Confirmation](/screenshots/trade_confirmation.png)

- A summary of all open and closed trades as well as account metrics are updated on the dashboard in real-time

  ![Dashboard Update](/screenshots/dashboard_update.png)

- Multiple watchlists can be added

  ![Watchlists](/screenshots/watchlists.png)

- Multiple stocks can be added and tracked in each watchlists

  ![Watchlist View](/screenshots/watchlist_view.png)