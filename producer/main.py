import uvicorn
import json
import time
from datetime import datetime
from fastapi import FastAPI,WebSocket
from kafka import KafkaProducer


app = FastAPI()
producer = KafkaProducer(
    bootstrap_servers=["kafka:29092"],
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    retries=5
)

@app.get("/")
async def base():
    return {"foo": "bar"}

@app.websocket("//{service}")
async def sensor_endpoint(websocket: WebSocket,service: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"service:{service} data:{data}")
        payload=parse_data(service,data)
        payload["@timestamp"] = datetime.now().isoformat()
        payload["sender"] = websocket.client.host
        payload["service"] = service
        # print(payload)
        producer.send("smartphone-sensor", value=payload).add_callback(on_send_success).add_errback(on_send_error)
        # await websocket.send_text(data)
    # websocket.close()
    

def parse_data(service:str,data:str)->dict:
    if service in ["accelerometer","gyroscope","orientation","proximity"]:
        data=list(eval(data))
    if service=="geolocation":
        data=json.loads(data)
    dict_={}
    dict_[service]=data
    dict_["raw_data"]=data
    return dict_

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)

if __name__ == "__main__":
    time.sleep(15)
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True,log_level="trace")
    metrics = producer.metrics()
    print(metrics)