import tornado.websocket
import logging
from tornado.options import options
from tornado.websocket import websocket_connect
from services import RelayService
import requests
import json
import time

class WebSocketClient:

    def open(self):
        logging.info('open connect [%s]', options.ws_url)
        url = options.ws_url

        self.conn_future = websocket_connect(url=url,
                          callback=self.on_connect,
                          on_message_callback=self.on_message,
                          ping_interval=1,
                          ping_timeout=10)
        logging.getLogger().info('connect to %s', url)
        return self.conn_future

    def on_connect(self, future):
        logging.getLogger().info('on connect: %s, %r', options.ws_url, future)
        try:
            self.conn = future.result()
            logging.getLogger().info('connect is done: %s, conn: %r', options.ws_url, self.conn)
        except Exception as e:
            self.conn = None
            logging.getLogger().error('connect [%s] with exception %r', options.ws_url, e)
            time.sleep(1)
            self.open()

    def on_message(self, message):
        logging.getLogger().info('on msg: %s', message)
        if not message:
            self.on_close()
            return
        try:
            msg = json.loads(message)
            if msg and 'type' in msg:
                msg_type = msg['type']
                self.handleMsg(msg_type, msg)
        except Exception as e:
            logging.getLogger().error('process msg with exception %r', e)


    def on_close(self):
        logging.getLogger().info('on close')
        self.open()

    def handleMsg(self, msg_type, msg):
        handler = {
            'open': self.handleOpen,
            'close': self.handleClose,
            'power_on_fan': self.powerOnFan,
            'power_off_fan': self.powerOffFan,
            'get_jobs': self.getJobs,
            'pause_jobs': self.pauseJobs,
            'resume_jobs': self.resumeJobs,
            'modify_job': self.modifyJob
        }

        seq = '0'
        if 'seq' in msg:
            seq = str(msg['seq'])

        func = handler[msg_type]
        if func:
            func(msg, seq)

    def sendResp(self, msg):
        if self.conn:
            self.conn.write_message(json.dumps(msg))
        requests.post(url=options.log_url, json=msg)

    def handleOpen(self, msg, seq):
        RelayService.openWindow()
        resp = {'type': 'resp', 'content': 'window opening', 'seq': seq}
        self.sendResp(resp)


    def handleClose(self, msg, seq):
        RelayService.closeWindow()
        resp = {'type': 'resp', 'content': 'window closing', 'seq': seq}
        self.sendResp(resp)

    def powerOnFan(self, msg, seq):
        RelayService.openFan()
        resp = {'type': 'resp', 'content': 'power on fan', 'seq': seq}
        self.sendResp(resp)

    def powerOffFan(self, msg, seq):
        RelayService.closeFan()
        resp = {'type': 'resp', 'content': 'power off fan', 'seq': seq}
        self.sendResp(resp)

    def getJobs(self, msg, seq):
        jobs = RelayService.getJobs()
        resp = {'type': 'resp', 'jobs': jobs, 'seq': seq, 'content': '%s' % (jobs,)}
        self.sendResp(resp)

    def pauseJobs(self, msg, seq):
        RelayService.pause()
        resp = {'type': 'resp', 'content': 'pause all jobs', 'seq': seq}
        self.sendResp(resp)

    def resumeJobs(self, msg, seq):
        RelayService.resume()
        resp = {'type': 'resp', 'content': 'resume all jobs', 'seq': seq}
        self.sendResp(resp)

    def modifyJob(self, msg, seq):
        if 'job_id' in msg and 'time_params' in msg:
            job_id = msg['job_id']
            time_params = msg['time_params']
            job = RelayService.modityExecuteTime(job_id, time_params)
            resp = {'type': 'resp', 'content': 'modify job %s' % (job,)}
            self.sendResp(resp)
        else:
            resp = {'type': 'resp', 'content': 'missing job id or time params for modify job', 'seq': seq}
            self.sendResp(resp)





