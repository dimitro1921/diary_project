from apscheduler.schedulers.background import BackgroundScheduler
from app.logic import generate_daily_prompts
from app.config import PROMPT_HOUR, PROMPT_MINUTE

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(
        generate_daily_prompts,
        trigger="cron",
        hour=PROMPT_HOUR,
        minute=PROMPT_MINUTE,
        id="daily_prompt_job",
        replace_existing=True
    )
    scheduler.start()
