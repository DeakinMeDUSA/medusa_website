from .production import *  # Need starred import here to import all vars so that celery can find tasks

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"}},
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "logfile": {
            "class": "logging.FileHandler",
            "filename": str(ROOT_DIR / "logs/celery_server.log"),
            "level": "INFO",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console", "logfile"]},
    "loggers": {
        "django": {
            "handlers": ["logfile", "logfile"],
        },
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console", "logfile"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console", "logfile"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
