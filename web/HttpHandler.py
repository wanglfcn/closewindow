import logging
from tornado.web import RequestHandler
from services.RelayService import *

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
