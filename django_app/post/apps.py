from django.apps import AppConfig


class PostConfig(AppConfig):
    name = 'post'

    def ready(self):
        # Makes sure all signal handlers are connected
        from . import handlers  # noqa
