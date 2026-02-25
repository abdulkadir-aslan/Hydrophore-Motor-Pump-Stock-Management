
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('homepage.urls')),
    path('', include('warehouses.urls')),
    path('', include('hydrophore.urls')),
    path('', include('other_materials.urls')),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)

handler404 = "homepage.views.page_not_found"
handler500 = "homepage.views.server_error"