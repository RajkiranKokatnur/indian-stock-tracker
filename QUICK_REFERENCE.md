# 📋 Quick Reference Guide

## 🚀 Getting Started in 3 Steps

### Windows Users:
1. Double-click `run_tracker.bat`
2. Wait for completion
3. Check generated charts and CSV files

### Linux/Mac Users:
```bash
chmod +x run_tracker.sh
./run_tracker.sh
```

## 📊 Understanding the Output

### Console Output:
- **Gainers**: Stocks that moved up by 3%+, 5%+, 10%+, 15%+
- **Losers**: Stocks that moved down by -3%, -5%, -10%, -15%
- **Neutral**: Stocks between -3% and +3%
- **Market Breadth**: % of advancing stocks (>60% = bullish, <40% = bearish)

### Files Generated:
- `stock_movements_history.csv` - Historical database (keeps growing)
- `stock_details_YYYY-MM-DD.csv` - Today's individual stock data
- `stock_movement_dashboard_YYYY-MM-DD.png` - Visual charts

## 📈 Chart Interpretation

| Chart | What It Shows | How to Read |
|-------|---------------|-------------|
| **Market Breadth** | Green vs Red lines | Green > Red = Bullish market |
| **Extreme Movements** | 15%+ movers | Spikes = high volatility day |
| **Distribution Heatmap** | Category concentration | Darker = more stocks in that range |
| **Advance-Decline Line** | Cumulative trend | Rising = sustained bullish, Falling = sustained bearish |
| **Volatility** | Total movers | Higher bars = more volatile day |
| **Weekly Pattern** | Day-of-week trends | Shows which days tend to be bullish/bearish |

## ⚡ Common Commands

```bash
# Manual run (one time)
python stock_tracker.py

# View trends from existing data
python visualize_trends.py

# Start automated daily tracking
python scheduler.py

# Install dependencies
pip install -r requirements.txt

# Test with sample data
cp stock_movements_history_sample.csv stock_movements_history.csv
python visualize_trends.py
```

## 🎯 Key Metrics to Watch

### Bullish Signals:
- ✅ Gainers > Losers by 20%+
- ✅ Advance-Decline line trending up
- ✅ Low extreme losses (15%+ down)
- ✅ High extreme gains (15%+ up)

### Bearish Signals:
- ⚠️ Losers > Gainers by 20%+
- ⚠️ Advance-Decline line trending down
- ⚠️ High extreme losses
- ⚠️ Low extreme gains

### High Volatility Indicators:
- 🔥 Total movers (3%+) > 250 stocks
- 🔥 Extreme movers (15%+) > 10 stocks combined
- 🔥 Volatility chart shows spikes

### Neutral/Range-bound Market:
- ➡️ Gainers ≈ Losers (within 10%)
- ➡️ Advance-Decline line flat
- ➡️ Low extreme movements
- ➡️ High neutral count

## 🔧 Customization Quick Tips

### Change Stock List:
Edit `stock_tracker.py` line 24:
```python
# For Nifty 50 only
url = "https://archives.nseindia.com/content/indices/ind_nifty50list.csv"
```

### Change Categories:
Edit `stock_tracker.py` line 71-86 (thresholds)

### Change Run Time:
Edit `scheduler.py` line 32:
```python
RUN_TIME = "15:45"  # Your preferred time
```

## 📞 Troubleshooting

| Issue | Quick Fix |
|-------|-----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| "No data fetched" | Check internet connection |
| "Charts not showing" | Files are saved as PNG, check folder |
| "Permission denied" | Run as administrator (Windows) or use `sudo` (Linux) |
| Script runs but no output | Check if market is open (weekday, not holiday) |

## 💡 Pro Tips

1. **First Time Users**: Run with sample data first to see how it works
   ```bash
   cp stock_movements_history_sample.csv stock_movements_history.csv
   python visualize_trends.py
   ```

2. **Daily Tracking**: Use scheduler.py or Task Scheduler for hands-free operation

3. **Analysis**: Wait for 5-7 days of data for meaningful trend analysis

4. **Backup**: Keep `stock_movements_history.csv` backed up - it's your treasure!

5. **Market Hours**: Indian stock market: Mon-Fri, 9:15 AM - 3:30 PM IST
   - Schedule runs after 4:00 PM

6. **Holidays**: Script won't fetch data on weekends/holidays (this is normal)

## 🎓 Learning Resources

- **Market Breadth**: Measures market participation and strength
- **Advance-Decline Line**: Shows underlying market trend direction
- **Volatility**: Measures price movement intensity
- **Distribution**: Shows which movements are most common

## 📝 Maintenance

### Daily (Automated):
- Script runs and updates CSV
- No action needed if scheduler is set up

### Weekly:
- Review charts for trends
- Check for any error messages

### Monthly:
- Backup `stock_movements_history.csv`
- Archive old `stock_details_*.csv` files (optional)
- Review long-term trends

### As Needed:
- Update stock universe if tracking different stocks
- Adjust thresholds if market behavior changes
- Update dependencies: `pip install --upgrade yfinance pandas`

---

**Remember**: Markets are inherently unpredictable. Use this tool as one of many inputs for decision-making, not as the sole basis for investments.

**Good luck with your tracking! 📊🎯**
