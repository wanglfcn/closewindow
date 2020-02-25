import logging
from tornado.web import RequestHandler
from services.RelayService import *
from services.Scheduler import *
import json

class OpenWindowHandler(RequestHandler):
    def get(self):
        logging.getLogger().info('set window to open')
        closeWindow()
        self.write('{"code":0,"status":"success"}')

class CloseWindowHandler(RequestHandler):
    def get(self):
        logging.getLogger().info('set window to close')
        openWindow()
        self.write('{"code":0,"status":"success"}')

class OpenFanHandler(RequestHandler):
    def get(self):
        logging.getLogger().info('power on fan')
        openFan()
        self.write('{"code":0,"status":"success"}')

class CloseFanHandler(RequestHandler):
    def get(self):
        logging.getLogger().info('power off fan')
        closeFan()
        self.write('{"code":0,"status":"success"}')

class GetJobsHandler(RequestHandler):
    def get(self):
        logging.getLogger().info('get all jobs')
        jobs = getJobs()
        resp = {
            'code': 0,
            'status': 'success',
            'jobs': jobs
        }

        result = json.dumps(resp)
        self.write(result)

class PauseJobsHandler(RequestHandler):
    def get(self):
        logging.getLogger().info('pause jobs')
        pause()
        self.write('{"code":0,"status":"success"}')

class ResumeJobsHandler(RequestHandler):
    def get(self):
        logging.getLogger().info('resume jobs')
        resume()
        self.write('{"code":0,"status":"success"}')

class ModifyJobByIdHandler(RequestHandler):
    def get(self):
        job_id = self.get_query_argument('job_id', None)
        if not job_id:
            self.write('{"code":1,"status":"fail","reason":"missing job id"}')
            return
        time_params = {}
        time_params['year'] = self.get_query_argument('year', '*')
        time_params['month'] = self.get_query_argument('month', '*')
        time_params['day'] = self.get_query_argument('day', '*')
        time_params['week'] = self.get_query_argument('week', '*')
        time_params['day_of_week'] = self.get_query_argument('day_of_week', '*')
        time_params['hour'] = self.get_query_argument('hour', '*')
        time_params['minute'] = self.get_query_argument('minute', '*')
        time_params['second'] = self.get_query_argument('second', '*')
        logging.getLogger().info('modify job')
        try:
            job = modityExecuteTime(job_id, time_params)
            resp = {
                'code': 0,
                'status': 'success',
                'job': '%s' % (job,)
            }

            self.write(json.dumps(resp))
        except Exception as e:
            resp = {
                'code': 1,
                'status': 'fail',
                'reason': '%s' % (e,)
            }
            self.write(json.dumps(resp))
