"""
Indian Stock Market Movement Tracker with Sector Analysis
Tracks daily stock movements by percentage categories AND sectors
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import time
from typing import Dict, List

class StockMovementTracker:
    def __init__(self, data_file='stock_movements_history.csv', sector_file='sector_movements_history.csv'):
        self.data_file = data_file
        self.sector_file = sector_file
        self.stock_list = []
        self.sector_mapping = {}
        
    def fetch_nifty_500_stocks(self) -> pd.DataFrame:
        """Fetch list of Nifty 500 stocks with sector information"""
        try:
            print("Fetching Nifty 500 stock list with sectors...")
            url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
            df = pd.read_csv(url)
            
            # Clean sector names
            df['Industry'] = df['Industry'].fillna('Other')
            
            print(f"Found {len(df)} stocks across {df['Industry'].nunique()} sectors")
            return df
        except Exception as e:
            print(f"Error fetching stock list: {e}")
            return self._get_fallback_stocks_with_sectors()
    
    def _get_fallback_stocks_with_sectors(self) -> pd.DataFrame:
        """Fallback list of major NSE stocks with sectors"""
        stocks_data = {
            'Symbol': ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR', 'ICICIBANK',
                      'KOTAKBANK', 'SBIN', 'BHARTIARTL', 'BAJFINANCE', 'ITC', 'ASIANPAINT',
                      'MARUTI', 'AXISBANK', 'LT', 'TITAN', 'SUNPHARMA', 'ULTRACEMCO'],
            'Industry': ['Oil & Gas', 'IT', 'Banks', 'IT', 'FMCG', 'Banks',
                        'Banks', 'Banks', 'Telecom', 'Finance', 'FMCG', 'Paints',
                        'Auto', 'Banks', 'Construction', 'Consumer Goods', 'Pharma', 'Cement']
        }
        return pd.DataFrame(stocks_data)
    
    def calculate_daily_movements(self, stocks_df: pd.DataFrame) -> tuple:
        """Calculate stock movements for the day with sector breakdown"""
        print(f"\nProcessing {len(stocks_df)} stocks...")
        
        # Overall movements
        movements = {
            'up_15+': 0, 'up_10_15': 0, 'up_5_10': 0, 'up_3_5': 0,
            'down_3_5': 0, 'down_5_10': 0, 'down_10_15': 0, 'down_15+': 0,
            'neutral': 0
        }
        
        # Sector-wise movements
        sectors = stocks_df['Industry'].unique()
        sector_movements = {sector: {
            'up_3+': 0, 'down_3+': 0, 'neutral': 0, 'total': 0
        } for sector in sectors}
        
        stock_details = []
        processed = 0
        successful = 0
        
        for idx, row in stocks_df.iterrows():
            stock = row['Symbol'] + '.NS'
            sector = row['Industry']
            
            try:
                # Download last 5 days of data
                data = yf.download(stock, period='5d', progress=False, auto_adjust=True)
                
                if data is not None and len(data) >= 2:
                    prev_close = float(data['Close'].iloc[-2])
                    curr_close = float(data['Close'].iloc[-1])
                    pct_change = ((curr_close - prev_close) / prev_close) * 100
                    
                    # Categorize movement
                    category = self._categorize_movement(pct_change)
                    movements[category] += 1
                    
                    # Update sector movements
                    sector_movements[sector]['total'] += 1
                    if pct_change >= 3:
                        sector_movements[sector]['up_3+'] += 1
                    elif pct_change <= -3:
                        sector_movements[sector]['down_3+'] += 1
                    else:
                        sector_movements[sector]['neutral'] += 1
                    
                    stock_details.append({
                        'symbol': row['Symbol'],
                        'sector': sector,
                        'change_pct': round(pct_change, 2),
                        'category': category
                    })
                    
                    successful += 1
                
                processed += 1
                if processed % 50 == 0:
                    print(f"Processed {processed}/{len(stocks_df)} stocks... ({successful} successful)")
                    time.sleep(1)
                    
            except Exception as e:
                processed += 1
                continue
        
        print(f"\nSuccessfully processed {successful} out of {len(stocks_df)} stocks")
        return movements, sector_movements, stock_details
    
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
    
    def save_daily_data(self, movements: Dict, sector_movements: Dict):
        """Save daily movement data to CSV"""
        today = datetime.now().date()
        
        # Save overall movements
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
        
        if os.path.exists(self.data_file):
            df = pd.read_csv(self.data_file)
            if today.strftime('%Y-%m-%d') in df['date'].values:
                df.loc[df['date'] == today.strftime('%Y-%m-%d')] = list(row.values())
            else:
                df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        else:
            df = pd.DataFrame([row])
        
        df.to_csv(self.data_file, index=False)
        print(f"\n✅ Data saved to {self.data_file}")
        
        # Save sector movements
        sector_rows = []
        for sector, moves in sector_movements.items():
            if moves['total'] > 0:
                breadth = (moves['up_3+'] / moves['total'] * 100) if moves['total'] > 0 else 0
                sector_rows.append({
                    'date': today,
                    'sector': sector,
                    'up_3_plus': moves['up_3+'],
                    'down_3_plus': moves['down_3+'],
                    'neutral': moves['neutral'],
                    'total': moves['total'],
                    'breadth': round(breadth, 1)
                })
        
        sector_df = pd.DataFrame(sector_rows)
        
        if os.path.exists(self.sector_file):
            existing_sector_df = pd.read_csv(self.sector_file)
            # Remove today's data if exists, then append new
            existing_sector_df = existing_sector_df[existing_sector_df['date'] != today.strftime('%Y-%m-%d')]
            sector_df = pd.concat([existing_sector_df, sector_df], ignore_index=True)
        
        sector_df.to_csv(self.sector_file, index=False)
        print(f"✅ Sector data saved to {self.sector_file}")
    
    def display_summary(self, movements: Dict, sector_movements: Dict):
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
        
        # Market breadth
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
        
        # Top performing sectors
        print(f"\n🏢 TOP PERFORMING SECTORS:")
        sector_breadth = []
        for sector, moves in sector_movements.items():
            if moves['total'] >= 5:  # Only show sectors with at least 5 stocks
                breadth = (moves['up_3+'] / moves['total'] * 100) if moves['total'] > 0 else 0
                sector_breadth.append((sector, breadth, moves['total']))
        
        sector_breadth.sort(key=lambda x: x[1], reverse=True)
        for i, (sector, breadth, total) in enumerate(sector_breadth[:5], 1):
            print(f"  {i}. {sector:<20} {breadth:>5.1f}% ({total} stocks)")
        
        print(f"\n🏢 WORST PERFORMING SECTORS:")
        for i, (sector, breadth, total) in enumerate(sector_breadth[-5:], 1):
            print(f"  {i}. {sector:<20} {breadth:>5.1f}% ({total} stocks)")
        
        print()
    
    def run_daily_tracking(self):
        """Main function to run daily tracking"""
        print("="*60)
        print("Starting Daily Stock Movement Tracker with Sector Analysis...")
        print(f"Timestamp: {datetime.now()}")
        print("="*60)
        
        # Fetch stock list with sectors
        stocks_df = self.fetch_nifty_500_stocks()
        
        # Calculate movements
        movements, sector_movements, details = self.calculate_daily_movements(stocks_df)
        
        # Display summary
        self.display_summary(movements, sector_movements)
        
        # Save data
        self.save_daily_data(movements, sector_movements)
        
        # Save detailed stock list
        if details:
            details_file = f"stock_details_{datetime.now().date()}.csv"
            pd.DataFrame(details).to_csv(details_file, index=False)
            print(f"✅ Detailed stock data saved to {details_file}")
        
        print("\n" + "="*60)
        print("✅ TRACKING COMPLETE!")
        print("="*60)
        
        return movements, sector_movements, details


if __name__ == "__main__":
    tracker = StockMovementTracker()
    tracker.run_daily_tracking()
