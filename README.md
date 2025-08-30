# StockSim
StockSim is a web based stock trading simulator, which enables users to create virtual stock trading accounts and trade the US Equity markets with virtual money. Users can test their trading skills and strategies on live markets and keep a record of their trading performance.

## Docker (web + Postgres)

This project ships with a Dockerfile and docker-compose.yml to run the app and a Postgres database.

Quick start:

1. Build the image and start services:

  - Build the image: `docker compose build`
  - Start the stack: `docker compose up -d`

2. App will be available at http://localhost:8000/stocksim (WSGI mounts the app under `/stocksim`).

3. Database connection used in Compose: `postgresql://stocksim:stocksim@db:5432/stocksim`.

Notes:

- The image contains the full code base. In development, you can uncomment the bind mount in `docker-compose.yml` to live-edit code.
- To seed local data: `docker compose exec web python seed.py`.
- Logs: `docker compose logs -f web` and `docker compose logs -f db`.
- Stop and clean up: `docker compose down` (add `-v` to remove DB volume).

## Host on Ubuntu with HTTPS (Caddy)

Prereqs:
- Ubuntu box reachable via your DDNS domain (e.g., myname.ddns.net) and ports 80/443 open/forwarded to the server.
- Docker and Docker Compose installed.

Steps:
1. Copy repo to server:
  - git clone https://github.com/omermj/stocksim.git && cd stocksim
2. Create a `.env` file (on the server, not committed):
  - DOMAIN=myname.ddns.net
  - EMAIL=you@example.com        # optional, for Let’s Encrypt account
  - SECRET_KEY=your_flask_secret
  - ALPACA_API_KEY=...
  - ALPACA_SECRET_KEY=...
3a. If you want Dockerized Caddy: 
   - docker compose -f docker-compose.prod.yml build
   - docker compose -f docker-compose.prod.yml up -d
   - Visit: `https://myname.ddns.net/`

3b. If Caddy already runs on the host (systemd):
   - Start only web+db and bind web to loopback:
     - docker compose -f docker-compose.host-caddy.yml build
     - docker compose -f docker-compose.host-caddy.yml up -d
   - To serve the app at a subpath (e.g., https://myname.ddns.net/stocksim), add this to your host Caddyfile (e.g., /etc/caddy/Caddyfile):
     
     myname.ddns.net {
       encode gzip zstd
       # Proxy only the /stocksim path; strip it before forwarding
       handle_path /stocksim* {
         reverse_proxy 127.0.0.1:8000 {
           header_up X-Forwarded-Prefix "/stocksim"
         }
       }
       log {
         output file /var/log/caddy/stocksim.log
         format json
       }
     }
   - Reload Caddy:
     - sudo systemctl reload caddy
   - Visit: `https://myname.ddns.net/stocksim`

   Notes:
   - The app already enables ProxyFix with x_prefix, so setting X-Forwarded-Prefix makes url_for/static URLs include the /stocksim prefix correctly.

Notes:
- Postgres isn’t exposed publicly; only Caddy exposes 80/443.
- Certificates are handled automatically by Caddy and stored in a Docker volume.
- Update the app without downtime: rebuild and restart `web` only.
  - docker compose -f docker-compose.prod.yml build web
  - docker compose -f docker-compose.prod.yml up -d web


Live link: https://stocksim.herokuapp.com/

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


## Installation instructions

1. Create a free account on Alpaca Markets API (https://alpaca.markets/data) to get your API keys
2. Clone the repo to your local machine

        $ git clone https://github.com/codersixteen/stocksim.git

3. If not already, install PostgreSQL in your development environment
4. Create a Postgres Database (app assumes a default name of <code>stocksim-db</code>, but can be changed in <code>config.py</code> file)

        $ createdb stocksim-db

5. Create a virtual environment and install app dependencies in the new virtual environment:
   
        $ pip install -r requirements.txt

6. In <code>keys.py</code> file, put your API keys from Alpaca Data API. You can also save the keys in your environment variables. App will first check for keys in environment variables and if not available, it will use the keys provided in <code>keys.py</code> file.
   
7. Run the <code>seed.py</code> to create tables in the database and setup a sample user
   
        $ python seed.py

8. Run flask server:

        $ flask run


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