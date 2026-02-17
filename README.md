# 📊 Indian Stock Market Movement Tracker

A Python-based automated system to track daily movements of Indian stocks listed on NSE, categorized by percentage changes (3%, 5%, 10%, 15%). Includes historical data storage, trend visualization, and **interactive web dashboard**.

## 🎯 Features

- ✅ Tracks Nifty 500 stocks daily (or major Nifty 50 stocks as fallback)
- ✅ Categorizes stocks by movement: ±3%, ±5%, ±10%, ±15%
- ✅ Stores historical data in CSV format
- ✅ Automated daily execution
- ✅ **Interactive web dashboard with real-time charts**
- ✅ Comprehensive trend visualization with 6 different charts
- ✅ Market breadth and volatility analysis
- ✅ Advance-decline line tracking
- ✅ Weekly pattern analysis
- ✅ Export data to CSV/Excel

## 📁 Files Included

### Core Scripts:
1. **stock_tracker.py** - Main tracking script (fetches and analyzes data)
2. **visualize_trends.py** - Generates static charts and trend analysis
3. **dashboard.py** - **Interactive web dashboard (NEW!)**
4. **scheduler.py** - Automated daily scheduler

### Utilities:
5. **requirements.txt** - Python dependencies
6. **run_tracker.bat** / **run_tracker.sh** - Quick run scripts
7. **run_dashboard.bat** / **run_dashboard.sh** - **Launch dashboard**

### Documentation:
8. **README.md** - This file (complete guide)
9. **DASHBOARD_GUIDE.md** - **Interactive dashboard guide**
10. **QUICK_REFERENCE.md** - Cheat sheet for daily use
11. **config.ini** - Easy customization (optional)
12. **stock_movements_history_sample.csv** - Sample data for testing

## 🚀 Quick Start

### Step 1: Install Python

Make sure you have Python 3.8+ installed:
```bash
python --version
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install yfinance pandas matplotlib seaborn schedule
```

### Step 3: Run the Tracker Manually (First Time)

```bash
python stock_tracker.py
```

This will:
- Fetch Nifty 500 stock list
- Download latest price data
- Categorize stocks by movement
- Save data to `stock_movements_history.csv`
- Create `stock_details_YYYY-MM-DD.csv` with individual stock data

**Expected Output:**
```
Starting Daily Stock Movement Tracker...
Fetching Nifty 500 stock list...
Processing 500 stocks...
Processed 50/500 stocks...
...
DAILY MARKET MOVEMENT SUMMARY - 2024-XX-XX
========================================
📈 GAINERS:
  15%+      : 5 stocks
  10-15%    : 12 stocks
  5-10%     : 45 stocks
  3-5%      : 78 stocks
...
```

## 🎨 Interactive Dashboard (NEW!)

### Launch the Dashboard:

**Windows:** Double-click `run_dashboard.bat`

**Linux/Mac:**
```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

**Or manually:**
```bash
streamlit run dashboard.py
```

The dashboard automatically opens at: **http://localhost:8501**

### Dashboard Features:
- 📊 **Real-time KPI metrics** (gainers, losers, breadth, extremes)
- 📈 **Interactive charts** with zoom, pan, and hover details
- 🎯 **Market insights** with automatic sentiment analysis
- 📅 **Date range filters** for custom period analysis
- 🔄 **Auto-refresh option** for live monitoring
- 📥 **CSV export** for Excel analysis
- 📱 **Responsive design** - works on mobile too!

### Dashboard Tabs:
1. **Market Breadth** - Gainers vs Losers, Extreme movements
2. **Volatility** - Daily movers, Weekly patterns
3. **Trends** - Advance-Decline line, Distribution stacks
4. **Data Table** - Sortable table with download option

**See DASHBOARD_GUIDE.md for detailed usage instructions.**

### Step 4: Generate Visualizations

```bash
python visualize_trends.py
```

This creates:
- Dashboard PNG file with 6 charts
- Console output with insights and trends

## 📅 Automated Daily Execution

### Option A: Using the Built-in Scheduler (Recommended for Testing)

```bash
python scheduler.py
```

This runs the tracker daily at 4:00 PM IST (after market close).
- Modify `RUN_TIME` in `scheduler.py` to change execution time
- Keeps running in the background
- Press Ctrl+C to stop

### Option B: Windows Task Scheduler (Recommended for Production)

1. Open **Task Scheduler** (search in Start menu)
2. Click **"Create Basic Task"**
3. Name: "Stock Tracker Daily"
4. Trigger: **Daily** at 4:00 PM (16:00)
5. Action: **Start a program**
   - Program: `python`
   - Arguments: `C:\path\to\stock_tracker.py`
   - Start in: `C:\path\to\` (folder containing script)
6. Finish and enable

### Option C: Linux/Mac Cron Job

```bash
# Edit crontab
crontab -e

# Add this line (runs at 4:00 PM daily)
0 16 * * * cd /path/to/tracker && /usr/bin/python3 stock_tracker.py >> tracker.log 2>&1
```

Verify cron job:
```bash
crontab -l
```

## 📊 Understanding the Visualizations

The `visualize_trends.py` script generates 6 charts:

### 1. Market Breadth (Gainers vs Losers)
- Shows daily count of gaining vs losing stocks
- Helps identify bullish/bearish trends

### 2. Extreme Movements (15%+)
- Tracks stocks with extreme volatility
- Useful for identifying market panic or euphoria

### 3. Distribution Heatmap
- Visual distribution across all movement categories
- Darker colors = more stocks in that category

### 4. Advance-Decline Line
- Cumulative difference between gainers and losers
- Rising line = bullish trend, falling = bearish trend

### 5. Market Volatility
- Total stocks moving 3%+ daily
- Shows market activity levels
- Includes 5-day moving average

### 6. Weekly Pattern Analysis
- Average gainers/losers by day of week
- Identifies if certain days tend to be bullish/bearish

## 📈 Sample Insights Output

```
📈 MARKET INSIGHTS & TREND ANALYSIS
====================================
📅 Latest Data (2024-02-09):
   Gainers (3%+): 142 stocks
   Losers (3%+): 98 stocks
   Extreme gains (15%+): 3 stocks
   Extreme losses (15%+): 1 stocks

📊 5-Day Trend:
   Average gainers: 135.2 stocks/day
   Average losers: 102.4 stocks/day
   ✅ Bullish trend - More gainers than losers

🌊 Volatility Analysis:
   Average daily movers (3%+): 237.4 stocks
   Latest: 240 stocks
```

## 🗂️ Output Files

### Generated Each Run:

1. **stock_movements_history.csv** (Historical tracking)
   - Columns: date, up_15_plus, up_10_15, up_5_10, up_3_5, down_3_5, down_5_10, down_10_15, down_15_plus, neutral
   - Appends daily, updates if date exists

2. **stock_details_YYYY-MM-DD.csv** (Daily stock list)
   - Individual stocks with their exact percentage change
   - Useful for drilling down into specific stocks

3. **stock_movement_dashboard_YYYY-MM-DD.png** (Visualization)
   - High-resolution dashboard with all charts
   - Generated by visualize_trends.py

## ⚙️ Customization

### Change Stock Universe

Edit `stock_tracker.py` line ~30 to modify the stock list:

```python
# Use different index
url = "https://archives.nseindia.com/content/indices/ind_nifty50list.csv"

# Or manually define stocks
stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', ...]
```

### Modify Movement Categories

Edit the `_categorize_movement()` function in `stock_tracker.py`:

```python
def _categorize_movement(self, pct_change: float) -> str:
    if pct_change >= 20:  # Change threshold
        return 'up_20+'
    # Add more categories as needed
```

### Change Execution Time

In `scheduler.py`:
```python
RUN_TIME = "15:45"  # Run at 3:45 PM instead
```

## 🐛 Troubleshooting

### Issue: "No stocks processed"
- **Cause**: Network issues or Yahoo Finance API down
- **Solution**: Check internet connection, try again later, or use fallback stock list

### Issue: "Rate limit errors"
- **Cause**: Too many requests to Yahoo Finance
- **Solution**: Script includes automatic delays. If issues persist, reduce stock count

### Issue: "Module not found"
- **Cause**: Dependencies not installed
- **Solution**: Run `pip install -r requirements.txt`

### Issue: Charts not displaying
- **Cause**: Missing GUI backend for matplotlib
- **Solution**: 
  - Windows: Install matplotlib properly
  - Linux: `sudo apt-get install python3-tk`
  - Or save plots only (they're already saved as PNG)

## 📝 Best Practices

1. **Run after market hours**: Indian stock market closes at 3:30 PM IST. Schedule for 4:00 PM or later.

2. **Weekend handling**: Script will not fetch new data on weekends (market closed). This is normal.

3. **Data backup**: Keep `stock_movements_history.csv` backed up. It contains all your historical data.

4. **Monitor logs**: Check console output for errors, especially first few runs.

5. **Storage**: Daily CSV files can accumulate. Archive or delete old `stock_details_*.csv` files periodically.

## 📊 Use Cases

- **Day Traders**: Monitor daily volatility and market breadth
- **Swing Traders**: Identify trend changes using advance-decline line
- **Researchers**: Analyze market patterns and correlations
- **Portfolio Managers**: Track overall market health
- **Educators**: Demonstrate market dynamics with real data

## 🔮 Future Enhancements

Ideas for extending this project:

- [ ] Add sector-wise breakdown
- [ ] Integration with trading platforms (APIs)
- [ ] Email/SMS alerts for extreme market days
- [ ] Machine learning predictions based on patterns
- [ ] Real-time updates during market hours (websockets)
- [ ] Comparison with index movements (Nifty/Sensex correlation)
- [ ] Advanced filters in dashboard (sector, market cap)
- [ ] Historical backtesting features
- [ ] Mobile app version
- [ ] Multi-user support with portfolios

## 📄 License

Free to use and modify for personal or commercial purposes.

## 🤝 Contributing

Feel free to fork, modify, and improve! Some contribution ideas:
- Add more visualization types
- Improve error handling
- Add more data sources
- Create web interface
- Add backtesting features

## ⚠️ Disclaimer

This tool is for informational and educational purposes only. It is not financial advice. Always do your own research before making investment decisions. Stock market data may have delays or inaccuracies.

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Verify all dependencies are installed
4. Ensure Python 3.8+ is being used

---

**Happy Tracking! 📈📉**
