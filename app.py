import tornado.web
import tornado.ioloop
from settings import Settings
from auth.vk import VkAuthHandler


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("fooo")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/vk/login/?", VkAuthHandler, {'login_url': '/vk/login'}),
])

if __name__ == "__main__":
    application.listen(Settings.get('app')['port'])
    tornado.ioloop.IOLoop.instance().start()
