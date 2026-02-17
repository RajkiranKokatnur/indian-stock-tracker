"""
Backfill Historical Data - Last 2 Weeks
Collects stock movement data for the past 14 days
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import time
from typing import Dict, List

class HistoricalDataBackfill:
    def __init__(self, data_file='stock_movements_history.csv'):
        self.data_file = data_file
        
    def fetch_nifty_500_stocks(self) -> List[str]:
        """Fetch list of Nifty 500 stocks"""
        try:
            print("Fetching Nifty 500 stock list...")
            url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
            df = pd.read_csv(url)
            stocks = [symbol + '.NS' for symbol in df['Symbol'].tolist()]
            print(f"Found {len(stocks)} stocks")
            return stocks
        except Exception as e:
            print(f"Error fetching stock list: {e}")
            return self._get_fallback_stocks()
    
    def _get_fallback_stocks(self) -> List[str]:
        """Fallback list of major NSE stocks"""
        major_stocks = [
            'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR', 'ICICIBANK',
            'KOTAKBANK', 'SBIN', 'BHARTIARTL', 'BAJFINANCE', 'ITC', 'ASIANPAINT',
            'MARUTI', 'AXISBANK', 'LT', 'TITAN', 'SUNPHARMA', 'ULTRACEMCO',
            'NESTLEIND', 'WIPRO', 'TATAMOTORS', 'HCLTECH', 'ADANIENT', 'ONGC',
            'NTPC', 'POWERGRID', 'BAJAJFINSV', 'M&M', 'COALINDIA', 'DRREDDY',
            'JSWSTEEL', 'TATASTEEL', 'INDUSINDBK', 'TECHM', 'HINDALCO', 'ADANIPORTS',
            'EICHERMOT', 'APOLLOHOSP', 'GRASIM', 'CIPLA', 'DIVISLAB', 'HEROMOTOCO',
            'BRITANNIA', 'SHREECEM', 'BPCL', 'TATACONSUM', 'UPL', 'BAJAJ-AUTO'
        ]
        return [stock + '.NS' for stock in major_stocks]
    
    def get_trading_days(self, days_back=14) -> List[datetime]:
        """Get list of trading days (exclude weekends)"""
        trading_days = []
        current_date = datetime.now().date()
        
        for i in range(days_back + 1):
            date = current_date - timedelta(days=i)
            # Exclude weekends (Saturday=5, Sunday=6)
            if date.weekday() < 5:
                trading_days.append(date)
        
        trading_days.reverse()  # Oldest first
        return trading_days
    
    def calculate_movements_for_date(self, stocks: List[str], target_date: datetime) -> Dict:
        """Calculate stock movements for a specific date"""
        movements = {
            'up_15+': 0, 'up_10_15': 0, 'up_5_10': 0, 'up_3_5': 0,
            'down_3_5': 0, 'down_5_10': 0, 'down_10_15': 0, 'down_15+': 0,
            'neutral': 0
        }
        
        successful = 0
        
        # Download data for all stocks at once (more efficient)
        print(f"   Downloading data for {len(stocks)} stocks...")
        
        # Use a date range that includes the target date and previous day
        end_date = target_date + timedelta(days=1)
        start_date = target_date - timedelta(days=5)  # Get extra days for safety
        
        for i, stock in enumerate(stocks):
            try:
                # Download historical data
                data = yf.download(stock, start=start_date, end=end_date, progress=False, auto_adjust=True)
                
                if data is not None and len(data) >= 2:
                    # Find the target date in the data
                    data.index = pd.to_datetime(data.index).date
                    
                    if target_date in data.index:
                        # Get target date index
                        target_idx = data.index.get_loc(target_date)
                        
                        if target_idx > 0:
                            prev_close = float(data['Close'].iloc[target_idx - 1])
                            curr_close = float(data['Close'].iloc[target_idx])
                            
                            pct_change = ((curr_close - prev_close) / prev_close) * 100
                            category = self._categorize_movement(pct_change)
                            movements[category] += 1
                            successful += 1
                
                # Progress indicator every 100 stocks
                if (i + 1) % 100 == 0:
                    print(f"   Processed {i + 1}/{len(stocks)} stocks... ({successful} successful)")
                    
            except Exception as e:
                continue
        
        print(f"   ✅ Successfully processed {successful} stocks for {target_date}")
        return movements
    
    def _categorize_movement(self, pct_change: float) -> str:
        """Categorize stock movement by percentage"""
        if pct_change >= 15:
            return 'up_15+'
        elif pct_change >= 10:
            return 'up_10_15'
        elif pct_change >= 5:
            return 'up_5_10'
        elif pct_change >= 3:
            return 'up_3_5'
        elif pct_change <= -15:
            return 'down_15+'
        elif pct_change <= -10:
            return 'down_10_15'
        elif pct_change <= -5:
            return 'down_5_10'
        elif pct_change <= -3:
            return 'down_3_5'
        else:
            return 'neutral'
    
    def backfill_data(self, days_back=14):
        """Backfill historical data for the specified number of days"""
        print("="*70)
        print("HISTORICAL DATA BACKFILL - LAST 2 WEEKS")
        print("="*70)
        
        # Get stock list
        stocks = self.fetch_nifty_500_stocks()
        
        # Get trading days
        trading_days = self.get_trading_days(days_back)
        print(f"\nFound {len(trading_days)} trading days to process")
        print(f"Date range: {trading_days[0]} to {trading_days[-1]}")
        
        # Prepare data structure
        all_data = []
        
        # Process each day
        for idx, trade_date in enumerate(trading_days, 1):
            print(f"\n[{idx}/{len(trading_days)}] Processing {trade_date.strftime('%Y-%m-%d (%A)')}...")
            
            movements = self.calculate_movements_for_date(stocks, trade_date)
            
            # Prepare row
            row = {
                'date': trade_date,
                'up_15_plus': movements['up_15+'],
                'up_10_15': movements['up_10_15'],
                'up_5_10': movements['up_5_10'],
                'up_3_5': movements['up_3_5'],
                'down_3_5': movements['down_3_5'],
                'down_5_10': movements['down_5_10'],
                'down_10_15': movements['down_10_15'],
                'down_15_plus': movements['down_15+'],
                'neutral': movements['neutral']
            }
            
            all_data.append(row)
            
            # Display summary
            gainers = movements['up_15+'] + movements['up_10_15'] + movements['up_5_10'] + movements['up_3_5']
            losers = movements['down_15+'] + movements['down_10_15'] + movements['down_5_10'] + movements['down_3_5']
            total_movers = gainers + losers
            breadth = (gainers / total_movers * 100) if total_movers > 0 else 50
            
            print(f"   Gainers: {gainers} | Losers: {losers} | Breadth: {breadth:.1f}%")
            
            # Small delay between days
            time.sleep(1)
        
        # Save to CSV
        df = pd.DataFrame(all_data)
        df.to_csv(self.data_file, index=False)
        
        print("\n" + "="*70)
        print("✅ BACKFILL COMPLETE!")
        print("="*70)
        print(f"✅ Data saved to: {self.data_file}")
        print(f"✅ Total days processed: {len(trading_days)}")
        print(f"✅ Date range: {trading_days[0]} to {trading_days[-1]}")
        print("\n🎨 You can now launch the dashboard to view trends!")
        print("   Command: streamlit run dashboard.py")
        print("="*70)

if __name__ == "__main__":
    backfill = HistoricalDataBackfill()
    backfill.backfill_data(days_back=14)
