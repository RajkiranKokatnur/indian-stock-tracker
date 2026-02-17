"""
Indian Stock Market Movement Tracker - FIXED VERSION
Tracks daily stock movements by percentage categories
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import time
from typing import Dict, List

class StockMovementTracker:
    def __init__(self, data_file='stock_movements_history.csv'):
        self.data_file = data_file
        self.stock_list = []
        
    def fetch_nifty_500_stocks(self) -> List[str]:
        """Fetch list of Nifty 500 stocks"""
        try:
            print("Fetching Nifty 500 stock list...")
            url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
            df = pd.read_csv(url)
            
            # Add .NS suffix for Yahoo Finance
            stocks = [symbol + '.NS' for symbol in df['Symbol'].tolist()]
            print(f"Found {len(stocks)} stocks")
            return stocks
        except Exception as e:
            print(f"Error fetching stock list: {e}")
            # Fallback to Nifty 50 major stocks
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
            'BRITANNIA', 'SHREECEM', 'BPCL', 'TATACONSUM', 'UPL', 'BAJAJ-AUTO',
            'PIDILITIND', 'SIEMENS'
        ]
        return [stock + '.NS' for stock in major_stocks]
    
    def calculate_daily_movements(self, stocks: List[str]) -> Dict:
        """Calculate stock movements for the day"""
        print(f"\nProcessing {len(stocks)} stocks...")
        
        movements = {
            'up_15+': 0, 'up_10_15': 0, 'up_5_10': 0, 'up_3_5': 0,
            'down_3_5': 0, 'down_5_10': 0, 'down_10_15': 0, 'down_15+': 0,
            'neutral': 0
        }
        
        stock_details = []
        processed = 0
        successful = 0
        
        for stock in stocks:
            try:
                # Download last 5 days of data
                data = yf.download(stock, period='5d', progress=False, auto_adjust=True)
                
                if data is not None and len(data) >= 2:
                    # Get the last two closing prices
                    prev_close = float(data['Close'].iloc[-2])
                    curr_close = float(data['Close'].iloc[-1])
                    
                    # Calculate percentage change
                    pct_change = ((curr_close - prev_close) / prev_close) * 100
                    
                    # Categorize movement
                    category = self._categorize_movement(pct_change)
                    movements[category] += 1
                    
                    stock_details.append({
                        'symbol': stock.replace('.NS', ''),
                        'change_pct': round(pct_change, 2),
                        'category': category
                    })
                    
                    successful += 1
                
                processed += 1
                if processed % 50 == 0:
                    print(f"Processed {processed}/{len(stocks)} stocks... ({successful} successful)")
                    time.sleep(1)  # Rate limiting
                    
            except Exception as e:
                # Skip stocks with errors silently
                processed += 1
                continue
        
        print(f"\nSuccessfully processed {successful} out of {len(stocks)} stocks")
        return movements, stock_details
    
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
    
    def save_daily_data(self, movements: Dict):
        """Save daily movement data to CSV"""
        today = datetime.now().date()
        
        # Prepare data row
        row = {
            'date': today,
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
        
        # Check if file exists
        if os.path.exists(self.data_file):
            df = pd.read_csv(self.data_file)
            # Update if today's data exists, else append
            if today.strftime('%Y-%m-%d') in df['date'].values:
                df.loc[df['date'] == today.strftime('%Y-%m-%d')] = list(row.values())
            else:
                df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        else:
            df = pd.DataFrame([row])
        
        df.to_csv(self.data_file, index=False)
        print(f"\n✅ Data saved to {self.data_file}")
    
    def display_summary(self, movements: Dict):
        """Display daily summary"""
        print("\n" + "="*60)
        print(f"DAILY MARKET MOVEMENT SUMMARY - {datetime.now().date()}")
        print("="*60)
        print(f"\n📈 GAINERS:")
        print(f"  15%+      : {movements['up_15+']} stocks")
        print(f"  10-15%    : {movements['up_10_15']} stocks")
        print(f"  5-10%     : {movements['up_5_10']} stocks")
        print(f"  3-5%      : {movements['up_3_5']} stocks")
        
        print(f"\n📉 LOSERS:")
        print(f"  -3 to -5% : {movements['down_3_5']} stocks")
        print(f"  -5 to -10%: {movements['down_5_10']} stocks")
        print(f"  -10 to -15%: {movements['down_10_15']} stocks")
        print(f"  -15%+     : {movements['down_15+']} stocks")
        
        print(f"\n➡️  Neutral (-3% to +3%): {movements['neutral']} stocks")
        print("="*60)
        
        # Market breadth analysis
        total_movers = sum(movements.values()) - movements['neutral']
        up_stocks = movements['up_15+'] + movements['up_10_15'] + movements['up_5_10'] + movements['up_3_5']
        down_stocks = movements['down_15+'] + movements['down_10_15'] + movements['down_5_10'] + movements['down_3_5']
        
        if total_movers > 0:
            advance_decline = (up_stocks / total_movers) * 100
            print(f"\n📊 Market Breadth: {advance_decline:.1f}% advancing")
            if advance_decline > 60:
                print("   Strong bullish sentiment ✅")
            elif advance_decline < 40:
                print("   Strong bearish sentiment ⚠️")
            else:
                print("   Mixed/Neutral sentiment ➡️")
        print()
    
    def run_daily_tracking(self):
        """Main function to run daily tracking"""
        print("="*60)
        print("Starting Daily Stock Movement Tracker...")
        print(f"Timestamp: {datetime.now()}")
        print("="*60)
        
        # Fetch stock list
        stocks = self.fetch_nifty_500_stocks()
        self.stock_list = stocks
        
        # Calculate movements
        movements, details = self.calculate_daily_movements(stocks)
        
        # Display summary
        self.display_summary(movements)
        
        # Save data
        self.save_daily_data(movements)
        
        # Save detailed stock list
        if details:
            details_file = f"stock_details_{datetime.now().date()}.csv"
            pd.DataFrame(details).to_csv(details_file, index=False)
            print(f"✅ Detailed stock data saved to {details_file}")
        
        print("\n" + "="*60)
        print("✅ TRACKING COMPLETE!")
        print("="*60)
        
        return movements, details


if __name__ == "__main__":
    tracker = StockMovementTracker()
    tracker.run_daily_tracking()
