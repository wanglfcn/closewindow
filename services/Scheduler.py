from apscheduler.schedulers.tornado import TornadoScheduler
from tornado.options import options

class Scheduler:
    def __init__(self):
        scheduler = TornadoScheduler()
        scheduler.add_jobstore('sqlalchemy', url=options.db_url)
        scheduler.start()
