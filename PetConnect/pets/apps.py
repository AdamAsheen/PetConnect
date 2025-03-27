from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db import IntegrityError


class PetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pets'

    def ready(self):
        import pets.signals
        from .models import Category


        def create_general_category(sender, **kwargs):
            if not Category.objects.filter(category_name="General").exists():
                try:
                    Category.objects.create(category_name="General")
                    print("General category created")
                except IntegrityError:
                    pass
        
        post_migrate.connect(create_general_category, sender=self)