import functools
import tornado.web
from tornado.gen import coroutine


def authenticated_token_async(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in raise HTTPError(403)
    """
    @functools.wraps(method)
    @coroutine
    def wrapper(self, *args, **kwargs):
        self._auto_finish = False
        self.token = yield self.validate_token()
        if not self.token:
            raise tornado.web.HTTPError(403)
        method(self, *args, **kwargs)
    return wrapper
