import tornado.web


class ValidationError(tornado.web.HTTPError):
    def __init__(self, status_code, error_messages, **kwargs):
        self.error_messages = error_messages
        super(ValidationError, self).__init__(status_code, **kwargs)
