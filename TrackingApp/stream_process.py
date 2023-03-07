import cv2 
import time 
import logging 
import asyncio
import threading
import numpy as np 
from media_player import Reader 
from logging.handlers import RotatingFileHandler
from grpc_libs.ai_client import PersonGrpcClient as PGC

locked = False
command = "STOP"

async def pipe_process(grpc_client:PGC, frame):
    global locked
    if locked:
        return
    try:
        locked = True
        boxes, _, _ = grpc_client.detection(frame)
        result = {}
        tasks = []
        for box in boxes:
            # cv2.rectangle(test, (box[0], box[1]), (box[2], box[3]), (255, 128, 0), 4)
            crop_image = frame[box[1]:box[3], box[0]: box[2]]
            task = asyncio.create_task(check_emotion(grpc_client=grpc_client, crop_image=crop_image, result = result))
            tasks.append(task)
        await asyncio.gather(*tasks)     
    finally:
        locked = False
        return result
 
async def check_emotion(grpc_client, crop_image, result):
    res = grpc_client.check_emotion(crop_image)
    if res[0] in result:
        result[res[0]] += 1
    else:
        result[res[0]] = 1

async def send_result(sessionID, result):
    print(result)

async def process(args, logger):
    logger.info("Create thread load frame")
    reader = Reader(args.u)
    reader.start()
    logger.info("Create redis connection")
    grpc_client = PGC.getInstance(args.i, args.p, args.c)
    while True:
        frame = reader.get_frame()
        if frame is None:
            time.sleep(0.5)
        else:
            global locked
            if not locked:
                logger.info("Start task check")
                task1 = asyncio.create_task(
                    pipe_process(grpc_client=grpc_client, frame=frame))
                await task1 
                result = task1.result()
                logger.info(result)
                task2 = asyncio.create_task(send_result(args.session, result))     
                await task2  

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Process stream data into database & save file')
    parser.add_argument('--i', type=str, help='IP GRPC', default="127.0.0.1")
    parser.add_argument('--p', type=str, help='PORT GRPC', default="51111")
    parser.add_argument('--c', type=str, help='clientId', default="client0")
    parser.add_argument('--u', type=str, help='RTSP URL camera',default="0")
    parser.add_argument('--t', type=int, default=5 ,help='Interval time check')
    parser.add_argument('--session', type=str, help='Session is working')
    args = parser.parse_args()

    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    logFile = f'./logs/process_{args.c}.log'

    handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                    backupCount=1, encoding=None, delay=0)

    handler.setFormatter(log_formatter)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('root')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    asyncio.run(process(args, logger)) 
    # remove from redis if exist
    # redis_connection = CustomRedisClient.getInstance()
    # cfm = redis_connection.set_value(f"proc{args.process_id}", 0)
    logger.info('Finish process') 