from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.collectors.price_data_collector import collect_tv

def run_daily_task():
    print(f"[{datetime.now()}] 🚀 Running TradingView collector")
    collect_tv()

scheduler = BackgroundScheduler(timezone="Asia/Ho_Chi_Minh")
scheduler.add_job(run_daily_task, "cron", hour=0, minute=30, second=45)  # 0:28 giờ VN
scheduler.start()