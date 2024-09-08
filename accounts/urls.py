from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts import views


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("signin/", views.signin, name='signin'),
    path("login/", views.login, name='login'),
    path("profile/", views.profile, name='profile'),
    path("<int:rollno>/", views.student, name='student')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)