import io
import logging
from nsetools import Nse
import pandas as pd
import requests
import yfinance as yf
from jugaad_data.nse import NSELive

nse = Nse()

logging.basicConfig(filename="logs/app.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)


def get_all_tickers():
  logger.info("Triggered get_all_tickers function:")
  nse_url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"

  # create Session from 'real' browser
  headers = {'User-Agent': 'Mozilla/5.0'}
  s = requests.Session()
  s.headers.update(headers)

  # do a get call now
  response = s.get(nse_url)
  s.close()
  df_nse = pd.read_csv(io.BytesIO(response.content))

  # print the tickers/symbols
  tickers = df_nse['SYMBOL']
  logger.info("All the tickers are listed")
  #print("Sample tickers are:")
  #print(tickers[0:50])
  return tickers


#get_all_tickers()


def get_current_stock_value():
  data = get_all_tickers()
  count = 0
  for ticker in data:
    n = NSELive()
    if count <= 2:
      stock_data = {}
      stock_price = n.stock_quote(ticker)
      stock_data["symbol"] = stock_price['info']['symbol']
      stock_data["company"] = stock_price['info']['companyName']
      print(stock_price)
      print(stock_data)
      print(count)
      count += 1


get_current_stock_value()
