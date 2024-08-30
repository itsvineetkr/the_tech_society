from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from events import views


urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)