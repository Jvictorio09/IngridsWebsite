from django.shortcuts import redirect
from django.conf import settings

class WWWRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if not settings.DEBUG and host == 'ingridcruysberghs.com':
            return redirect('https://www.ingridcruysberghs.com' + request.get_full_path())
        return self.get_response(request)
