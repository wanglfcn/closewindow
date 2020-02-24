import logging
from tornado.web import RequestHandler
from services.RelayService import *
from services.Scheduler import *

class OpenWindowHandler(RequestHandler):
    def get(self, *args, **kwargs):
        logging.getLogger().info('set window to open')
        self.write('{"code":0,"status":"success"}')
        closeWindow()

class CloseWindowHandler(RequestHandler):
    def get(self, *args, **kwargs):
        logging.getLogger().info('set window to close')
        self.write('{"code":0,"status":"success"}')
        openWindow()

class OpenFanHandler(RequestHandler):
    def get(self, *args, **kwargs):
        logging.getLogger().info('power on fan')
        openFan()
        self.write('{"code":0,"status":"success"}')

class CloseFanHandler(RequestHandler):
    def get(self, *args, **kwargs):
        logging.getLogger().info('power off fan')
        closeFan()
        self.write('{"code":0,"status":"success"}')

class GetJobsHandler(RequestHandler):
    def get(self, *args, **kwargs):
        logging.getLogger().info('get all jobs')
        jobs = getJobs()
        val = 'jobs: %r' % (jobs,)
        logging.getLogger().info('jobs ' + val)
        self.write('{"code":0,"status":"success"}')

def PauseJobsHandler(RequestHandler):
    def get(self, *args, **kwargs):
        logging.getLogger().info('pause jobs')
        pause()
        self.write('{"code":0,"status":"success"}')

def ResumeJobsHandler(RequestHandler):
    def get(self, *args, **kwargs):
        logging.getLogger().info('resume jobs')
        resume()
        self.write('{"code":0,"status":"success"}')

class ModifyJobByIdHandler(RequestHandler):
    def get(self, *args, **kwargs):
        logging.getLogger().info('modify job')
        modityExecuteTime()
        self.write('{"code":0,"status":"success"}')
