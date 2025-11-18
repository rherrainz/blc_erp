import threading

_thread_locals = threading.local()


class RequestMiddleware:
    """Middleware que guarda la request actual en thread-local.

    Permite acceder a la request y al user desde código que no recibe
    el objeto request (por ejemplo signals).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        return response


def get_current_request():
    return getattr(_thread_locals, 'request', None)


def get_current_user():
    req = get_current_request()
    if req is None:
        return None
    user = getattr(req, 'user', None)
    return user if user and user.is_authenticated else None
