from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from events import views


urlpatterns = [
    path("add-event/", views.add_event, name='addEvent'),
    path("events/", views.event_list, name="eventList"),
    path('events/<slug:slug>/', views.each_event, name='eachEvent'),
    path('handle-data/', views.handle_data, name='handleData')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)