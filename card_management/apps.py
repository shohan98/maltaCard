from django.apps import AppConfig


class CardManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'card_management'
    
    def ready(self):
        """Import signals when app is ready"""
        import card_management.signals
