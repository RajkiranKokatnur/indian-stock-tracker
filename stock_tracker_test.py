import yfinance as yf
import pandas as pd
from datetime import datetime

# Test with just 10 major stocks
stocks = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
    'BHARTIARTL.NS', 'ITC.NS', 'SBIN.NS', 'LT.NS', 'HINDUNILVR.NS'
]

print("Testing with 10 major stocks...")
results = []

for stock in stocks:
    try:
        print(f"Downloading {stock}...")
        data = yf.download(stock, period='5d', progress=False)
        if len(data) >= 2:
            prev_close = data['Close'].iloc[-2]
            curr_close = data['Close'].iloc[-1]
            pct_change = ((curr_close - prev_close) / prev_close) * 100
            results.append({
                'symbol': stock,
                'change': round(pct_change, 2),
                'status': 'SUCCESS'
            })
            print(f"  ✅ {stock}: {pct_change:+.2f}%")
        else:
            print(f"  ❌ {stock}: Not enough data")
    except Exception as e:
        print(f"  ❌ {stock}: Error - {e}")

print(f"\n{'='*50}")
print(f"Successfully downloaded: {len(results)}/{len(stocks)} stocks")
print(f"{'='*50}")