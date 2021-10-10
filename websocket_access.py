import sys
import asyncio
from websocket import create_connection
import time

# 動作確認用
async def send_message(message, num):
    ws = create_connection("ws://localhost:8888/websocket")
    print(ws.send(message))
    cnt = 0
    while True:
        receive = ws.recv()
        if receive != 'EOS':
            print('{}: {}: {}'.format(num, cnt, receive[0:5]))
        else:
            print('{}: {}: {}'.format(num, cnt, receive))
            break
        cnt += 1
    ws.close()


if len(sys.argv) > 1:
    message = sys.argv[1]
else:
    message = 'hello'

counters = asyncio.gather(
    send_message(ws, message, 1),
    send_message(ws, message, 2),
)

loop = asyncio.get_event_loop()
result = loop.run_untile_complete(counters)
print(result)
loop.close()

