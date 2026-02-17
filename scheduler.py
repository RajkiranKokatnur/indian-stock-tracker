"""
Automated Scheduler for Daily Stock Tracking
Runs stock_tracker.py at a specified time every day
"""

import schedule
import time
from datetime import datetime
import subprocess
import os

def run_tracker():
    """Execute the stock tracker script"""
    print(f"\n{'='*60}")
    print(f"Running Daily Stock Tracker at {datetime.now()}")
    print(f"{'='*60}\n")
    
    try:
        # Run the tracker script
        result = subprocess.run(['python', 'stock_tracker.py'], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("✅ Tracker completed successfully")
            
            # Optionally run visualization after tracking
            print("\n🎨 Generating visualizations...")
            viz_result = subprocess.run(['python', 'visualize_trends.py'], 
                                       capture_output=True, text=True)
            print(viz_result.stdout)
        else:
            print("❌ Tracker failed with errors:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error running tracker: {e}")

def main():
    """Main scheduler function"""
    # Set the time to run (Indian market hours: after 3:30 PM IST when market closes)
    # Adjust time as needed (24-hour format)
    RUN_TIME = "16:00"  # 4:00 PM IST (after market close)
    
    print("🚀 Stock Movement Tracker Scheduler Started")
    print(f"📅 Scheduled to run daily at {RUN_TIME} IST")
    print(f"💾 Data will be saved to: stock_movements_history.csv")
    print("\n⌨️  Press Ctrl+C to stop the scheduler\n")
    
    # Schedule the job
    schedule.every().day.at(RUN_TIME).do(run_tracker)
    
    # Optional: Run immediately on start (comment out if not needed)
    print("🔄 Running initial execution...")
    run_tracker()
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n⛔ Scheduler stopped by user")

if __name__ == "__main__":
    main()
