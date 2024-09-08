from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from events.models import *
from events.utils import *
from accounts.models import *


def addEvent(request):
    if not request.user.is_staff:
        return redirect("/")

    if request.method == "POST":
        saveEvent(request)

    return render(request, "events/addEvent.html")


def eventList(request):
    events = AllEventList.objects.all()
    return render(request, "events/eventList.html", {"events": events})


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
