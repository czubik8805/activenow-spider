class BaseNotificationBackend:
    def __init__(self, message, subject=""):
        self.message = message
        self.subject = subject

    def run(self):
        raise NotImplementedError
