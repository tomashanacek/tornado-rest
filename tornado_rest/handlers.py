import tornado.web
import errors
import validation
from raven.contrib.tornado import SentryMixin
from tornado.gen import coroutine


class BaseHandler(SentryMixin, tornado.web.RequestHandler):

    def prepare(self):
        self._json = None

    @property
    def json(self):
        if self._json is None:
            try:
                self._json = tornado.escape.json_decode(self.request.body)
            except ValueError as e:
                raise tornado.web.HTTPError(400, e.message)
        return self._json

    def write_error(self, status_code, **kwargs):
        error_messages = None
        if "exc_info" in kwargs:
            exception = kwargs["exc_info"][1]
            if isinstance(exception, errors.ValidationError) and \
                    exception.error_messages:

                    error_messages = exception.error_messages

        if error_messages:
            self.write({"errors": error_messages})
            self.finish()
        else:
            super(BaseHandler, self).write_error(status_code, **kwargs)

    @coroutine
    def validate_token(self):
        """Override to determine the token from, e.g., a database."""
        return

    def validate_arguments(self, validate_class):
        arguments = dict(
            (key, self.get_argument(key))
            for key in self.request.arguments)
        return validation.validate(arguments, validate_class)

    def validate_body(self, validate_class):
        return validation.validate(self.json, validate_class)
