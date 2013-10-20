from settings_local import apply_settings_local

settings = {
    'app': {
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
