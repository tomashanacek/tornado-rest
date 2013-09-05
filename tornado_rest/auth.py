import functools
import tornado.web
from tornado import stack_context
from tornado.gen import coroutine
from tornado.concurrent import Future
from tornado.ioloop import IOLoop


def authenticated_token_async(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in raise HTTPError(403)
    """
    @functools.wraps(method)
    @coroutine
    def wrapper(self, *args, **kwargs):
        self._auto_finish = False
        self.token = yield stack_context.run_with_stack_context(
            stack_context.ExceptionStackContext(
                self._stack_context_handle_exception),
            self.validate_token)
        if not self.token:
            raise tornado.web.HTTPError(403)

        with stack_context.ExceptionStackContext(
                self._stack_context_handle_exception):

            result = method(self, *args, **kwargs)

            if isinstance(result, Future):
                def future_complete(f):
                    f.result()
                    if not self._finished:
                        self.finish()
                IOLoop.current().add_future(result, future_complete)
    return wrapper
