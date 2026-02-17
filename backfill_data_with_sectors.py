"""
Backfill Historical Data with Sector Analysis - Last 2 Weeks
Collects stock movement data AND sector performance for the past 14 days
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import time
from typing import Dict, List

class HistoricalDataBackfillWithSectors:
    def __init__(self, data_file='stock_movements_history.csv', sector_file='sector_movements_history.csv'):
        self.data_file = data_file
        self.sector_file = sector_file
        
    def fetch_nifty_500_stocks(self) -> pd.DataFrame:
        """Fetch list of Nifty 500 stocks with sector information"""
        try:
            print("Fetching Nifty 500 stock list with sectors...")
            url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
            df = pd.read_csv(url)
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
                      'MARUTI', 'AXISBANK', 'LT', 'TITAN', 'SUNPHARMA', 'ULTRACEMCO',
                      'NESTLEIND', 'WIPRO', 'TATAMOTORS', 'HCLTECH', 'ONGC', 'NTPC',
                      'POWERGRID', 'BAJAJFINSV', 'COALINDIA', 'DRREDDY', 'JSWSTEEL', 'TATASTEEL'],
            'Industry': ['Oil & Gas', 'IT', 'Banks', 'IT', 'FMCG', 'Banks',
                        'Banks', 'Banks', 'Telecom', 'Finance', 'FMCG', 'Paints',
                        'Auto', 'Banks', 'Construction', 'Consumer Goods', 'Pharma', 'Cement',
                        'FMCG', 'IT', 'Auto', 'IT', 'Oil & Gas', 'Power',
                        'Power', 'Finance', 'Metals', 'Pharma', 'Metals', 'Metals']
        }
        return pd.DataFrame(stocks_data)
    
    def get_trading_days(self, days_back=14) -> List[datetime]:
        """Get list of trading days (exclude weekends)"""
        trading_days = []
        current_date = datetime.now().date()
        
        for i in range(days_back + 5):  # Add buffer for weekends
            date = current_date - timedelta(days=i)
            if date.weekday() < 5:  # Mon-Fri
                trading_days.append(date)
                if len(trading_days) >= days_back:
                    break
        
        trading_days.reverse()  # Oldest first
        return trading_days
    
    def calculate_movements_for_date(self, stocks_df: pd.DataFrame, target_date: datetime) -> tuple:
        """Calculate stock movements and sector performance for a specific date"""
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
        
        successful = 0
        end_date = target_date + timedelta(days=1)
        start_date = target_date - timedelta(days=5)
        
        print(f"   Processing {len(stocks_df)} stocks...")
        
        for i, row in stocks_df.iterrows():
            stock = row['Symbol'] + '.NS'
            sector = row['Industry']
            
            try:
                data = yf.download(stock, start=start_date, end=end_date, progress=False, auto_adjust=True)
                
                if data is not None and len(data) >= 2:
                    data.index = pd.to_datetime(data.index).date
                    
                    if target_date in data.index:
                        target_idx = data.index.get_loc(target_date)
                        
                        if target_idx > 0:
                            prev_close = float(data['Close'].iloc[target_idx - 1])
                            curr_close = float(data['Close'].iloc[target_idx])
                            pct_change = ((curr_close - prev_close) / prev_close) * 100
                            
                            # Overall categorization
                            category = self._categorize_movement(pct_change)
                            movements[category] += 1
                            
                            # Sector categorization
                            sector_movements[sector]['total'] += 1
                            if pct_change >= 3:
                                sector_movements[sector]['up_3+'] += 1
                            elif pct_change <= -3:
                                sector_movements[sector]['down_3+'] += 1
                            else:
                                sector_movements[sector]['neutral'] += 1
                            
                            successful += 1
                
                if (i + 1) % 100 == 0:
                    print(f"   Processed {i + 1}/{len(stocks_df)} stocks... ({successful} successful)")
                    
            except Exception as e:
                continue
        
        print(f"   ✅ Successfully processed {successful} stocks for {target_date}")
        return movements, sector_movements
    
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
        """Backfill historical data with sector analysis"""
        print("="*70)
        print("HISTORICAL DATA BACKFILL WITH SECTORS - LAST 2 WEEKS")
        print("="*70)
        
        # Get stock list with sectors
        stocks_df = self.fetch_nifty_500_stocks()
        
        # Get trading days
        trading_days = self.get_trading_days(days_back)
        print(f"\nFound {len(trading_days)} trading days to process")
        print(f"Date range: {trading_days[0]} to {trading_days[-1]}")
        print("\n⏱️  This will take 10-20 minutes. Processing...")
        
        # Prepare data structures
        all_movements = []
        all_sector_movements = []
        
        # Process each day
        for idx, trade_date in enumerate(trading_days, 1):
            print(f"\n[{idx}/{len(trading_days)}] Processing {trade_date.strftime('%Y-%m-%d (%A)')}...")
            
            movements, sector_movements = self.calculate_movements_for_date(stocks_df, trade_date)
            
            # Store overall movements
            all_movements.append({
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
            })
            
            # Store sector movements
            for sector, moves in sector_movements.items():
                if moves['total'] > 0:
                    breadth = (moves['up_3+'] / moves['total'] * 100)
                    all_sector_movements.append({
                        'date': trade_date,
                        'sector': sector,
                        'up_3_plus': moves['up_3+'],
                        'down_3_plus': moves['down_3+'],
                        'neutral': moves['neutral'],
                        'total': moves['total'],
                        'breadth': round(breadth, 1)
                    })
            
            # Display summary
            gainers = movements['up_15+'] + movements['up_10_15'] + movements['up_5_10'] + movements['up_3_5']
            losers = movements['down_15+'] + movements['down_10_15'] + movements['down_5_10'] + movements['down_3_5']
            total_movers = gainers + losers
            breadth = (gainers / total_movers * 100) if total_movers > 0 else 50
            
            print(f"   📊 Gainers: {gainers} | Losers: {losers} | Breadth: {breadth:.1f}%")
            
            # Show top/bottom sectors
            sector_breadth = [(s, (m['up_3+'] / m['total'] * 100)) 
                            for s, m in sector_movements.items() if m['total'] >= 3]
            sector_breadth.sort(key=lambda x: x[1], reverse=True)
            
            if len(sector_breadth) > 0:
                top_sector = sector_breadth[0]
                bottom_sector = sector_breadth[-1]
                print(f"   🏆 Top: {top_sector[0]} ({top_sector[1]:.0f}%)")
                print(f"   ⚠️  Bottom: {bottom_sector[0]} ({bottom_sector[1]:.0f}%)")
            
            time.sleep(1)
        
        # Save to CSV files
        print("\n" + "="*70)
        print("💾 Saving data...")
        
        # Save overall movements
        movements_df = pd.DataFrame(all_movements)
        movements_df.to_csv(self.data_file, index=False)
        print(f"✅ Overall movements saved to: {self.data_file}")
        
        # Save sector movements
        sector_df = pd.DataFrame(all_sector_movements)
        sector_df.to_csv(self.sector_file, index=False)
        print(f"✅ Sector movements saved to: {self.sector_file}")
        
        print("\n" + "="*70)
        print("✅ BACKFILL COMPLETE!")
        print("="*70)
        print(f"✅ Total days processed: {len(trading_days)}")
        print(f"✅ Date range: {trading_days[0]} to {trading_days[-1]}")
        print(f"✅ Sectors tracked: {len(stocks_df['Industry'].unique())}")
        print(f"✅ Total records: {len(movements_df)} days × {len(sector_df) // len(trading_days)} sectors")
        print("\n🎨 Launch the dashboard to see your data!")
        print("   Command: streamlit run dashboard.py")
        print("\n📊 You now have:")
        print("   • Movement category heatmap with 2 weeks history")
        print("   • Sector performance heatmap with 2 weeks history")
        print("   • All trends and patterns ready to analyze!")
        print("="*70)

if __name__ == "__main__":
    backfill = HistoricalDataBackfillWithSectors()
    backfill.backfill_data(days_back=60)
