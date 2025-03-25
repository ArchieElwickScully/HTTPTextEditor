import multiprocessing.process
from multiprocessing import Queue
import time

class requestHandler(multiprocessing.Process):
    def __init__(self, queue):
        super().__init__()

        self.token = ''
        self.queue = queue
        print('request handler instantiated')

    def run(self):
        while True:
            if not self.queue.empty():
                task = self.queue.get()
                print(task)

if __name__ == '__main__':
    requestQueue = Queue()

    rh = requestHandler(requestQueue)
    rh.start()

    while True:
        time.sleep(3)
        requestQueue.put('test')
