"""
Interactive Stock Movement Dashboard
Real-time monitoring with Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os
from pathlib import Path

# Import market intelligence module
try:
    from market_intelligence import MarketIntelligence
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False
    st.warning("⚠️ Analytics module not found. Some features will be limited.")

# Page configuration
st.set_page_config(
    page_title="Indian Stock Movement Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

class DashboardData:
    def __init__(self, data_file='stock_movements_history.csv', sector_file='sector_movements_history.csv'):
        self.data_file = data_file
        self.sector_file = sector_file
        self.df = None
        self.sector_df = None
        
    def load_data(self):
        """Load historical data with full error handling and column validation"""
        if not os.path.exists(self.data_file):
            return None
        
        try:
            df = pd.read_csv(self.data_file)
            
            # Empty file
            if df.empty or len(df.columns) == 0:
                return None
            
            # Auto-fix: rename first column to 'date' if it contains date-like values
            if 'date' not in df.columns:
                first_col = df.columns[0]
                try:
                    pd.to_datetime(df[first_col].iloc[0])
                    df = df.rename(columns={first_col: 'date'})
                except:
                    return None
            
            # Required movement columns
            required_cols = ['up_15_plus', 'up_10_15', 'up_5_10', 'up_3_5',
                           'down_3_5', 'down_5_10', 'down_10_15', 'down_15_plus']
            
            # Fill any missing movement columns with 0
            for col in required_cols:
                if col not in df.columns:
                    df[col] = 0
            
            # Fill neutral if missing
            if 'neutral' not in df.columns:
                df['neutral'] = 0
            
            # Convert date column
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Drop rows where date conversion failed
            df = df.dropna(subset=['date'])
            
            # Convert numeric columns
            for col in required_cols + ['neutral']:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
            # Sort by date
            df = df.sort_values('date').reset_index(drop=True)
            
            return df if len(df) > 0 else None
            
        except Exception as e:
            st.error(f"❌ Error loading data: {e}")
            st.info("💡 Run `python stock_tracker_with_sectors.py` to collect fresh data.")
            return None
    
    def load_sector_data(self):
        """Load sector historical data with full error handling"""
        if not os.path.exists(self.sector_file):
            return None
        
        try:
            sector_df = pd.read_csv(self.sector_file)
            
            if sector_df.empty or len(sector_df.columns) == 0:
                return None
            
            # Auto-fix: rename first column to 'date' if needed
            if 'date' not in sector_df.columns:
                first_col = sector_df.columns[0]
                try:
                    pd.to_datetime(sector_df[first_col].iloc[0])
                    sector_df = sector_df.rename(columns={first_col: 'date'})
                except:
                    return None
            
            sector_df['date'] = pd.to_datetime(sector_df['date'], errors='coerce')
            sector_df = sector_df.dropna(subset=['date'])
            
            # Fill missing numeric columns with 0
            for col in ['up_3_plus', 'down_3_plus', 'neutral', 'total', 'breadth']:
                if col not in sector_df.columns:
                    sector_df[col] = 0
                sector_df[col] = pd.to_numeric(sector_df[col], errors='coerce').fillna(0)
            
            sector_df = sector_df.sort_values('date').reset_index(drop=True)
            
            return sector_df if len(sector_df) > 0 else None
            
        except Exception as e:
            return None
    
    def get_latest_stats(self, df):
        """Get latest day statistics"""
        if df is None or len(df) == 0:
            return None
        
        latest = df.iloc[-1]
        
        gainers = latest['up_3_5'] + latest['up_5_10'] + latest['up_10_15'] + latest['up_15_plus']
        losers = latest['down_3_5'] + latest['down_5_10'] + latest['down_10_15'] + latest['down_15_plus']
        total_movers = gainers + losers
        
        return {
            'date': latest['date'],
            'gainers': int(gainers),
            'losers': int(losers),
            'extreme_up': int(latest['up_15_plus']),
            'extreme_down': int(latest['down_15_plus']),
            'neutral': int(latest['neutral']),
            'total_movers': int(total_movers),
            'breadth': (gainers / total_movers * 100) if total_movers > 0 else 50
        }
    
    def get_trend_stats(self, df, days=5):
        """Get trend statistics for last N days"""
        if df is None or len(df) < days:
            return None
        
        recent = df.tail(days)
        
        gainers = (recent['up_3_5'] + recent['up_5_10'] + 
                  recent['up_10_15'] + recent['up_15_plus']).mean()
        losers = (recent['down_3_5'] + recent['down_5_10'] + 
                 recent['down_10_15'] + recent['down_15_plus']).mean()
        
        return {
            'avg_gainers': gainers,
            'avg_losers': losers,
            'trend': 'Bullish' if gainers > losers * 1.2 else 'Bearish' if losers > gainers * 1.2 else 'Neutral'
        }

def create_market_breadth_chart(df):
    """Create interactive market breadth chart"""
    gainers = df['up_3_5'] + df['up_5_10'] + df['up_10_15'] + df['up_15_plus']
    losers = df['down_3_5'] + df['down_5_10'] + df['down_10_15'] + df['down_15_plus']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=gainers,
        name='Gainers (3%+)',
        mode='lines+markers',
        line=dict(color='green', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'], y=losers,
        name='Losers (3%+)',
        mode='lines+markers',
        line=dict(color='red', width=3),
        fill='tozeroy',
        fillcolor='rgba(255, 0, 0, 0.2)'
    ))
    
    fig.update_layout(
        title='Market Breadth: Gainers vs Losers Over Time',
        xaxis_title='Date',
        yaxis_title='Number of Stocks',
        hovermode='x unified',
        legend=dict(x=0.01, y=0.99),
        height=400
    )
    
    return fig

def create_extreme_movements_chart(df):
    """Create extreme movements chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['date'], 
        y=df['up_15_plus'],
        name='Up 15%+',
        marker_color='darkgreen'
    ))
    
    fig.add_trace(go.Bar(
        x=df['date'], 
        y=-df['down_15_plus'],
        name='Down 15%+',
        marker_color='darkred'
    ))
    
    fig.update_layout(
        title='Extreme Movements (±15%)',
        xaxis_title='Date',
        yaxis_title='Number of Stocks',
        hovermode='x unified',
        height=400,
        barmode='relative'
    )
    
    return fig

def create_volatility_gauge(total_movers, avg_movers):
    """Create volatility gauge"""
    volatility_pct = (total_movers / avg_movers * 100) if avg_movers > 0 else 100
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=total_movers,
        delta={'reference': avg_movers, 'suffix': ' vs avg'},
        title={'text': "Daily Volatility<br>(Stocks Moving 3%+)"},
        gauge={
            'axis': {'range': [0, max(500, total_movers * 1.5)]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, avg_movers * 0.8], 'color': "lightgray"},
                {'range': [avg_movers * 0.8, avg_movers * 1.2], 'color': "gray"},
                {'range': [avg_movers * 1.2, max(500, total_movers * 1.5)], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': avg_movers * 1.3
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_advance_decline_chart(df):
    """Create cumulative advance-decline line"""
    gainers = df['up_3_5'] + df['up_5_10'] + df['up_10_15'] + df['up_15_plus']
    losers = df['down_3_5'] + df['down_5_10'] + df['down_10_15'] + df['down_15_plus']
    
    daily_diff = gainers - losers
    cumulative = daily_diff.cumsum()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=cumulative,
        mode='lines',
        name='A/D Line',
        line=dict(color='blue', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 0, 255, 0.1)'
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)
    
    fig.update_layout(
        title='Cumulative Advance-Decline Line',
        xaxis_title='Date',
        yaxis_title='Cumulative Difference',
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_distribution_pie(latest_data):
    """Create distribution pie chart for latest day (excluding neutral)"""
    categories = {
        'Up 15%+': latest_data['up_15_plus'],
        'Up 10-15%': latest_data['up_10_15'],
        'Up 5-10%': latest_data['up_5_10'],
        'Up 3-5%': latest_data['up_3_5'],
        'Down 3-5%': latest_data['down_3_5'],
        'Down 5-10%': latest_data['down_5_10'],
        'Down 10-15%': latest_data['down_10_15'],
        'Down 15%+': latest_data['down_15_plus']
    }
    
    colors = ['#006400', '#228B22', '#90EE90', '#98FB98',
              '#FFB6C1', '#FF69B4', '#DC143C', '#8B0000']
    
    fig = go.Figure(data=[go.Pie(
        labels=list(categories.keys()),
        values=list(categories.values()),
        hole=.4,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='auto'
    )])
    
    fig.update_layout(
        title=f'Stock Distribution - {latest_data["date"].strftime("%Y-%m-%d")} (Excluding Neutral)',
        height=400
    )
    
    return fig

def create_heatmap(df):
    """Create category heatmap with RAG color scheme (excluding neutral)"""
    categories = ['up_15_plus', 'up_10_15', 'up_5_10', 'up_3_5', 
                 'down_3_5', 'down_5_10', 'down_10_15', 'down_15_plus']
    
    labels = ['↑15%+', '↑10-15%', '↑5-10%', '↑3-5%', 
             '↓3-5%', '↓5-10%', '↓10-15%', '↓15%+']
    
    heatmap_data = df[categories].T.values
    
    # Custom RAG colorscale for 8 categories (no neutral)
    custom_colorscale = [
        [0.0, '#8B0000'],    # Dark Red (↓15%+ - Most bearish)
        [0.143, '#DC143C'],  # Crimson Red (↓10-15%)
        [0.286, '#FF6347'],  # Tomato Red (↓5-10%)
        [0.429, '#FFA500'],  # Orange/Amber (↓3-5%)
        [0.571, '#ADFF2F'],  # Yellow-Green (↑3-5%)
        [0.714, '#7FFF00'],  # Chartreuse (↑5-10%)
        [0.857, '#32CD32'],  # Lime Green (↑10-15%)
        [1.0, '#006400']     # Dark Green (↑15%+ - Most bullish)
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=df['date'].dt.strftime('%Y-%m-%d'),
        y=labels,
        colorscale=custom_colorscale,
        reversescale=True,  # Reverse so dark green is at top (up movements)
        text=heatmap_data,
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Stock Count")
    ))
    
    fig.update_layout(
        title='Movement Distribution Heatmap (🟢 Bullish → 🔴 Bearish, Neutral Excluded)',
        xaxis_title='Date',
        yaxis_title='Category',
        height=400
    )
    
    return fig

def create_sector_heatmap(sector_df):
    """Create sector performance heatmap"""
    if sector_df is None or len(sector_df) == 0:
        return None
    
    # Pivot data: sectors as rows, dates as columns, breadth as values
    pivot_data = sector_df.pivot(index='sector', columns='date', values='breadth')
    
    # Sort sectors by average breadth
    pivot_data['avg'] = pivot_data.mean(axis=1)
    pivot_data = pivot_data.sort_values('avg', ascending=False)
    pivot_data = pivot_data.drop('avg', axis=1)
    
    # Custom colorscale for breadth (0-100%)
    breadth_colorscale = [
        [0.0, '#8B0000'],    # Dark Red (0% - all stocks down)
        [0.2, '#DC143C'],    # Crimson Red
        [0.35, '#FF6347'],   # Tomato Red
        [0.45, '#FFA500'],   # Orange/Amber
        [0.5, '#FFD700'],    # Gold (50% - neutral)
        [0.55, '#ADFF2F'],   # Yellow-Green
        [0.65, '#7FFF00'],   # Chartreuse
        [0.8, '#32CD32'],    # Lime Green
        [1.0, '#006400']     # Dark Green (100% - all stocks up)
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=[d.strftime('%Y-%m-%d') for d in pivot_data.columns],
        y=pivot_data.index,
        colorscale=breadth_colorscale,
        zmid=50,  # Center at 50% breadth
        text=pivot_data.values,
        texttemplate='%{text:.0f}%',
        textfont={"size": 9},
        colorbar=dict(title="Breadth %", ticksuffix="%"),
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Sector Performance Heatmap (% of Stocks Up 3%+ in Each Sector)',
        xaxis_title='Date',
        yaxis_title='Sector/Industry',
        height=600,
        yaxis=dict(tickfont=dict(size=10))
    )
    
    return fig

def get_sector_momentum_emoji(breadth):
    """Convert breadth percentage to emoji"""
    if breadth >= 70:
        return '🟢'
    elif breadth >= 55:
        return '🟡'
    else:
        return '🔴'

def create_sector_insights(sector_df):
    """Create sector rotation and momentum insights"""
    if sector_df is None or len(sector_df) == 0:
        return None
    
    # Get unique dates sorted
    dates = sorted(sector_df['date'].unique())
    
    if len(dates) < 2:
        return None
    
    insights = {
        'momentum_patterns': [],
        'rotations': []
    }
    
    # Get all sectors
    sectors = sector_df['sector'].unique()
    
    # Momentum patterns (last 7 days if available)
    recent_dates = dates[-7:] if len(dates) >= 7 else dates
    
    for sector in sectors:
        sector_data = sector_df[sector_df['sector'] == sector]
        sector_data = sector_data[sector_data['date'].isin(recent_dates)]
        sector_data = sector_data.sort_values('date')
        
        if len(sector_data) >= 3:
            pattern = ''.join([get_sector_momentum_emoji(b) for b in sector_data['breadth'].values])
            avg_breadth = sector_data['breadth'].mean()
            
            insights['momentum_patterns'].append({
                'sector': sector,
                'pattern': pattern,
                'avg_breadth': avg_breadth,
                'days': len(sector_data)
            })
    
    # Sort by average breadth
    insights['momentum_patterns'].sort(key=lambda x: x['avg_breadth'], reverse=True)
    
    # Rotation analysis (compare last 5 days vs previous 5 days)
    if len(dates) >= 10:
        mid_point = len(dates) - 5
        week1_dates = dates[mid_point-5:mid_point]
        week2_dates = dates[mid_point:]
        
        for sector in sectors:
            sector_data = sector_df[sector_df['sector'] == sector]
            
            week1_data = sector_data[sector_data['date'].isin(week1_dates)]
            week2_data = sector_data[sector_data['date'].isin(week2_dates)]
            
            if len(week1_data) >= 3 and len(week2_data) >= 3:
                week1_avg = week1_data['breadth'].mean()
                week2_avg = week2_data['breadth'].mean()
                change = week2_avg - week1_avg
                
                insights['rotations'].append({
                    'sector': sector,
                    'week1_avg': week1_avg,
                    'week2_avg': week2_avg,
                    'change': change,
                    'week1_emoji': get_sector_momentum_emoji(week1_avg),
                    'week2_emoji': get_sector_momentum_emoji(week2_avg)
                })
        
        # Sort by biggest changes
        insights['rotations'].sort(key=lambda x: abs(x['change']), reverse=True)
    
    return insights

def main():
    # Header
    st.title("📊 Indian Stock Movement Dashboard")
    st.markdown("Real-time monitoring of daily stock movements across NSE")
    
    # Initialize data loader
    data_loader = DashboardData()
    
    # Sidebar
    st.sidebar.header("⚙️ Settings")
    
    # Data refresh button
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
    
    # Load data
    df = data_loader.load_data()
    sector_df = data_loader.load_sector_data()
    
    if df is None or len(df) == 0:
        st.error("📂 No data found! Please run `stock_tracker.py` first to collect data.")
        st.info("💡 Or use the sample data file to test the dashboard.")
        st.code("cp stock_movements_history_sample.csv stock_movements_history.csv")
        return
    
    # Date range filter
    st.sidebar.subheader("📅 Date Range")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select date range:",
        value=(max(min_date, max_date - timedelta(days=30)), max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data by date range
    if len(date_range) == 2:
        mask = (df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])
        df_filtered = df[mask].copy()
    else:
        df_filtered = df.copy()
    
    # Get statistics
    latest_stats = data_loader.get_latest_stats(df)
    trend_stats = data_loader.get_trend_stats(df)
    
    # Display last update time
    st.sidebar.markdown("---")
    st.sidebar.info(f"📅 **Latest Data:** {latest_stats['date'].strftime('%Y-%m-%d')}")
    st.sidebar.info(f"📊 **Total Days:** {len(df)}")
    
    # Auto-refresh toggle
    st.sidebar.markdown("---")
    auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)")
    if auto_refresh:
        import time
        time.sleep(30)
        st.rerun()
    
    # Main dashboard layout
    st.markdown("---")
    
    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="📈 Gainers (3%+)",
            value=latest_stats['gainers'],
            delta=f"{latest_stats['breadth']:.1f}% breadth"
        )
    
    with col2:
        st.metric(
            label="📉 Losers (3%+)",
            value=latest_stats['losers'],
            delta=f"{100-latest_stats['breadth']:.1f}% breadth"
        )
    
    with col3:
        st.metric(
            label="🚀 Extreme Gains (15%+)",
            value=latest_stats['extreme_up'],
            delta="High volatility" if latest_stats['extreme_up'] > 5 else None
        )
    
    with col4:
        st.metric(
            label="⚠️ Extreme Losses (15%+)",
            value=latest_stats['extreme_down'],
            delta="High volatility" if latest_stats['extreme_down'] > 5 else None
        )
    
    with col5:
        st.metric(
            label="➡️ Neutral",
            value=latest_stats['neutral'],
            delta=trend_stats['trend'] if trend_stats else None
        )
    
    st.markdown("---")
    
    # Market sentiment indicator
    breadth = latest_stats['breadth']
    if breadth > 60:
        sentiment = "🟢 **Strong Bullish**"
        color = "green"
    elif breadth > 52:
        sentiment = "🟡 **Slightly Bullish**"
        color = "orange"
    elif breadth < 40:
        sentiment = "🔴 **Strong Bearish**"
        color = "red"
    elif breadth < 48:
        sentiment = "🟠 **Slightly Bearish**"
        color = "orange"
    else:
        sentiment = "⚪ **Neutral**"
        color = "gray"
    
    st.markdown(f"### Market Sentiment: {sentiment}")
    
    # Market Intelligence Section
    if ANALYTICS_AVAILABLE and len(df) >= 5:
        st.markdown("---")
        st.subheader("🎯 Market Intelligence Center")
        
        intel = MarketIntelligence(df, sector_df)
        
        # Market Score
        market_score = intel.calculate_market_score()
        if market_score:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Market Score", f"{market_score['overall']:.0f}/100")
                st.progress(int(market_score['overall']) / 100)
            
            with col2:
                st.metric("Breadth Score", f"{market_score['breadth_score']:.0f}/100")
            
            with col3:
                st.metric("Momentum", f"{market_score['momentum']:.0f}/100")
            
            with col4:
                st.metric("Volatility", f"{market_score['volatility']:.0f}/100")
            
            regime = market_score['regime']
            st.success(f"**{regime['emoji']} {regime['name']}**: {regime['description']}")
        
        # Statistical Context
        stats = intel.get_statistical_context()
        if stats:
            st.markdown("---")
            st.markdown("### 📊 Statistical Context")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Breadth", f"{stats['current']:.1f}%")
            
            with col2:
                st.metric("Historical Avg", f"{stats['mean']:.1f}%",
                         delta=f"{stats['current']-stats['mean']:+.1f}%")
            
            with col3:
                st.metric("Percentile", f"{stats['percentile']:.0f}th")
            
            with col4:
                st.metric("Z-Score", f"{stats['z_score']:.2f}")
            
            st.info(f"{stats['color']} **{stats['interpretation']}**")
        
        # Prediction
        prediction = intel.predict_next_breadth()
        if prediction:
            st.markdown("---")
            st.markdown("### 🔮 Tomorrow's Forecast")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Predicted Breadth", 
                         f"{prediction['prediction']:.1f}%")
            
            with col2:
                st.metric("Confidence", f"{prediction['confidence']:.0f}%")
            
            with col3:
                st.metric("Range", 
                         f"{prediction['range_low']:.1f}% - {prediction['range_high']:.1f}%")
            
            st.caption(f"Trend: {prediction['trend']}")
        
        # Divergence Alert
        divergence = intel.detect_divergences()
        if divergence:
            st.markdown("---")
            st.warning(f"""
            **⚠️ {divergence['type']}** (Severity: {divergence['severity']})
            
            {divergence['description']}
            
            **Recommended Action:** {divergence['action']}
            """)
    
    # Main charts
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Trends", "🔥 Volatility", "📅 Distribution", "🎯 Signals"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_extreme_movements_chart(df_filtered), use_container_width=True, key="extreme_overview")
        
        with col2:
            st.plotly_chart(create_distribution_pie(df.iloc[-1]), use_container_width=True, key="pie_overview")
    
    with tab2:
        # Trend analysis
        if trend_stats:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("5-Day Avg Gainers", f"{trend_stats['avg_gainers']:.0f}")
            with col2:
                st.metric("5-Day Avg Losers", f"{trend_stats['avg_losers']:.0f}")
            with col3:
                trend_color = "🟢" if trend_stats['trend'] == 'Bullish' else "🔴" if trend_stats['trend'] == 'Bearish' else "⚪"
                st.metric("5-Day Trend", f"{trend_color} {trend_stats['trend']}")
        
        # Moving average trends
        gainers_series = df_filtered['up_3_5'] + df_filtered['up_5_10'] + df_filtered['up_10_15'] + df_filtered['up_15_plus']
        losers_series = df_filtered['down_3_5'] + df_filtered['down_5_10'] + df_filtered['down_10_15'] + df_filtered['down_15_plus']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_filtered['date'], y=gainers_series.rolling(5).mean(), 
                                name='Gainers (5-day MA)', line=dict(color='green', width=3)))
        fig.add_trace(go.Scatter(x=df_filtered['date'], y=losers_series.rolling(5).mean(), 
                                name='Losers (5-day MA)', line=dict(color='red', width=3)))
        fig.update_layout(title='5-Day Moving Average: Gainers vs Losers', height=400)
        st.plotly_chart(fig, use_container_width=True, key="ma_trends")
    
    with tab3:
        st.header("🔄 Sector Rotation & Momentum Analysis")
        
        if sector_df is not None and len(sector_df) > 0:
            # Filter sector data by date range
            if len(date_range) == 2:
                mask = (sector_df['date'].dt.date >= date_range[0]) & (sector_df['date'].dt.date <= date_range[1])
                sector_df_filtered = sector_df[mask].copy()
            else:
                sector_df_filtered = sector_df.copy()
            
            if len(sector_df_filtered) > 0:
                # Sector Performance Heatmap
                st.subheader("📊 Sector Performance Heatmap")
                sector_heatmap = create_sector_heatmap(sector_df_filtered)
                if sector_heatmap:
                    st.plotly_chart(sector_heatmap, use_container_width=True, key="sector_heatmap_rotation")
                
                st.markdown("---")
                
                # Get sector insights
                insights = create_sector_insights(sector_df_filtered)
                
                if insights:
                    # Momentum patterns
                    st.subheader("🎯 Sector Momentum Patterns")
                    st.markdown("**Recent performance (🟢 Bullish | 🟡 Neutral | 🔴 Bearish)**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 💪 Strongest Sectors")
                        for item in insights['momentum_patterns'][:10]:
                            st.markdown(f"`{item['sector']:<20}` {item['pattern']} **({item['avg_breadth']:.0f}%)**")
                    
                    with col2:
                        st.markdown("### ⚠️ Weakest Sectors")
                        for item in insights['momentum_patterns'][-10:]:
                            st.markdown(f"`{item['sector']:<20}` {item['pattern']} **({item['avg_breadth']:.0f}%)**")
                    
                    st.markdown("---")
                    
                    # Rotation analysis
                    if insights['rotations']:
                        st.subheader("🔄 Sector Rotation Analysis")
                        st.markdown("**Week 1 vs Week 2 Comparison (Last 10 Days)**")
                        
                        # Show biggest rotations
                        rotation_data = []
                        for rot in insights['rotations'][:15]:
                            direction = "📈" if rot['change'] > 0 else "📉"
                            rotation_data.append({
                                'Sector': rot['sector'],
                                'Week 1': f"{rot['week1_emoji']} {rot['week1_avg']:.0f}%",
                                'Week 2': f"{rot['week2_emoji']} {rot['week2_avg']:.0f}%",
                                'Change': f"{direction} {rot['change']:+.1f}%",
                                'Status': '🔥 Strong' if abs(rot['change']) > 20 else '➡️ Moderate' if abs(rot['change']) > 10 else '💤 Stable'
                            })
                        
                        rotation_df = pd.DataFrame(rotation_data)
                        st.dataframe(rotation_df, use_container_width=True, hide_index=True)
                        
                        st.markdown("---")
                        
                        # Key insights
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("🚀 Biggest Gainer", 
                                     insights['rotations'][0]['sector'],
                                     f"+{insights['rotations'][0]['change']:.1f}%")
                        
                        with col2:
                            # Find biggest loser
                            biggest_loser = min(insights['rotations'], key=lambda x: x['change'])
                            st.metric("📉 Biggest Loser",
                                     biggest_loser['sector'],
                                     f"{biggest_loser['change']:.1f}%")
                        
                        with col3:
                            # Count rotations (significant changes)
                            significant = len([r for r in insights['rotations'] if abs(r['change']) > 15])
                            st.metric("🔄 Active Rotations",
                                     f"{significant}",
                                     "Sectors with 15%+ change")
                        
                        st.markdown("---")
                        
                        # Interpretation guides
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.info("""
                            **🔄 Rotation Signals:**
                            - 🔴 → 🟢 = **Money flowing IN** (bullish)
                            - 🟢 → 🔴 = **Money flowing OUT** (bearish)
                            - 🟢 → 🟢 = **Sustained strength** (momentum)
                            - 🔴 → 🔴 = **Continued weakness** (avoid)
                            """)
                        
                        with col2:
                            st.success("""
                            **🎯 Trading Strategies:**
                            - **Strong Rotation (20%+)**: Major sector shift, act decisively
                            - **Moderate (10-20%)**: Confirm with price action
                            - **Stable (<10%)**: Wait for clearer signals
                            """)
                    
                    st.markdown("---")
                    
                    # Momentum pattern guide
                    st.info("""
                    **📖 How to Read Momentum Patterns:**
                    - 🟢🟢🟢🟢🟢 = **Strong sustained rally** → Ride the trend, trail stops
                    - 🟢🟢🟢🟡🔴 = **Fading momentum** → Consider taking profits
                    - 🔴🔴🔴🔴🔴 = **Persistent weakness** → Avoid or short opportunity
                    - 🔴🔴🟡🟢🟢 = **Reversing higher** → Potential entry point
                    - 🟡🟡🟡🟡🟡 = **Range-bound** → Wait for directional breakout
                    - 🟢🔴🟢🔴🟢 = **Choppy/volatile** → High-risk environment
                    """)
            else:
                st.warning("No sector data available for selected date range.")
        else:
            st.warning("""
            ### 📌 Sector Rotation Analysis Not Available
            
            To enable this powerful feature:
            
            1. **Get 2 weeks of historical data:**
               ```
               python backfill_data_with_sectors.py
               ```
               ⏱️ Takes 10-20 minutes
            
            2. **Daily updates:**
               ```
               python stock_tracker_with_sectors.py
               ```
            
            **What you'll get:**
            - 🎯 See which sectors have momentum
            - 🔄 Track money rotation between sectors
            - 💪 Identify strongest/weakest industries
            - 📈 Make informed sector allocation decisions
            
            **Example insights:**
            - "IT sector showing 7-day rally 🟢🟢🟢🟢🟢🟢🟢"
            - "Banks rotating from weakness to strength 🔴🔴🟡🟢🟢"
            - "Money flowing from Tech to Financials (+35% rotation)"
            """)
            
            # Show sample visualization
            st.markdown("---")
            st.subheader("📸 Preview: What You'll See")
            st.markdown("""
            **Momentum Patterns:**
            ```
            Pharma    🟢🟢🟢🟢🟢🟢🟢 (85%) → Strong rally
            IT        🟢🟢🟢🟡🔴🔴🔴 (52%) → Fading momentum
            Auto      🟡🟢🟢🟢🟢🟢🟢 (72%) → Building strength
            Banks     🔴🔴🔴🔴🔴🔴🔴 (28%) → Persistent weakness
            ```
            
            **Rotation Analysis:**
            | Sector | Week 1 | Week 2 | Change |
            |--------|--------|--------|--------|
            | IT     | 🟢 78% | 🔴 35% | 📉 -43% |
            | Banks  | 🔴 31% | 🟢 72% | 📈 +41% |
            
            → Clear rotation from IT to Banks!
            """)
    
    with tab4:
        st.subheader("📊 Movement Distribution Heatmap")
        st.plotly_chart(create_heatmap(df_filtered), use_container_width=True, key="heatmap_distribution")
        
        st.info("""
        **How to read:** Colors show stock counts in each category over time.
        - 🟢 **Dark Green** = Many stocks in that movement range
        - 🟡 **Gold** = Neutral zone (balanced market)
        - 🔴 **Dark Red** = Many stocks in that movement range
        """)
        
        # Weekly pattern if enough data
        if len(df_filtered) >= 7:
            st.markdown("---")
            st.subheader("📅 Weekly Pattern Analysis")
            
            df_filtered['day_of_week'] = df_filtered['date'].dt.day_name()
            gainers = df_filtered['up_3_5'] + df_filtered['up_5_10'] + df_filtered['up_10_15'] + df_filtered['up_15_plus']
            losers = df_filtered['down_3_5'] + df_filtered['down_5_10'] + df_filtered['down_10_15'] + df_filtered['down_15_plus']
            
            weekly_data = pd.DataFrame({
                'Day': df_filtered['day_of_week'],
                'Gainers': gainers,
                'Losers': losers
            })
            
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            weekly_avg = weekly_data.groupby('Day').mean().reindex(day_order).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=weekly_avg['Day'], y=weekly_avg['Gainers'], 
                                name='Avg Gainers', marker_color='green'))
            fig.add_trace(go.Bar(x=weekly_avg['Day'], y=weekly_avg['Losers'], 
                                name='Avg Losers', marker_color='red'))
            fig.update_layout(title='Average Gainers/Losers by Day of Week', 
                            barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True, key="weekly_distribution")
            
            st.info("""
            **Day-of-week patterns can reveal:**
            - Monday effects (weekend news impact)
            - Friday patterns (position squaring)
            - Mid-week strength/weakness
            - Optimal entry/exit timing
            """)
    
    with tab5:
        st.subheader("🎯 Actionable Sector Signals")
        
        if ANALYTICS_AVAILABLE and sector_df is not None and len(sector_df) >= 5:
            intel = MarketIntelligence(df, sector_df)
            signals = intel.generate_sector_signals()
            
            if signals:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 💪 Strongest Sectors (BUY)")
                    for signal in signals[:5]:
                        with st.container():
                            st.markdown(f"**{signal['emoji']} {signal['action']}** - {signal['sector']}")
                            st.metric("Score", f"{signal['score']:.0f}/100", 
                                     delta=signal['trend'])
                            st.caption(signal['reasoning'])
                            
                            # Display top stocks
                            if signal['top_stocks'] and len(signal['top_stocks']) > 0:
                                st.markdown("**📈 Top Performers:**")
                                for stock in signal['top_stocks']:
                                    change_color = "🟢" if stock['change_pct'] > 0 else "🔴"
                                    st.markdown(f"  • {stock['symbol']}: {change_color} **{stock['change_pct']:+.2f}%**")
                            
                            st.markdown("---")
                
                with col2:
                    st.markdown("### ⚠️ Weakest Sectors (SELL)")
                    for signal in signals[-5:]:
                        with st.container():
                            st.markdown(f"**{signal['emoji']} {signal['action']}** - {signal['sector']}")
                            st.metric("Score", f"{signal['score']:.0f}/100",
                                     delta=signal['trend'])
                            st.caption(signal['reasoning'])
                            
                            # Display worst stocks
                            if signal['top_stocks'] and len(signal['top_stocks']) > 0:
                                st.markdown("**📉 Worst Performers:**")
                                for stock in signal['top_stocks']:
                                    change_color = "🟢" if stock['change_pct'] > 0 else "🔴"
                                    st.markdown(f"  • {stock['symbol']}: {change_color} **{stock['change_pct']:+.2f}%**")
                            
                            st.markdown("---")
                
                # Full signals table with expandable details
                st.markdown("---")
                st.markdown("### 📊 All Sector Signals")
                
                for signal in signals:
                    with st.expander(f"{signal['emoji']} {signal['sector']} - {signal['action']} ({signal['score']:.0f}/100)"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Score", f"{signal['score']:.0f}/100")
                        with col2:
                            st.metric("Breadth", f"{signal['breadth']:.1f}%")
                        with col3:
                            st.metric("Trend", signal['trend'])
                        
                        st.markdown(f"**Analysis:** {signal['reasoning']}")
                        
                        # Show top/bottom stocks
                        if signal['top_stocks'] and len(signal['top_stocks']) > 0:
                            st.markdown("---")
                            if signal['action'] in ['STRONG BUY', 'BUY']:
                                st.markdown("**🎯 Stocks to Watch (Top Performers):**")
                            elif signal['action'] in ['STRONG SELL', 'SELL']:
                                st.markdown("**⚠️ Stocks to Avoid (Worst Performers):**")
                            else:
                                st.markdown("**📊 Sample Stocks:**")
                            
                            # Display in a nice table format
                            stock_data = []
                            for stock in signal['top_stocks']:
                                stock_data.append({
                                    'Stock': stock['symbol'],
                                    'Change': f"{stock['change_pct']:+.2f}%",
                                    'Signal': '🟢 Buy' if stock['change_pct'] > 5 else '🔴 Sell' if stock['change_pct'] < -5 else '🟡 Hold'
                                })
                            
                            if stock_data:
                                st.table(pd.DataFrame(stock_data))
                
                # Risk Metrics
                st.markdown("---")
                st.subheader("⚠️ Risk Analysis")
                
                risk_metrics = intel.calculate_risk_metrics()
                if risk_metrics:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Risk Level", 
                                 f"{risk_metrics['emoji']} {risk_metrics['level']}")
                    
                    with col2:
                        st.metric("Sector Dispersion", 
                                 f"{risk_metrics['sector_dispersion']:.1f}%")
                    
                    with col3:
                        st.metric("Strong vs Weak", 
                                 f"{risk_metrics['strong_sectors']} vs {risk_metrics['weak_sectors']}")
                    
                    st.info(f"**Recommendation:** {risk_metrics['recommendation']}")
            else:
                st.info("Not enough sector data for signal generation. Need at least 5 days.")
        else:
            st.warning("""
            **📊 Sector Signals Unavailable**
            
            To enable actionable signals:
            1. Ensure `market_intelligence.py` is in your project folder
            2. Run `python stock_tracker_with_sectors.py` or `python backfill_data_with_sectors.py`
            3. Refresh this dashboard
            
            Signals provide BUY/SELL/HOLD recommendations per sector with top stock picks!
            """)
    
    # Data table (expandable)
    with st.expander("📋 View Raw Data"):
        st.dataframe(df_filtered.sort_values('date', ascending=False), use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "📊 Indian Stock Movement Tracker | Data updates daily after market close | "
        "Built with Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
