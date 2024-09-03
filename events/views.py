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

        if "ParticipateInIndividualEvent" in request.POST:
            IndividualEventRegistration(user=user, event=event).save()

        if "takeIndividualParticipationBack" in request.POST:
            IndividualEventRegistration.objects.filter(user=user, event=event).delete()

        if "joinTeam" in request.POST:
            teamName = request.POST.get("teamName")
            joinTeam(user, event, teamName)

        if "createTeam" in request.POST:
            teamName = request.POST.get("teamNameToBeCreated")
            createTeam(user, event, teamName)

        if "discardTeam" in request.POST:
            TeamsRegistration.objects.filter(teamLeader=user, event=event).delete()

        if "leaveTeam" in request.POST:
            TeamsRegistration.objects.filter(user=user, event=event, status=1).delete()

        if "acceptReq" in request.POST:
            userWantToJoin = request.POST.get("acceptReq")
            entry = TeamsRegistration.objects.get(
                event=event, user=userWantToJoin, teamLeader=user
            )
            entry.status = 1
            entry.save()

        return redirect("/events")

    return render(request, "events/eachEvent.html", {"event": data})
