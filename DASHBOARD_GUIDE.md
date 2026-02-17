# 🎨 Interactive Dashboard Guide

## 🚀 Quick Start

### Launch the Dashboard

```bash
streamlit run dashboard.py
```

Dashboard opens automatically at **http://localhost:8501**

### First Time? Use Sample Data

```bash
cp stock_movements_history_sample.csv stock_movements_history.csv
streamlit run dashboard.py
```

## ✨ Dashboard Features

### 📊 Top Metrics Bar
- **Gainers/Losers**: Stocks moving 3%+ with market breadth %
- **Extreme Movements**: 15%+ up/down (volatility indicator)
- **Neutral Stocks**: Between -3% and +3%
- **Market Trend**: 5-day trend direction

### 📈 Four Interactive Tabs

**1. Overview** - Main market health indicators
**2. Trends** - Historical trend analysis with moving averages
**3. Volatility** - Market volatility gauge and charts
**4. Distribution** - Heatmaps and weekly patterns

### 🎛️ Interactive Controls
- Date range selector (sidebar)
- Auto-refresh toggle (30-second intervals)
- Manual refresh button
- Expandable raw data table

## 📊 Chart Interpretations

### Market Breadth (Green vs Red Lines)
- **Green > Red** = Bullish (>60% = strong)
- **Red > Green** = Bearish (<40% = strong)
- **Close together** = Neutral/choppy

### Advance-Decline Line
- **Rising** = Sustained bullish trend
- **Falling** = Sustained bearish trend
- **Divergence from index** = Potential reversal

### Volatility Gauge
- **Green zone** = Low volatility
- **Gray zone** = Normal
- **Red zone** = High volatility (>30% above average)

### Extreme Movements Chart
- Spikes indicate panic (red) or euphoria (green)
- Multiple spikes = highly volatile period

## 🎯 How to Use Daily

### Morning Routine
```bash
# Start the dashboard
streamlit run dashboard.py
```

### After Market Close (4 PM IST)
```bash
# Run tracker in another terminal
python stock_tracker.py

# Dashboard auto-updates or click refresh button
```

### Continuous Monitoring
- Enable "Auto-refresh" in sidebar
- Dashboard updates every 30 seconds
- Keep browser tab open

## 💡 Pro Tips

1. **Export Charts**: Hover over any chart → click camera icon
2. **Mobile Access**: Use network URL on your phone
3. **Multiple Timeframes**: Adjust date range for different views
4. **Watch A/D Line**: Best indicator for trend changes
5. **Weekly Patterns**: Use for entry/exit timing

## 🔧 Advanced Usage

### Run on Custom Port
```bash
streamlit run dashboard.py --server.port 8080
```

### Network Access (Access from other devices)
```bash
streamlit run dashboard.py --server.address 0.0.0.0
# Access via: http://YOUR_IP:8501
```

### Background Mode (Linux/Mac)
```bash
nohup streamlit run dashboard.py > dashboard.log 2>&1 &
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "No data found" | Run `python stock_tracker.py` or use sample data |
| Dashboard won't start | Install: `pip install streamlit plotly` |
| Charts not updating | Click refresh button or check CSV file |
| Port already in use | Use different port: `--server.port 8502` |
| Slow performance | Reduce date range or disable auto-refresh |

## 📊 What to Watch

### Daily Checklist
- [ ] Market breadth % (>60% bullish, <40% bearish)
- [ ] Extreme movers count (>10 = high volatility)
- [ ] 5-day trend direction
- [ ] A/D line direction

### Bullish Signals
✅ Breadth > 60%
✅ A/D line rising
✅ More extreme gains than losses
✅ Gainers increasing daily

### Bearish Signals
⚠️ Breadth < 40%
⚠️ A/D line falling
⚠️ More extreme losses than gains
⚠️ Losers increasing daily

## 🎓 Learning Mode

### Week 1: Understanding Basics
- Focus on market breadth chart
- Learn to read sentiment indicators
- Compare with actual market indices

### Week 2: Trend Analysis
- Watch A/D line patterns
- Study 5-day moving averages
- Identify trend changes

### Week 3: Volatility Mastery
- Monitor volatility gauge
- Study extreme movement patterns
- Correlate with market events

### Week 4: Pattern Recognition
- Analyze weekly patterns
- Study distribution heatmap
- Develop trading insights

## 🚀 Next Level Features

### Customize Dashboard
Edit `dashboard.py` to add:
- Custom metrics
- Additional charts
- Alert thresholds
- Email notifications (future)

### Data Analysis
- Export raw data from expandable table
- Create custom analysis in Excel
- Build correlation studies
- Backtest strategies

### Integration Ideas
- Connect to trading platform
- Add news feed integration
- Include sector breakdown
- Add index overlay charts

## 📱 Mobile Access

1. Find your computer's IP address
   ```bash
   # Windows: ipconfig
   # Mac/Linux: ifconfig
   ```

2. Run with network access
   ```bash
   streamlit run dashboard.py --server.address 0.0.0.0
   ```

3. On phone, open browser to: `http://YOUR_IP:8501`

## ⚡ Performance Tips

- **Filter date range** for faster loading
- **Disable auto-refresh** when not monitoring
- **Close unused tabs** in browser
- **Restart dashboard** once a week
- **Archive old data** periodically

## 🎯 Dashboard Best Practices

1. **Keep it running** - Start in morning, stop at night
2. **Monitor daily** - Check after market close
3. **Track trends** - Don't focus on single day
4. **Compare periods** - Use date range selector
5. **Trust the data** - Let numbers guide decisions

---

**Remember**: The dashboard is a tool for insight, not a crystal ball. Use it alongside other analysis methods!

**Happy Trading! 📊🎯**
