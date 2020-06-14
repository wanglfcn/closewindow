import tornado.ioloop
import tornado.web
import web.HttpHandler
import logging.config
import yaml
import logging
from tornado.options import options, define
from web.WSHandler import WebSocketClient
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from services import Scheduler
import sqlalchemy

define('port', default=8000, type=int)
define('ws_url', type=str)
define('log_url', type=str)
define('db_url', type=str)
define('power_delay_on', type=float)
define('power_delay_off', type=float)
define('image_dir', type=str)
define('image_url', type=str)

def make_app():
    return tornado.web.Application([
        (r"/open", web.HttpHandler.OpenWindowHandler),
        (r"/close", web.HttpHandler.CloseWindowHandler),
        (r"/power_on_fan", web.HttpHandler.OpenFanHandler),
        (r"/power_off_fan", web.HttpHandler.CloseFanHandler),
        (r"/get_jobs", web.HttpHandler.GetJobsHandler),
        (r"/pause_jobs", web.HttpHandler.PauseJobsHandler),
        (r"/resume_jobs", web.HttpHandler.ResumeJobsHandler),
        (r"/modify_job", web.HttpHandler.ModifyJobByIdHandler)
        (r"/take_photo", web.HttpHandler.TakenPhoto)
    ])

def initLogger():
    log_config = './config/log.yml'

    with open(log_config, 'rt') as f:
        conf = yaml.safe_load(f.read())
        logging.config.dictConfig(conf)

if __name__ == '__main__':
    options.parse_config_file('./config/server.conf')
    initLogger()
    logger = logging.getLogger()
    app = make_app()
    logger.info('start server listen on port ' + str(options.port))
    ws = WebSocketClient()
    ws.open()

    app = HTTPServer(app)
    app.bind(options.port)
    app.start(1)

    Scheduler.init()
    Scheduler.startJobs()

    IOLoop.current().start()

