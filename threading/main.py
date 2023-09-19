import threading
import turtle as t
import time

def count(countTo):
    for x in range(countTo):
        print(x)
        time.sleep(.1)

t1 = threading.Thread(target=count, args=(100,))
t1.start()