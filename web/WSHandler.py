import tornado.websocket
import logging
from tornado.options import options
from tornado.websocket import websocket_connect
from services import RelayService
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
            resp = {'type': 'log'}
            if msg and 'type' in msg:
                if msg['type'] == 'open':
                    RelayService.openWindow()
                    resp['content'] = 'window opened'
                    if self.conn:
                        self.conn.write_message(json.dumps(resp))

                elif msg['type'] == 'close':
                    RelayService.closeWindow()
                    resp['content'] = 'window closed'
                    if self.conn:
                        self.conn.write_message(json.dumps(resp))
        except Exception as e:
            logging.getLogger().error('process msg with exception %r', e)


    def on_close(self):
        logging.getLogger().info('on close')
        self.open()


