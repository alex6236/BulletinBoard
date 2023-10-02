from django.apps import AppConfig


class MainBoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main_board'
    verbose_name = 'Доска объявлений'
    
    def ready(self):
        import apps.main_board.signals
