from .base import *

SECRET_KEY = env(
    "SECRET_KEY", default="ig3yfalmzd)@-t^j3ze6wiap^ihygqyt6)e4%-xrycvt9)@rbe"
)

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}
