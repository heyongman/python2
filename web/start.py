import task
import flask_server
import threading

if __name__ == '__main__':
    global_arg = [1]

    threading.Thread(target=flask_server.start, name='flask', args=(global_arg,)).start()
    print 'web started.'
    threading.Thread(target=task.start, name='task', args=(global_arg,)).start()
    print 'task started.'


