from grpc_libs.ai_client import PersonGrpcClient
import argparse
import cv2, numpy as np
import time 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Face Client')
    parser.add_argument('--ip', default="localhost", type=str,
                      help='Ip address of the server')
    parser.add_argument('--port', default=51111, type=int,
                      help='expose port of gRPC server')
    args = parser.parse_args()
    client = PersonGrpcClient(args.ip, args.port)
    test = cv2.imread("dependencies/1.jpg")
    res =  client.detection(test)
    boxes, labels, probs = res 
    t = time.time()
    for box in boxes:
        # cv2.rectangle(test, (box[0], box[1]), (box[2], box[3]), (255, 128, 0), 4)
        crop_image = test[box[1]:box[3], box[0]: box[2]]
        res = client.check_emotion(crop_image)
        print(res)
    print(time.time() - t)
        # cv2.imshow('img', crop_image)
        # cv2.waitKey(1000)
   