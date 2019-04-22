from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('index/', views.index),
    path('tuling/', views.tu_ling),
    path('func/', views.func),
    path('login/', views.login_view),
    path('acc_login/', views.acc_login),
    path('acc_logout/', views.acc_logout),
    ]+ static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    ) + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )