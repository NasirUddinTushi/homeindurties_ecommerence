from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.account.urls')),
    path('api/', include('apps.products.urls')),
    path('api/', include('apps.cms.urls')),
    path('api/', include('apps.shop.urls')),
    path('api/', include('apps.reviews.urls')),
]
