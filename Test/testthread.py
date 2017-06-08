import threading
from time import sleep

class DemoThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while 1:
            print 'second passsed'
            sleep(1)

class SecondThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            print 'second thread'
            var = raw_input('press 1')
            if var == 1:
                print 'one pressed'
            else:
                print 'sleeping two'
                sleep(2)

DemoThread().start()
SecondThread().start()
