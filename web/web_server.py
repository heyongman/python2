import web
import SimpleHTTPServer

urls = (
    '/(.*)', 'Web'
)

app = web.application(urls, globals())


class Web:
    def __init__(self):
        pass

    def GET(self, name):
        i = web.input(times=1)
        if not name:
            name = 'world'
        for c in xrange(int(i.times)):
            print 'Hello,', name + '!'
        return 'Hello, ' + name + '!'


if __name__ == "__main__":
    app.run()
