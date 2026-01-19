from django.http import HttpResponse


def administrator(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.authorization == "1":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Bu sayfaya erişim izniniz yok.')

    return wrapper_function

def admin(view_func):
    def wrapper_function(request, *args, **kwargs):
        if (request.user.authorization == "1") or (request.user.authorization == "2") :
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Bu sayfaya Erişim izniniz bulunmamaktadır.')
    
    return wrapper_function

def employe_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if (request.user.authorization == "1") or (request.user.authorization == "2") or (request.user.authorization == "3"):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('Bu sayfaya Erişim izniniz bulunmamaktadır.')
    
    return wrapper_function

