from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts import views


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("signup/", views.signup, name='signup'),
    path("login/", views.loginUser, name='login'),
    path("logout/", views.logoutUser, name='logout'),
    path("profile/", views.profile, name='profile'),
    path("<int:rollno>/", views.student, name='student'),
    path("forgetpassword/", views.forgetPassword, name='forgetPassword')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)