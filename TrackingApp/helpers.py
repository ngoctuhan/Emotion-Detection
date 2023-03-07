import os 
import signal
import shutil
LOG_PATH = "./logs/pid"
LOG_FILE = "./logs"

def kill_all_old_process():

    for item in os.listdir(LOG_FILE):
        if item.endswith(".log"):
            os.remove(os.path.join(LOG_FILE, item))

    if not os.path.exists(LOG_PATH):
        print("Not exist old process")
        return 
    for filename in os.listdir(LOG_PATH):
        file_path = os.path.join(LOG_PATH, filename)
        try:
            f = open(file_path, "r")
            pid = int(f.readline())
            os.kill(pid, signal.SIGKILL)
            print("Finish remove process: ", pid)
        except Exception as e:
            print(e)

def save_pid_is_running(list_proc):
    print(list_proc)
    try:
        shutil.rmtree(LOG_PATH) 
    except:
        pass 
    try:
        os.makedirs(LOG_PATH)
    except:
        pass
    for i, proc in enumerate(list_proc):
        with open(os.path.join(LOG_PATH, f"proc_{i}.txt"), 'w') as f:
            f.write(f"{list_proc[i].pid}")
