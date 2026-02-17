# 🎯 Complete Indian Stock Movement Tracker - Project Overview

## 📦 What You Got

A complete, professional-grade stock market tracking and visualization system with **3 components**:

### 1. 📊 **Data Collection System**
- Automated daily tracking of Nifty 500 stocks
- Categorizes movements: ±3%, ±5%, ±10%, ±15%
- Stores historical data in CSV format
- Runs automatically via scheduler

### 2. 📈 **Static Visualization**
- 6 professional charts (PNG output)
- Market breadth, trends, volatility analysis
- Print-ready, high-resolution outputs
- Perfect for reports and presentations

### 3. 🎨 **Interactive Web Dashboard** ⭐ NEW
- **Real-time monitoring** in your browser
- **Live charts** with zoom, pan, hover details
- **Multiple views**: Overview, Trends, Volatility, Distribution
- **Auto-refresh** capability
- **Date filtering** for custom analysis
- **Mobile accessible**

---

## 🚀 Complete Setup (One-Time)

### Step 1: Install All Dependencies

```bash
pip install -r requirements.txt
```

This installs everything you need:
- `yfinance` - Stock data
- `pandas` - Data processing
- `matplotlib` - Static charts
- `seaborn` - Beautiful visualizations
- `plotly` - Interactive charts
- `streamlit` - Web dashboard
- `schedule` - Automation

### Step 2: Test with Sample Data

```bash
# Copy sample data
cp stock_movements_history_sample.csv stock_movements_history.csv

# Launch dashboard to see it in action
streamlit run dashboard.py
```

### Step 3: Start Collecting Real Data

```bash
# Run once manually
python stock_tracker.py

# Or set up automated daily tracking
python scheduler.py
```

---

## 💡 How to Use (Daily Workflow)

### Option A: Simple Daily Use

**Morning:**
```bash
streamlit run dashboard.py
```
Dashboard opens in browser at http://localhost:8501

**After Market Close (4 PM):**
```bash
python stock_tracker.py
```
Data updates automatically, refresh dashboard to see latest

**Done!** Monitor trends, analyze market sentiment, make informed decisions.

### Option B: Fully Automated

**One-time setup:**
```bash
python scheduler.py
# Runs tracker daily at 4 PM automatically
# Keep this running in background
```

**Daily:**
```bash
streamlit run dashboard.py
# Just launch dashboard whenever you want to view data
```

---

## 📊 Dashboard Features Explained

### 🎯 **Top Metrics Bar**

Shows key numbers at a glance:
- **Gainers**: Stocks up 3%+ (with breadth %)
- **Losers**: Stocks down 3%+ (with breadth %)
- **Extreme Gains**: 15%+ up (volatility indicator)
- **Extreme Losses**: 15%+ down (risk indicator)
- **Neutral**: Stocks between -3% and +3%

### 📑 **Tab 1: Overview**

**Market Breadth Chart**
- Green line = Gainers, Red line = Losers
- When green > red = Bullish market
- When red > green = Bearish market

**Extreme Movements Chart**
- Shows 15%+ movers daily
- Spikes = High volatility days

**Advance-Decline Line**
- Cumulative trend indicator
- Rising = Bullish trend
- Falling = Bearish trend

**Distribution Pie**
- Current day stock distribution
- Visual breakdown of all categories

### 📑 **Tab 2: Trends**

**5-Day Moving Averages**
- Smoothed trend lines
- Shows trend direction clearly

**Trend Metrics**
- Average gainers/losers
- Current trend status (Bullish/Bearish/Neutral)

### 📑 **Tab 3: Volatility**

**Volatility Gauge**
- Shows if market is calm or agitated
- Compares current to average

**Daily Volatility Chart**
- Total stocks moving 3%+ daily
- 5-day moving average overlay

### 📑 **Tab 4: Distribution**

**Heatmap**
- Visual density of movements
- Darker = more concentration

**Weekly Pattern**
- Which days tend to be bullish/bearish
- Useful for timing decisions

---

## 🎓 Quick Interpretation Guide

### 🟢 **Bullish Market Signs**

- Breadth > 60%
- Gainers consistently > Losers
- A/D line rising
- Few extreme losses (15%+ down)
- More extreme gains than losses

**What to do:** Consider long positions, ride the trend

### 🔴 **Bearish Market Signs**

- Breadth < 40%
- Losers consistently > Gainers
- A/D line falling
- Many extreme losses (15%+ down)
- Few extreme gains

**What to do:** Be cautious, consider shorts or cash

### ⚪ **Neutral/Choppy Market**

- Breadth 45-55%
- Gainers ≈ Losers
- A/D line flat or choppy
- Moderate volatility

**What to do:** Range trading, wait for clearer signals

### 🔥 **High Volatility Day**

- Total movers > 250 stocks
- Extreme movers (15%+) > 10 stocks
- Volatility gauge in red zone

**What to do:** Use wider stops, be defensive

---

## 📁 File Structure Explained

### **Generated Daily:**
- `stock_movements_history.csv` - Main database (keeps all history)
- `stock_details_YYYY-MM-DD.csv` - Individual stock breakdown
- `stock_movement_dashboard_YYYY-MM-DD.png` - Static chart export

### **Core Scripts:**
- `stock_tracker.py` - Data collector (run daily)
- `dashboard.py` - Interactive dashboard (keep running)
- `visualize_trends.py` - Static chart generator
- `scheduler.py` - Automation scheduler

### **Easy Launchers:**
- `run_tracker.bat` / `.sh` - One-click data collection
- `launch_dashboard.bat` / `.sh` - One-click dashboard

### **Configuration:**
- `requirements.txt` - All dependencies
- `config.ini` - Settings (optional customization)

### **Documentation:**
- `README.md` - Complete setup guide
- `DASHBOARD_GUIDE.md` - Dashboard usage
- `QUICK_REFERENCE.md` - Cheat sheet
- `PROJECT_OVERVIEW.md` - This file

---

## 🎯 Common Use Cases

### Use Case 1: Daily Monitoring
**User:** Active trader monitoring market health
**Workflow:**
1. Launch dashboard in morning
2. Enable auto-refresh
3. Monitor throughout day
4. Review after market close

### Use Case 2: Trend Analysis
**User:** Swing trader looking for trend changes
**Workflow:**
1. Open dashboard
2. Go to "Trends" tab
3. Check A/D line direction
4. Look for divergences
5. Make position decisions

### Use Case 3: Volatility Trading
**User:** Options trader seeking high volatility
**Workflow:**
1. Go to "Volatility" tab
2. Check gauge and chart
3. Filter for high volatility periods
4. Plan volatility strategies

### Use Case 4: Weekly Patterns
**User:** Researcher studying market patterns
**Workflow:**
1. Accumulate 30+ days of data
2. Go to "Distribution" tab
3. Analyze weekly patterns
4. Optimize entry/exit timing

### Use Case 5: Reporting
**User:** Portfolio manager creating reports
**Workflow:**
1. Run `python visualize_trends.py`
2. Get high-res PNG charts
3. Include in presentations
4. Export raw data from dashboard

---

## 🔧 Customization Examples

### Change Stock Universe

**Edit** `stock_tracker.py` line ~24:

```python
# For Nifty 50 only
url = "https://archives.nseindia.com/content/indices/ind_nifty50list.csv"

# For specific stocks
stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS']
```

### Change Movement Thresholds

**Edit** `stock_tracker.py` line ~71:

```python
if pct_change >= 20:  # Change from 15 to 20
    return 'up_20+'
```

### Change Dashboard Theme

**Edit** `dashboard.py` line ~17:

```python
st.set_page_config(
    ...
    initial_sidebar_state="collapsed"  # Start with sidebar closed
)
```

### Add Email Alerts (Future)

Add to `stock_tracker.py` after data collection:

```python
if latest['extreme_up'] + latest['extreme_down'] > 15:
    send_email_alert(subject="High Volatility Alert!")
```

---

## 🎯 Best Practices

### 1. **Data Collection**
✅ Run tracker after 4 PM IST (market close)
✅ Keep `stock_movements_history.csv` backed up
✅ Archive old `stock_details_*.csv` weekly
❌ Don't run during market hours (data incomplete)

### 2. **Dashboard Usage**
✅ Launch in morning, keep running all day
✅ Use date filters for specific period analysis
✅ Export charts when needed (hover → camera icon)
❌ Don't keep auto-refresh on if not monitoring

### 3. **Analysis**
✅ Wait for 7+ days before drawing conclusions
✅ Compare with actual index movements
✅ Use multiple timeframes (daily, weekly)
✅ Track long-term A/D line trends
❌ Don't make decisions on single day data

### 4. **Performance**
✅ Close unused browser tabs
✅ Restart dashboard weekly
✅ Use date range filter for faster loading
❌ Don't track too many stocks (stick to 500 max)

---

## 🚀 Advanced Tips

### Tip 1: Multi-Monitor Setup
- Dashboard on one screen
- Trading platform on another
- Correlate movements in real-time

### Tip 2: Mobile Monitoring
```bash
streamlit run dashboard.py --server.address 0.0.0.0
# Access from phone: http://your-ip:8501
```

### Tip 3: Cloud Deployment
- Deploy to Streamlit Cloud (free)
- Access from anywhere
- Always running, auto-updating

### Tip 4: Data Export
- Click "View Raw Data" in dashboard
- Copy/paste to Excel
- Perform custom analysis

### Tip 5: Correlation Studies
- Export historical data
- Correlate with index movements
- Find leading indicators

---

## 📈 Roadmap (Potential Future Features)

### Short-term
- [ ] Email/SMS alerts for extreme days
- [ ] Sector-wise breakdown
- [ ] Index overlay charts
- [ ] Comparison with Nifty/Sensex

### Medium-term
- [ ] Machine learning predictions
- [ ] Real-time intraday updates
- [ ] Trading platform integration
- [ ] Portfolio correlation analysis

### Long-term
- [ ] Multi-market support (US, UK, etc.)
- [ ] Social sentiment integration
- [ ] Backtesting engine
- [ ] Mobile app

---

## ❓ FAQ

**Q: Do I need to keep the dashboard running all the time?**
A: No, launch it when you want to view data. Data collection and dashboard are separate.

**Q: Can I track different stocks?**
A: Yes, edit `stock_tracker.py` to change the stock list.

**Q: How much historical data do I need?**
A: Minimum 7 days for trends, 30+ days for meaningful patterns.

**Q: Will this work on Windows/Mac/Linux?**
A: Yes, Python works on all platforms. Use `.bat` on Windows, `.sh` on Mac/Linux.

**Q: Is the data real-time?**
A: Yahoo Finance has ~15-20 min delay. Good enough for daily tracking.

**Q: Can I share the dashboard with my team?**
A: Yes, use network mode or deploy to cloud.

**Q: Does it cost anything?**
A: Completely free. All tools and data sources are free.

---

## 🎯 Success Stories (Hypothetical Use Cases)

### Case 1: Catching the Trend Change
Trader noticed A/D line diverging from index for 5 days. Adjusted positions before reversal. Avoided 8% drawdown.

### Case 2: Volatility Spike Trading
Options trader used volatility gauge to identify IV expansion days. Profited from premium selling.

### Case 3: Weekly Pattern Edge
Researcher found Mondays tend to be bearish, Fridays bullish. Adjusted entry timing, improved win rate by 12%.

### Case 4: Risk Management
PM noticed extreme losses spiking. Reduced exposure 2 days before market correction. Protected capital.

---

## 📞 Support & Community

### Getting Help
1. Check `QUICK_REFERENCE.md` for common tasks
2. Review `DASHBOARD_GUIDE.md` for dashboard issues
3. Check Troubleshooting sections in README

### Contributing Ideas
- Found a bug? Note it down
- Have a feature idea? Sketch it out
- Made an improvement? Document it

### Sharing
- Share charts on social media
- Write about your findings
- Help others learn the system

---

## 🎓 Learning Path

### Week 1: Setup & Basics
- [ ] Install all dependencies
- [ ] Run tracker manually once
- [ ] Launch dashboard, explore all tabs
- [ ] Understand key metrics

### Week 2: Daily Monitoring
- [ ] Set up automated tracking
- [ ] Monitor daily after market close
- [ ] Start recognizing patterns
- [ ] Compare with market news

### Week 3: Analysis
- [ ] Use date filters for period analysis
- [ ] Study A/D line patterns
- [ ] Track volatility trends
- [ ] Identify bullish/bearish signals

### Week 4: Application
- [ ] Use insights for decision making
- [ ] Track your predictions
- [ ] Refine your interpretation
- [ ] Build your own strategies

---

## 🌟 Final Words

You now have a **professional-grade market analysis tool** that:

✅ Automatically tracks 500 stocks daily
✅ Provides beautiful interactive visualizations
✅ Offers comprehensive trend analysis
✅ Is completely free and customizable
✅ Works on any platform
✅ Requires minimal maintenance

**The tool is built. Now it's up to you to use it wisely.**

Remember:
- Data informs, but you decide
- Trends help, but markets change
- Tools assist, but discipline wins

**May your trades be profitable and your losses small! 📊🎯🚀**

---

*Built with Python, Streamlit, Plotly, and a passion for market analysis.*
