from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts import views


urlpatterns = [
    path("signin/", views.signin, name='signin'),
    path("login/", views.login, name='login'),
    path("profile/", views.profile, name='profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)