import tornado.web
import tornado.ioloop
from settings import Settings
from views.index import IndexHandler
from auth.vk import VkAuthHandler


app_settings = {
    'debug': True,
    'template_path': './templates',
    'cookie_secret': 'jas7dKs8&d9cs9jj!090ksJU9*jsbg_hs'
}

application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/login/vk/?", VkAuthHandler, {'login_url': '/login/vk'}),
], **app_settings)

if __name__ == "__main__":
    application.listen(Settings.get('app')['port'])
    tornado.ioloop.IOLoop.instance().start()
