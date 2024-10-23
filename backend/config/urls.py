from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('channels.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('channels/', include('channels.urls')),
]
