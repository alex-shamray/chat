from django.apps import apps as global_apps
from django.db import DEFAULT_DB_ALIAS


def create_persons(app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    """
    Create persons for users in all the installed apps.
    """
    from .models import Person

    models = [
        model for app_label, app_models in global_apps.all_models.items() for model_name, model in app_models.items()
        if hasattr(model, 'USERNAME_FIELD')
    ]

    for UserModel in models:
        for user in UserModel.objects.all():
            Person.objects.get_for_user(user)
