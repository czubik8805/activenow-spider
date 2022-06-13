import os

from .email import EmailBackend
from .telegram import TelegramBackend


def get_notification_backend():
    return {
        "email": EmailBackend,
        "telegram": TelegramBackend,
    }.get(os.getenv("NOTIFICATION_BACKEND", "telegram"))
