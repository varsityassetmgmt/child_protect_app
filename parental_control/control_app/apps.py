from django.apps import AppConfig




class ControlAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'control_app'

    def ready(self):
        import control_app.signals