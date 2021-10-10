#!/usr/bin/env python3

import os
import signal
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.log import app_log
from mysql_client import MySQLClient

from ffmpeg import load_audio
from custom_logger import init_logger


class AudioStreamer:
    def __init__(self, tornado_websocket_handler):
        self.sql_client = MySQLClient()
        self.ws = tornado_websocket_handler

    async def process(self, message):
        # current_audio_type = self.sql_client.get_current_audio_type()
        # if current_audio_type is None:
        #     app_log.info("not found: current_audio_type")
        #     return None

        file_name = self.sql_client.get_audio(message)
        if file_name is None:
            app_log.info("not found: {}".format(message))
            return False

        # dir_path = current_audio_type.get('dir_path')
        dir_path = "/var/lib/aion/Data/audios/"
        file_path = os.path.join(dir_path, file_name)

        app_log.info("start streaming: {}".format(file_path))

        for chunk in load_audio(file_path):
            try:
                await self.ws.write_message(chunk, binary=True)
            except Exception:
                app_log.info("[AudioStreamer] failed to stream: {}".format(file_path))
                self.ws.close()
                return False

        app_log.info("complete streaming: {}".format(file_path))
        return True


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    # チェックイン画面、チェックアウト画面で音声を再生するためのWebSocket
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_streamer = AudioStreamer(tornado_websocket_handler=self)

    def check_origin(self, origin):
        return True

    def open(self):
        app_log.info("[WebSocketHandler] WebSocket opened")

    async def on_message(self, message):
        result = await self.audio_streamer.process(message)
        if not result:
            app_log.info("[WebSocketHandler] failed to stream: {}".format(message))

    def on_close(self):
        app_log.info("[WebSocketHandler] WebSocket closed")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/websocket", WebSocketHandler),
        ]
        super().__init__(handlers)


def signal_handler(signum, frame):
    app_log.info("Interrupt caught")
    tornado.ioloop.IOLoop.instance().stop()


def main():
    init_logger()

    app = Application()

    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

    # or you can use a custom handler,
    # in which case recv will fail with EINTR
    app_log.info("registering sigint")
    signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    main()
