from api_ import crawl_thesis_info
from threading import Thread
import time


class ThesisThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            print(crawl_thesis_info())
            time.sleep(3600*24)

if __name__ == '__main__':
    test = ThesisThread()
    test.start()
    test.join()
