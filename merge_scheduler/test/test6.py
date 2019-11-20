import threading
import time
import os
import json


class Job:
    def __init__(self, *kw):
        self.index = 1
        print kw

    def loop(self):
        for i in range(3):
            if i == 2:
                self.loop()
            print i
        print 'loop'

    def check(self):
        print self.index
        try:
            if self.index == 1 or self.index == 2 or self.index == 3:
                print 'first if'
                self.index += 1
                time.sleep(3)
                return self.check()
            # elif self.index == 2:
            #     return True
            elif self.index == 4:
                print 'second if'
                return False
        except Exception as e:
            print e

    def status(self):
        with open('./test.json','r') as f:
            j = json.load(f)
            print j[0]


if __name__ == '__main__':
    Job(1, 2).status()
