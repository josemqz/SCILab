# Prueba de threading

import threading
import time
import sys

# deprecated
class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  stop_event, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        # self._stop_event = threading.Event()
        self._stop_event = stop_event

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

""" 
# TEST #
###############

running1 = False
running2 = False
running3 = False

def thread_function1(name, input_event, lock):
    global running1
    print(f"{name} waiting for input...")
    a = input()
    # input_event.wait()  # Wait for input event to be set
    if len(a) > 0:
            
        print(f"{name} received input. Starting method...")

        with lock:
            running1 = True
            # Your thread's method goes here
            for i in range(5):
                print(f"{name}: Step {i + 1}")
                time.sleep(1)
            
            running1 = False

def thread_function2(name, input_event, lock):
    global running2
    print(f"{name} waiting for input...")
    input_event.wait()  # Wait for input event to be set
    print(f"{name} received input. Starting method...")

    with lock:
        running2 = True
        # Your thread's method goes here
        for i in range(5):
            print(f"{name}: Step {i + 1}")
            time.sleep(1)
        
        running2 = False

def thread_function3(name, input_event, lock):
    global running3
    print("Thread waiting for input...")
    input_event.wait()  # Wait for input event to be set
    print("Thread received input. Starting method...")

    with lock:
        running3 = True
        # Your thread's method goes here
        for i in range(5):
            print(f"{name}: Step {i + 1}")
            time.sleep(1)
        
        running3 = False


# Create a lock
lock = threading.Lock()

event1 = threading.Event()
event2 = threading.Event()
event3 = threading.Event()

thread1 = StoppableThread(event1, target=thread_function1, args=("Thread 1", event1, lock))
thread2 = StoppableThread(event2, target=thread_function2, args=("Thread 2", event2, lock))
thread3 = StoppableThread(event3, target=thread_function3, args=("Thread 3", event3, lock))


while 1:
    try:

        # Simulate input from different sources
        time.sleep(2)
        event1.set()  # Signal Thread 1 to start
        # time.sleep(2)
        # event2.set()  # Signal Thread 2 to start
        time.sleep(1)

        if not thread1.is_alive():
            print("creating new instance thread1")
            event1.clear()
            event1 = threading.Event()
            thread1 = StoppableThread(event1, target=thread_function1, args=("Thread 1", event1, lock))
            thread1.start()

        if not thread2.is_alive():
            print("creating new instance thread2")
            event2.clear()
            event2 = threading.Event()
            thread2 = StoppableThread(event2, target=thread_function2, args=("Thread 2", event2, lock))
            thread2.start()
        
        if not thread3.is_alive():
            print("creating new instance thread3")
            event3.clear()
            event3 = threading.Event()
            thread3 = StoppableThread(event3, target=thread_function3, args=("Thread 3", event3, lock))
            thread3.start()
        
        time.sleep(1)

        event3.set()

        print("loop.")

    except KeyboardInterrupt:
        print("Sending stop signal to threads...")
        thread1.stop()
        thread2.stop()
        thread3.stop()
        print("leaving program")
        sys.exit()
"""