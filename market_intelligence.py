"""
Market Intelligence Module
Adds descriptive, predictive, and prescriptive analytics
"""

import pandas as pd
import numpy as np
from scipy.stats import percentileofscore
from datetime import datetime, timedelta

class MarketIntelligence:
    def __init__(self, movements_df, sector_df=None):
        self.movements_df = movements_df
        self.sector_df = sector_df
        
    def calculate_market_score(self):
        """Calculate overall market health score (0-100)"""
        if len(self.movements_df) < 5:
            return None
        
        latest = self.movements_df.iloc[-1]
        
        # Calculate breadth
        gainers = latest['up_3_5'] + latest['up_5_10'] + latest['up_10_15'] + latest['up_15_plus']
        losers = latest['down_3_5'] + latest['down_5_10'] + latest['down_10_15'] + latest['down_15_plus']
        total_movers = gainers + losers
        breadth = (gainers / total_movers * 100) if total_movers > 0 else 50
        
        # Calculate momentum (5-day trend)
        if len(self.movements_df) >= 5:
            recent = self.movements_df.tail(5)
            recent_breadths = []
            for _, row in recent.iterrows():
                g = row['up_3_5'] + row['up_5_10'] + row['up_10_15'] + row['up_15_plus']
                l = row['down_3_5'] + row['down_5_10'] + row['down_10_15'] + row['down_15_plus']
                tm = g + l
                recent_breadths.append((g / tm * 100) if tm > 0 else 50)
            
            momentum_score = (recent_breadths[-1] - recent_breadths[0]) / 50 * 100
            momentum_score = max(0, min(100, 50 + momentum_score))
        else:
            momentum_score = 50
        
        # Calculate volatility score (lower volatility = higher score)
        if len(self.movements_df) >= 10:
            all_breadths = []
            for _, row in self.movements_df.tail(10).iterrows():
                g = row['up_3_5'] + row['up_5_10'] + row['up_10_15'] + row['up_15_plus']
                l = row['down_3_5'] + row['down_5_10'] + row['down_10_15'] + row['down_15_plus']
                tm = g + l
                all_breadths.append((g / tm * 100) if tm > 0 else 50)
            
            volatility = np.std(all_breadths)
            volatility_score = max(0, 100 - (volatility * 2))
        else:
            volatility_score = 50
        
        # Weighted score
        overall_score = (
            breadth * 0.5 +
            momentum_score * 0.3 +
            volatility_score * 0.2
        )
        
        return {
            'overall': round(overall_score, 0),
            'breadth': round(breadth, 1),
            'breadth_score': round(breadth, 0),
            'momentum': round(momentum_score, 0),
            'volatility': round(volatility_score, 0),
            'regime': self._determine_regime(breadth, momentum_score, volatility_score)
        }
    
    def _determine_regime(self, breadth, momentum, volatility):
        """Determine market regime"""
        if breadth > 60 and momentum > 55:
            return {'name': 'BULL MARKET', 'emoji': '🟢', 'description': 'Strong uptrend, favorable conditions'}
        elif breadth < 40 and momentum < 45:
            return {'name': 'BEAR MARKET', 'emoji': '🔴', 'description': 'Downtrend, defensive positioning advised'}
        elif volatility < 40:
            return {'name': 'HIGH VOLATILITY', 'emoji': '🟠', 'description': 'Choppy market, trade carefully'}
        else:
            return {'name': 'NEUTRAL', 'emoji': '🟡', 'description': 'Range-bound, wait for direction'}
    
    def generate_sector_signals(self):
        """Generate BUY/SELL/HOLD signals for each sector with top stocks"""
        if self.sector_df is None or len(self.sector_df) < 7:
            return None
        
        signals = []
        sectors = self.sector_df['sector'].unique()
        
        # Try to load latest stock details
        from datetime import datetime
        import glob
        import os
        
        # Find most recent stock details file
        stock_files = glob.glob('stock_details_*.csv')
        latest_stocks = None
        if stock_files:
            latest_file = max(stock_files)
            try:
                latest_stocks = pd.read_csv(latest_file)
            except:
                latest_stocks = None
        
        for sector in sectors:
            sector_data = self.sector_df[self.sector_df['sector'] == sector].tail(10)
            
            if len(sector_data) < 5:
                continue
            
            # Calculate metrics
            latest_breadth = sector_data.iloc[-1]['breadth']
            avg_breadth = sector_data['breadth'].mean()
            trend = sector_data['breadth'].diff().tail(5).mean()
            
            # Momentum score
            momentum = self._calculate_momentum_pattern(sector_data)
            
            # Calculate score
            score = (
                (latest_breadth / 100) * 40 +  # Current strength
                (trend + 5) * 5 +                # Trend direction
                momentum['score'] * 0.2         # Pattern strength
            )
            score = max(0, min(100, score))
            
            # Generate signal
            if score >= 70:
                action = "STRONG BUY"
                emoji = "🟢🟢🟢"
                reasoning = f"Strong momentum ({momentum['pattern']}), breadth {latest_breadth:.0f}% above average"
            elif score >= 55:
                action = "BUY"
                emoji = "🟢🟢"
                reasoning = f"Positive trend, breadth {latest_breadth:.0f}%"
            elif score >= 45:
                action = "HOLD"
                emoji = "🟡🟡"
                reasoning = f"Neutral conditions, breadth near average ({latest_breadth:.0f}%)"
            elif score >= 30:
                action = "SELL"
                emoji = "🔴🔴"
                reasoning = f"Weakening trend, breadth {latest_breadth:.0f}%"
            else:
                action = "STRONG SELL"
                emoji = "🔴🔴🔴"
                reasoning = f"Persistent weakness ({momentum['pattern']}), breadth {latest_breadth:.0f}%"
            
            # Get top stocks for this sector
            top_stocks = []
            if latest_stocks is not None and 'sector' in latest_stocks.columns:
                sector_stocks = latest_stocks[latest_stocks['sector'] == sector].copy()
                if len(sector_stocks) > 0:
                    sector_stocks = sector_stocks.sort_values('change_pct', ascending=False)
                    
                    # Get top 3 for BUY signals, bottom 3 for SELL signals
                    if action in ['STRONG BUY', 'BUY']:
                        top_stocks = sector_stocks.head(3)[['symbol', 'change_pct']].to_dict('records')
                    elif action in ['STRONG SELL', 'SELL']:
                        top_stocks = sector_stocks.tail(3)[['symbol', 'change_pct']].to_dict('records')
                    else:
                        # For HOLD, show mix of top and bottom
                        top_stocks = sector_stocks.head(2)[['symbol', 'change_pct']].to_dict('records')
            
            signals.append({
                'sector': sector,
                'score': round(score, 0),
                'action': action,
                'emoji': emoji,
                'breadth': latest_breadth,
                'trend': 'Rising' if trend > 0 else 'Falling',
                'reasoning': reasoning,
                'top_stocks': top_stocks
            })
        
        return sorted(signals, key=lambda x: x['score'], reverse=True)
    
    def _calculate_momentum_pattern(self, sector_data):
        """Analyze momentum pattern"""
        pattern = []
        for breadth in sector_data['breadth'].tail(7):
            if breadth >= 65:
                pattern.append('🟢')
            elif breadth >= 45:
                pattern.append('🟡')
            else:
                pattern.append('🔴')
        
        pattern_str = ''.join(pattern)
        
        # Calculate pattern score
        green_count = pattern_str.count('🟢')
        red_count = pattern_str.count('🔴')
        
        if green_count >= 5:
            return {'pattern': pattern_str, 'score': 80, 'description': 'Strong uptrend'}
        elif red_count >= 5:
            return {'pattern': pattern_str, 'score': 20, 'description': 'Strong downtrend'}
        else:
            return {'pattern': pattern_str, 'score': 50, 'description': 'Mixed'}
    
    def detect_divergences(self):
        """Detect market breadth divergences"""
        if len(self.movements_df) < 3:
            return None
        
        recent = self.movements_df.tail(3)
        breadths = []
        
        for _, row in recent.iterrows():
            g = row['up_3_5'] + row['up_5_10'] + row['up_10_15'] + row['up_15_plus']
            l = row['down_3_5'] + row['down_5_10'] + row['down_10_15'] + row['down_15_plus']
            tm = g + l
            breadths.append((g / tm * 100) if tm > 0 else 50)
        
        # Check for persistent narrow breadth
        if all(b < 48 for b in breadths):
            return {
                'type': 'BEARISH DIVERGENCE',
                'severity': 'HIGH',
                'description': 'Persistent narrow breadth for 3+ days. Weakness likely to continue.',
                'action': 'Reduce exposure, raise cash'
            }
        elif all(b < 52 and b > 48 for b in breadths):
            return {
                'type': 'NARROW BREADTH',
                'severity': 'MEDIUM',
                'description': 'Market lacking conviction. Few stocks participating.',
                'action': 'Be selective, avoid chasing'
            }
        
        return None
    
    def predict_next_breadth(self):
        """Predict tomorrow's market breadth"""
        if len(self.movements_df) < 10:
            return None
        
        # Get recent breadths
        recent_breadths = []
        for _, row in self.movements_df.tail(10).iterrows():
            g = row['up_3_5'] + row['up_5_10'] + row['up_10_15'] + row['up_15_plus']
            l = row['down_3_5'] + row['down_5_10'] + row['down_10_15'] + row['down_15_plus']
            tm = g + l
            recent_breadths.append((g / tm * 100) if tm > 0 else 50)
        
        current = recent_breadths[-1]
        momentum_5d = np.mean(recent_breadths[-5:])
        trend = np.mean(np.diff(recent_breadths[-5:]))
        volatility = np.std(recent_breadths)
        
        # Simple prediction model
        prediction = (
            current * 0.4 +
            momentum_5d * 0.3 +
            50 * 0.2 +  # Mean reversion
            trend * 5
        )
        
        prediction = max(20, min(80, prediction))
        confidence = max(50, 100 - volatility * 3)
        
        return {
            'prediction': round(prediction, 1),
            'range_low': round(prediction - volatility * 1.5, 1),
            'range_high': round(prediction + volatility * 1.5, 1),
            'confidence': round(confidence, 0),
            'trend': 'Rising' if trend > 0 else 'Falling' if trend < 0 else 'Flat'
        }
    
    def calculate_risk_metrics(self):
        """Calculate portfolio risk metrics"""
        if self.sector_df is None or len(self.sector_df) < 5:
            return None
        
        # Get latest sector breadths
        latest_date = self.sector_df['date'].max()
        latest_sectors = self.sector_df[self.sector_df['date'] == latest_date]
        
        # Calculate concentration
        breadths = latest_sectors['breadth'].values
        sector_volatility = np.std(breadths)
        
        # Identify extreme positions
        strong_sectors = len(latest_sectors[latest_sectors['breadth'] >= 65])
        weak_sectors = len(latest_sectors[latest_sectors['breadth'] <= 35])
        
        # Risk level
        if sector_volatility > 20 or weak_sectors > strong_sectors:
            risk_level = 'HIGH'
            risk_emoji = '🔴'
        elif sector_volatility > 15:
            risk_level = 'MEDIUM'
            risk_emoji = '🟡'
        else:
            risk_level = 'LOW'
            risk_emoji = '🟢'
        
        return {
            'level': risk_level,
            'emoji': risk_emoji,
            'sector_dispersion': round(sector_volatility, 1),
            'strong_sectors': strong_sectors,
            'weak_sectors': weak_sectors,
            'recommendation': self._get_risk_recommendation(risk_level, strong_sectors, weak_sectors)
        }
    
    def _get_risk_recommendation(self, level, strong, weak):
        """Get risk-based recommendations"""
        if level == 'HIGH':
            return "Reduce position sizes, increase cash levels, focus on quality"
        elif level == 'MEDIUM':
            return "Maintain balanced exposure, be selective with new positions"
        else:
            return "Favorable conditions for deployment, consider adding to winners"
    
    def get_statistical_context(self):
        """Get statistical context for current market"""
        if len(self.movements_df) < 30:
            return None
        
        # Calculate current breadth
        latest = self.movements_df.iloc[-1]
        g = latest['up_3_5'] + latest['up_5_10'] + latest['up_10_15'] + latest['up_15_plus']
        l = latest['down_3_5'] + latest['down_5_10'] + latest['down_10_15'] + latest['down_15_plus']
        tm = g + l
        current_breadth = (g / tm * 100) if tm > 0 else 50
        
        # Calculate historical breadths
        all_breadths = []
        for _, row in self.movements_df.iterrows():
            g = row['up_3_5'] + row['up_5_10'] + row['up_10_15'] + row['up_15_plus']
            l = row['down_3_5'] + row['down_5_10'] + row['down_10_15'] + row['down_15_plus']
            tm = g + l
            all_breadths.append((g / tm * 100) if tm > 0 else 50)
        
        mean = np.mean(all_breadths)
        std = np.std(all_breadths)
        percentile = percentileofscore(all_breadths, current_breadth)
        z_score = (current_breadth - mean) / std if std > 0 else 0
        
        # Interpretation
        if z_score > 2:
            interpretation = "Extremely bullish (top 5%)"
            color = "🟢"
        elif z_score > 1:
            interpretation = "Bullish (top 16%)"
            color = "🟢"
        elif z_score < -2:
            interpretation = "Extremely bearish (bottom 5%)"
            color = "🔴"
        elif z_score < -1:
            interpretation = "Bearish (bottom 16%)"
            color = "🔴"
        else:
            interpretation = "Normal range"
            color = "🟡"
        
        return {
            'current': round(current_breadth, 1),
            'mean': round(mean, 1),
            'std': round(std, 1),
            'percentile': round(percentile, 0),
            'z_score': round(z_score, 2),
            'interpretation': interpretation,
            'color': color
        }