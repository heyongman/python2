import time


class Job:
    def __init__(self, args):
        self.args = args

    def run(self):
        for i in range(1, 11):
            self.args.append(i)
            time.sleep(3)
            print self.args


def start(args):
    # global global_arg
    # global_arg = args
    Job(args).run()
