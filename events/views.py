from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from events.models import *
from events.utils import *
from accounts.models import *
from events.constants import CLUBS_CHOICES


def addEvent(request):
    if request.user.club_admin == "NORMAL":
        return redirect("/")

    if request.method == "POST":
        saveEvent(request)

    return render(request, "events/addEvent.html", {"clubs": CLUBS_CHOICES})


def eventList(request):
    events = AllEventList.objects.all()
    return render(request, "events/eventList.html", {"events": events, "clubs": CLUBS_CHOICES})


def eachEvent(request, slug):
    user = request.user
    event = get_object_or_404(AllEventList, slug=slug)
    data = getEventDataForUser(user=user, event=event)

    if request.method == "POST":
        if user.is_anonymous:
            return redirect("/login")

        handleParticipationPosts(request, event)
        return redirect(request.path)

    return render(request, "events/eachEvent.html", {"event": data})
