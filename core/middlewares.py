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
