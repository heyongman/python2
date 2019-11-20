import merge_scheduler.global_variable as gv
import test4
import threading
import time


class Job:

    def __init__(self):
        pass

    def test(self):
        index = 1
        while True:
            gv.set_value([{'a': index}])
            index += 1
            print gv.get_value()
            time.sleep(3)


if __name__ == '__main__':
    gv.init()
    threading.Thread(target=test4.start, args=(8080,)).start()
    threading.Thread(target=Job().test).start()
