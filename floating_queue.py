# start out by taking out the priority queue. Can we get it to do jobs in a list.
# Then add cancel job function
# then add a priority queue instead of queue and find a place for reheap. Likely gonna be in the add_job function.

import threading
import time
import queue

def thread_target():
    print("From inside thread target")
    time.sleep(5)
    print("leaving thread target")

def infinite_thread():
    print("in the infinity thread")
    # while True:
    time.sleep(5)
    print("left the infinite thread. Not really infinite rn.")

class FloatingQueue(threading.Thread):
    def __init__(self, num_workers):
        threading.Thread.__init__(self)
        self.is_running = True
        self.workers = None
        self.job_queue = queue.Queue()
        self.num_workers = num_workers
        self.lock = threading.Lock()

    def run(self):
        workers = [threading.Thread(target=self._worker) for _ in range(self.num_workers)]

        for worker in workers:
            worker.start()
            print("worker started")

        while self.is_running:
            if self.job_queue.empty() :
                time.sleep(5)
                print("\nawaiting jobs")

    def _worker(self):
        while self.is_running:
            try:
                job = self.job_queue.get(timeout=1)
                job.start()
            except queue.Empty:
                #print("passing over an empty jobs list.")
                continue
        
        print("worker has been passed through")

    def add_job(self, target):
        self.job_queue.put(threading.Thread(target=target))

    def shutdown(self):
        self.is_running = False


# the main program.

if __name__ == "__main__":

    q1 = FloatingQueue(1)
    
    q1.start()
    print("main thread started")
    # time.sleep(5)

    # q1.add_job(thread_target)
    # q1.add_job(thread_target)
    # q1.add_job(infinite_thread)
    # q1.add_job(thread_target)
    

    # print(q1.job_queue)
    # q1.add_job(thread_target)
    # print(q1.job_queue)

    while q1.is_running:
        command = input("1, 0, or 2(shutdown): ")
        try:
            command = int(command)
        except Exception as e:
            command = 4
        print(command)
        if command == 1:
            q1.add_job(thread_target)
        elif command == 0:
            q1.add_job(infinite_thread)
        elif command == 2:
            q1.shutdown()
            print("shutting down")
        else:
            print("whaaaaaat")

    print("weewaooo")
    q1.join()
    

