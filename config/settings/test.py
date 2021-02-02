from .base import *

SECRET_KEY = env(
    "SECRET_KEY", default="ig3yfalmzd)@-t^j3ze6wiap^ihygqyt6)e4%-xrycvt9)@rbe"
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
