
import yfinance as yf

print(f'jugaad_data version: {jd.__version__}')

n = NSELive()
stock_price = n.stock_quote('HDFC')
print(stock_price)
