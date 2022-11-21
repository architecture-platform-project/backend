from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("MYSQL_DATABASE"),
        "USER": "root",
        "PASSWORD": os.environ.get("MYSQL_ROOT_PASSWORD"),
        "HOST": "mysql",
        "PORT": 3306,
    }
}
