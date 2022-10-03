from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "zium",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": 3306,
    }
}
