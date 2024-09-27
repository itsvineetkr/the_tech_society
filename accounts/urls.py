from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from accounts import views


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("signup/", views.signup, name='signup'),
    path("login/", views.login_user, name='login'),
    path("logout/", views.logout_user, name='logout'),
    path("profile/", views.profile, name='profile'),
    path("<int:rollno>/", views.student, name='student'),
    path("forgotpassword/", views.forgot_password, name='forgotPassword'),
    path("updateProfile/", views.update_profile, name='updateProfile'),
    path('notifications/mark-seen/', views.mark_notifications_as_seen, name='mark_notifications_as_seen'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)