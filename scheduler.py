from apscheduler.schedulers.background import BackgroundScheduler
from engine import execute_all_rules
import time

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(execute_all_rules, 'interval', minutes=1)
    scheduler.start()
    print("Scheduler started. Running every 1 minutes.")

    try:
        while True:
            time.sleep(10)  # Keeps the scheduler alive
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
