from apscheduler.schedulers.background import BackgroundScheduler
from tornado.options import options, define
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from services import RelayService


job_default = {
    'coalesce': False,
    'max_instances': 5
}

scheduler = BackgroundScheduler(job_defaults=job_default, timezone='Asia/Shanghai')

def init():
    scheduler.add_jobstore('sqlalchemy', url=options.db_url)
    scheduler.add_executor(ThreadPoolExecutor(20))
    scheduler.add_executor(ProcessPoolExecutor(10), alias='processpool')

    scheduler.add_job(RelayService.openWindow, id='openWindow', replace_existing=True, trigger='cron', hour='18', minute='0', second='0')
    scheduler.add_job(RelayService.closeWindow, id='closeWindow', replace_existing=True, trigger='cron', hour='19', minute='30', second='0')
    scheduler.add_job(RelayService.openFan, id='powerOnFan', replace_existing=True, trigger='cron', hour='18', minute='1', second='0')
    scheduler.add_job(RelayService.closeFan, id='powerOffFan', replace_existing=True, trigger='cron', hour='19', minute='31', second='0')
    scheduler.add_job(RelayService.takePhoto, id="takePhoto", replace_existing=True, trigger='cron', hour='18,19', minute='2,32', second='0')

def startJobs():
    scheduler.start()

def getJobs():
    jobs = scheduler.get_jobs()
    result = {}
    for job in jobs:
        result[job.id] = '%s' % (job,)

    return result

def pause():
    scheduler.pause()

def resume():
    scheduler.resume()

def modityExecuteTime(job_id, time_params):
    year = getOrDefault(time_params, 'year')
    month = getOrDefault(time_params, 'month')
    day = getOrDefault(time_params, 'day')
    week = getOrDefault(time_params, 'week')
    day_of_week = getOrDefault(time_params, 'day_of_week')
    hour = getOrDefault(time_params, 'hour')
    minute = getOrDefault(time_params, 'minute')
    second = getOrDefault(time_params, 'second')

    return scheduler.reschedule_job(job_id=job_id,
                                  trigger='cron',
                                  year=year,
                                  month=month,
                                  day=day,
                                  week=week,
                                  day_of_week=day_of_week,
                                  hour=hour,
                                  minute=minute,
                                  second=second)

def getOrDefault(map, key, def_val='*'):
    if map and key in map:
        return map[key]
    return def_val
