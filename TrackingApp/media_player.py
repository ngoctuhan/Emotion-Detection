import cv2 
from queue import Queue
import time
import threading

class Reader:
    
    FPS = 30
    WIDTH = 640
    HEIGHT = 480

    def __init__(self, camera_url) -> None:
        self.camera_url = int(camera_url)
        self.storage = Queue(maxsize=Reader.FPS)

    def start(self):

        print("Start a thread read RTSP camera")
        self.cap = cv2.VideoCapture(self.camera_url)
        # apply config for camera
        self.create_thread_pool()
    
    def create_thread_pool(self):
        thread_loading = threading.Thread(target=self.load_frame, args=())
        thread_loading.daemon = True 
        thread_loading.start()

    def load_frame(self):
        # Read until video is completed
        failed = 0
        frame_id = 0
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if ret == True:
                # Display the resulting frame
                self.storage.put(frame)
                frame_id = 0
            else: 
                failed += 1 
                time.sleep(0.01)
            if failed > Reader.FPS * 5:
                print("Reconnect to RTSP: ", self.camera_url)
                self.cap.release()
                cv2.destroyAllWindows()
                self.cap = cv2.VideoCapture(self.camera_url)
                failed = 0
            time.sleep(1)
            frame_id += 1 
            
    def get_frame(self):
        if not self.storage.empty():
            return self.storage.get()
        return None




        

