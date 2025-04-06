from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json, time
from WebSpider import *

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # 初始化Web类
    web = Web()
    web.get_cookie()
    while True:
        r_data = await websocket.receive_text()
        print(r_data)
        data = {"message": "Success",
                "from": "server",
                "type": None,
                "step": 0,
                "time_use": None,
                "progress": 0}

        if r_data == "login":
            t1 = time.time()
            if not web.is_login():
                web.login('pctest', '954321')
                web.save_cookie()
            t2 = time.time()
            data["type"] = "login"
            data["time_use"] = t2 - t1
            send_data = json.dumps(data)
            await websocket.send_text(send_data)

        else:
            # 获取房间号
            t1 = time.time()
            try:
                web.get_roomid()
            except:
                pass
            web.get_roomid()
            t2 = time.time()
            data["type"] = "upgrade"
            data["time_use"] = t2 - t1
            send_data = json.dumps(data)
            await websocket.send_text(send_data)

            t1 = time.time()
            web.get_roompage()
            t2 = time.time()
            data["time_use"] = t2 - t1
            data["step"] += 1
            send_data = json.dumps(data)
            await websocket.send_text(send_data)

            ts = time.time()
            t1 = time.time()
            web.get_testid()
            t2 = time.time()
            data["time_use"] = t2 - t1
            data["step"] += 1
            send_data = json.dumps(data)
            await websocket.send_text(send_data)

            t1 = time.time()
            html = web.get_review()
            qs = web.get_ans(html)
            t2 = time.time()
            data["time_use"] = t2 - t1
            data["step"] += 1
            send_data = json.dumps(data)
            await websocket.send_text(send_data)
            ind = 0
            t1 = time.time()
            data["step"] += 1
            for q in qs:
                ind += 1
                time.sleep(0.5)
                web.submit_ans(q[2], q[3], q[1])
                data["progress"] = ind*10
                send_data = json.dumps(data)
                await websocket.send_text(send_data)
                if ind == 10:
                    te = time.time()
                    if te - ts < 20:
                        time.sleep(relu(20 - (te-ts) + 0.1))
                    else:
                        time.sleep(0.1)
                jf = web.get_result(ind + 1)
            ted = time.time()
            data["time_use"] = te-ts
            data["step"] += 1
            send_data = json.dumps(data)
            await websocket.send_text(send_data)
            data["time_use"] = ted - ts
            data["step"] += 1
            send_data = json.dumps(data)
            await websocket.send_text(send_data)

