import io
from jugaad_data.nse import NSELive
import logging
from nsetools import Nse
import pandas as pd
import redis_conn
import requests
import yfinance as yf
import json
import datetime
import pytz

nse = Nse()

logging.basicConfig(filename="logs/app.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)


def get_all_tickers():
  logger.info("Triggered get_all_tickers function")
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
    stock_data = {}
    to_redis = {}
    stock_price = n.stock_quote(ticker)
    #print(stock_price)

    stock_data["symbol"] = stock_price['info']['symbol']
    stock_data["company"] = stock_price['info']['companyName']
    stock_data["intra_min"] = stock_price['priceInfo']["intraDayHighLow"][
        "min"]
    stock_data["intra_max"] = stock_price['priceInfo']["intraDayHighLow"][
        "max"]
    stock_data["intra_val"] = stock_price['priceInfo']['intraDayHighLow'][
        "value"]
    stock_data["week_high"] = stock_price['priceInfo']['weekHighLow']["max"]
    stock_data["week_low"] = stock_price["priceInfo"]["weekHighLow"]["min"]
    stock_data["week_val"] = stock_price['priceInfo']['weekHighLow']["value"]
    stock_data["week_high_date"] = stock_price['priceInfo']['weekHighLow'][
        "maxDate"]
    stock_data["week_low_date"] = stock_price['priceInfo']['weekHighLow'][
        "minDate"]
    stock_data["lastprice"] = stock_price["priceInfo"]["lastPrice"]
    stock_data["change"] = stock_price["priceInfo"]["change"]
    stock_data["previousClose"] = stock_price["priceInfo"]["previousClose"]
    stock_data["open"] = stock_price["priceInfo"]["open"]
    stock_data["basePrice"] = stock_price["priceInfo"]["basePrice"]
    stock_data["macro"] = stock_price["industryInfo"]["macro"]
    stock_data["sector"] = stock_price["industryInfo"]["sector"]
    stock_data["pdSectorInd"] = stock_price["metadata"]["pdSectorInd"]
    IST = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(IST)
    stock_data["querried_time"] = current_time.strftime("%d-%m-%Y %H:%M:%S")
    json_object = json.dumps(stock_data)
    to_redis["symbol"] = stock_price["info"]["symbol"]
    to_redis["lastprice"] = stock_price["priceInfo"]["lastPrice"]
    response = redis_conn.push_to_redis(to_redis)
    print("Redis response: ", response)
    with open("data.json", "w") as outfile:
      outfile.write(json_object)
      outfile.write('\n')
    print(stock_data)
    redis_json_object = json.dumps(to_redis)
    with open("redis_test.json", "+a") as outfile:
      outfile.write(redis_json_object)
      outfile.write('\n')


get_current_stock_value()
