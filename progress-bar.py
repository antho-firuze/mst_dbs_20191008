import threading
import time

def blackbox():
    print('abc')
    time.sleep(10)

thread = threading.Thread(target=blackbox)
thread.start()

eli_count = 0
while thread.is_alive():
    print('Sync', '.'*(eli_count+1), ' '*(2-eli_count), end='\r')
    eli_count = (eli_count + 1) % 3
    time.sleep(0.1)
thread.join()
print('Done      ')