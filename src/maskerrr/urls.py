from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mskr.urls')),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('sign_up/', views.sign_up, name='sign_up'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
