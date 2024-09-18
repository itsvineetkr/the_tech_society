from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from events.models import *
from events.utils import *
from accounts.models import *
from events.constants import CLUBS_CHOICES


def add_event(request):
    if request.user.club_admin == "NORMAL":
        return redirect("/")

    if request.method == "POST":
        save_event(request)
        messages.success(request,"Event Added!")
    return render(request, "events/addEvent.html", {"clubs": CLUBS_CHOICES})


def event_list(request):
    today = timezone.now().date()
    events = AllEventList.objects.filter(eventDate__gte=today)
    return render(request, "events/eventList.html", {"events": events, "clubs": CLUBS_CHOICES})


def each_event(request, slug):
    user = request.user
    event = get_object_or_404(AllEventList, slug=slug)
    data = get_event_data_for_user(user=user, event=event)

    if request.method == "POST":
        if user.is_anonymous:
            return redirect("/login")

        handle_participation_posts(request, event)
        return redirect(request.path)

    return render(request, "events/eachEvent.html", {"event": data})
