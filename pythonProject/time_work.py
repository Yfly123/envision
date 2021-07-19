from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler
def job_need_do():
    pass
schd = BlockingScheduler()
schd.add_job(job_need_do,'cron')