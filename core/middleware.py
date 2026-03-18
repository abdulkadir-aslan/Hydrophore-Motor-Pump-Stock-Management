from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Tüm view'lar için login kontrolü.
    İstisnalar exempt_urls listesinde.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse('login'),  # login sayfası
            '/admin/',         # admin panel
            '/static/',        # statik dosyalar
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if not any(path.startswith(url) for url in self.exempt_urls):
                return redirect('login')
        response = self.get_response(request)
        return response

import threading
_user_thread_local = threading.local()

def get_current_user():
    return getattr(_user_thread_local, 'user', None)

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user_thread_local.user = request.user
        response = self.get_response(request)
        return response