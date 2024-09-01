from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from events import views


urlpatterns = [
    path("add-event/", views.addEvent, name='addEvent'),
    path("events/", views.eventList)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)