"""
Stock Movement Visualization and Trend Analysis
Generates charts and insights from historical tracking data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

class StockMovementVisualizer:
    def __init__(self, data_file='stock_movements_history.csv'):
        self.data_file = data_file
        self.df = None
        
    def load_data(self):
        """Load historical data"""
        if not os.path.exists(self.data_file):
            print(f"Error: {self.data_file} not found!")
            print("Run stock_tracker.py first to collect data.")
            return False
        
        self.df = pd.read_csv(self.data_file)
        self.df['date'] = pd.to_datetime(self.df['date'])
        print(f"Loaded {len(self.df)} days of data")
        return True
    
    def create_all_visualizations(self):
        """Generate all visualization charts"""
        if not self.load_data():
            return
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (15, 10)
        
        # Create subplots
        fig = plt.figure(figsize=(18, 12))
        
        # 1. Market Breadth Trend (Gainers vs Losers over time)
        ax1 = plt.subplot(3, 2, 1)
        self._plot_market_breadth(ax1)
        
        # 2. Extreme Movements Trend (15%+ moves)
        ax2 = plt.subplot(3, 2, 2)
        self._plot_extreme_movements(ax2)
        
        # 3. Distribution Heatmap
        ax3 = plt.subplot(3, 2, 3)
        self._plot_distribution_heatmap(ax3)
        
        # 4. Advance-Decline Line
        ax4 = plt.subplot(3, 2, 4)
        self._plot_advance_decline(ax4)
        
        # 5. Volatility Trend (Total movers 3%+)
        ax5 = plt.subplot(3, 2, 5)
        self._plot_volatility_trend(ax5)
        
        # 6. Weekly Pattern Analysis
        ax6 = plt.subplot(3, 2, 6)
        self._plot_weekly_pattern(ax6)
        
        plt.tight_layout()
        
        # Save figure
        output_file = f'stock_movement_dashboard_{datetime.now().date()}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\n📊 Dashboard saved as: {output_file}")
        
        plt.show()
    
    def _plot_market_breadth(self, ax):
        """Plot gainers vs losers over time"""
        gainers = self.df['up_3_5'] + self.df['up_5_10'] + self.df['up_10_15'] + self.df['up_15_plus']
        losers = self.df['down_3_5'] + self.df['down_5_10'] + self.df['down_10_15'] + self.df['down_15_plus']
        
        ax.plot(self.df['date'], gainers, label='Gainers (3%+)', color='green', linewidth=2, marker='o')
        ax.plot(self.df['date'], losers, label='Losers (3%+)', color='red', linewidth=2, marker='o')
        ax.fill_between(self.df['date'], gainers, alpha=0.3, color='green')
        ax.fill_between(self.df['date'], losers, alpha=0.3, color='red')
        
        ax.set_title('Market Breadth: Gainers vs Losers (3%+ moves)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Stocks')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def _plot_extreme_movements(self, ax):
        """Plot extreme movements (15%+) over time"""
        ax.plot(self.df['date'], self.df['up_15_plus'], label='Up 15%+', 
                color='darkgreen', linewidth=2, marker='^', markersize=8)
        ax.plot(self.df['date'], self.df['down_15_plus'], label='Down 15%+', 
                color='darkred', linewidth=2, marker='v', markersize=8)
        
        ax.set_title('Extreme Movements (15%+)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Stocks')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def _plot_distribution_heatmap(self, ax):
        """Create heatmap of stock distribution across categories"""
        categories = ['up_15_plus', 'up_10_15', 'up_5_10', 'up_3_5', 
                     'neutral', 'down_3_5', 'down_5_10', 'down_10_15', 'down_15_plus']
        
        heatmap_data = self.df[categories].T
        
        sns.heatmap(heatmap_data, cmap='RdYlGn', center=heatmap_data.mean().mean(),
                   cbar_kws={'label': 'Stock Count'}, ax=ax, annot=False)
        
        ax.set_title('Distribution Heatmap (Darker = More Stocks)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Date Index')
        ax.set_yticklabels(['↑15%+', '↑10-15%', '↑5-10%', '↑3-5%', 
                           'Neutral', '↓3-5%', '↓5-10%', '↓10-15%', '↓15%+'], rotation=0)
    
    def _plot_advance_decline(self, ax):
        """Plot cumulative advance-decline line"""
        gainers = self.df['up_3_5'] + self.df['up_5_10'] + self.df['up_10_15'] + self.df['up_15_plus']
        losers = self.df['down_3_5'] + self.df['down_5_10'] + self.df['down_10_15'] + self.df['down_15_plus']
        
        daily_diff = gainers - losers
        cumulative_ad = daily_diff.cumsum()
        
        ax.plot(self.df['date'], cumulative_ad, linewidth=2.5, color='blue')
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax.fill_between(self.df['date'], cumulative_ad, 0, 
                       where=(cumulative_ad >= 0), alpha=0.3, color='green', label='Bullish')
        ax.fill_between(self.df['date'], cumulative_ad, 0, 
                       where=(cumulative_ad < 0), alpha=0.3, color='red', label='Bearish')
        
        ax.set_title('Cumulative Advance-Decline Line', fontsize=12, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Difference')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def _plot_volatility_trend(self, ax):
        """Plot overall market volatility (total stocks moving 3%+)"""
        total_movers = (self.df['up_3_5'] + self.df['up_5_10'] + self.df['up_10_15'] + 
                       self.df['up_15_plus'] + self.df['down_3_5'] + self.df['down_5_10'] + 
                       self.df['down_10_15'] + self.df['down_15_plus'])
        
        ax.bar(self.df['date'], total_movers, color='purple', alpha=0.6)
        ax.plot(self.df['date'], total_movers.rolling(window=5, min_periods=1).mean(), 
               color='orange', linewidth=3, label='5-day MA')
        
        ax.set_title('Market Volatility (Total Stocks Moving 3%+)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Stocks')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def _plot_weekly_pattern(self, ax):
        """Analyze patterns by day of week"""
        if len(self.df) < 7:
            ax.text(0.5, 0.5, 'Need at least 7 days of data\nfor weekly pattern analysis',
                   ha='center', va='center', fontsize=12)
            ax.set_title('Weekly Pattern Analysis', fontsize=12, fontweight='bold')
            return
        
        self.df['day_of_week'] = self.df['date'].dt.day_name()
        
        gainers = self.df['up_3_5'] + self.df['up_5_10'] + self.df['up_10_15'] + self.df['up_15_plus']
        losers = self.df['down_3_5'] + self.df['down_5_10'] + self.df['down_10_15'] + self.df['down_15_plus']
        
        weekly_data = pd.DataFrame({
            'day': self.df['day_of_week'],
            'gainers': gainers,
            'losers': losers
        })
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        weekly_avg = weekly_data.groupby('day').mean().reindex(day_order)
        
        x = range(len(weekly_avg))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], weekly_avg['gainers'], width, 
              label='Avg Gainers', color='green', alpha=0.7)
        ax.bar([i + width/2 for i in x], weekly_avg['losers'], width, 
              label='Avg Losers', color='red', alpha=0.7)
        
        ax.set_title('Average Gainers/Losers by Day of Week', fontsize=12, fontweight='bold')
        ax.set_xlabel('Day of Week')
        ax.set_ylabel('Average Number of Stocks')
        ax.set_xticks(x)
        ax.set_xticklabels(day_order, rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    def generate_insights(self):
        """Generate textual insights from the data"""
        if not self.load_data():
            return
        
        print("\n" + "="*70)
        print("📈 MARKET INSIGHTS & TREND ANALYSIS")
        print("="*70)
        
        # Latest data
        latest = self.df.iloc[-1]
        print(f"\n📅 Latest Data ({latest['date'].date()}):")
        
        gainers = latest['up_3_5'] + latest['up_5_10'] + latest['up_10_15'] + latest['up_15_plus']
        losers = latest['down_3_5'] + latest['down_5_10'] + latest['down_10_15'] + latest['down_15_plus']
        
        print(f"   Gainers (3%+): {int(gainers)} stocks")
        print(f"   Losers (3%+): {int(losers)} stocks")
        print(f"   Extreme gains (15%+): {int(latest['up_15_plus'])} stocks")
        print(f"   Extreme losses (15%+): {int(latest['down_15_plus'])} stocks")
        
        # Trend analysis (last 5 days if available)
        if len(self.df) >= 5:
            print(f"\n📊 5-Day Trend:")
            recent = self.df.tail(5)
            
            avg_gainers = (recent['up_3_5'] + recent['up_5_10'] + 
                          recent['up_10_15'] + recent['up_15_plus']).mean()
            avg_losers = (recent['down_3_5'] + recent['down_5_10'] + 
                         recent['down_10_15'] + recent['down_15_plus']).mean()
            
            print(f"   Average gainers: {avg_gainers:.1f} stocks/day")
            print(f"   Average losers: {avg_losers:.1f} stocks/day")
            
            if avg_gainers > avg_losers * 1.2:
                print(f"   ✅ Bullish trend - More gainers than losers")
            elif avg_losers > avg_gainers * 1.2:
                print(f"   ⚠️ Bearish trend - More losers than gainers")
            else:
                print(f"   ➡️ Neutral/Mixed trend")
        
        # Volatility analysis
        if len(self.df) >= 2:
            print(f"\n🌊 Volatility Analysis:")
            total_movers = (self.df['up_3_5'] + self.df['up_5_10'] + self.df['up_10_15'] + 
                          self.df['up_15_plus'] + self.df['down_3_5'] + self.df['down_5_10'] + 
                          self.df['down_10_15'] + self.df['down_15_plus'])
            
            avg_volatility = total_movers.mean()
            latest_volatility = total_movers.iloc[-1]
            
            print(f"   Average daily movers (3%+): {avg_volatility:.1f} stocks")
            print(f"   Latest: {int(latest_volatility)} stocks")
            
            if latest_volatility > avg_volatility * 1.3:
                print(f"   🔥 High volatility day (+{((latest_volatility/avg_volatility - 1) * 100):.0f}% above average)")
            elif latest_volatility < avg_volatility * 0.7:
                print(f"   😴 Low volatility day ({((1 - latest_volatility/avg_volatility) * 100):.0f}% below average)")
        
        print("="*70 + "\n")


if __name__ == "__main__":
    viz = StockMovementVisualizer()
    viz.generate_insights()
    viz.create_all_visualizations()
