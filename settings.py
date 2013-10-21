try:
    from settings_local import apply_settings_local
except ImportError:
    apply_settings_local = lambda x: x

settings = {
    'app': {
        'base_url': 'http://localhost',
        'port': 8888
    },
    'auth': {
        'vk': {
            'client_id': '',
            'client_secret': ''
        }
    }
}


class Settings(object):

    @classmethod
    def get(cls, name=None):
        if not hasattr(cls, '_settings'):
            cls._settings = apply_settings_local(settings)
        if name is None:
            return cls._settings
        else:
            return cls._settings.get(name, None)
