from django.shortcuts import render, redirect, get_object_or_404
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
    event = get_object_or_404(AllEventList, slug=slug)
    user = request.user
    data = getEventDataForUser(user=user, event=event)

    if request.method == "POST":
        if user.is_anonymous:
            return redirect("/login")

        if "individualEvent" in request.POST:
            uniqueEventName = request.POST.get("eventName")
            event = AllEventList.objects.get(uniqueEventName=uniqueEventName)
            entry = IndividualEventRegistration(user=user, event=event)
            entry.save()
            return redirect("/events")

        if "teamEvent" in request.POST:
            uniqueEventName = request.POST.get("eventName")
            event = AllEventList.objects.get(uniqueEventName=uniqueEventName)
            teamParticipateType = request.POST.get("teamParticipateType")

            if teamParticipateType == "createTeam":
                teamName = request.POST.get("teamNameCreate")
                createTeam(user, event, teamName)

            else:
                teamName = request.POST.get("teamParticipateType")
                teamLeader = TeamsRegistration.objects.filter(teamName=teamName)[
                    0
                ].teamLeader

                entry = TeamsRegistration(
                    event=event,
                    teamName=teamName,
                    teamLeader=teamLeader,
                    user=user,
                    status=0,
                )
                entry.save()
            return redirect("/events")

    return render(request, "events/eachEvent.html", {"event": data})


"""
event count me status 0 wale na include ho
ek leader ki ek event me ek hi team hogi
ek team me banda ek hi baar ja skta hai dubara vo team show na ho
team leader ko koi team show na kyunki vo khud participated as leader of a team hai (usko aana hai to profile me jake naam pichhe le)
individual me bhi participate karne ke baad participate ki button na dikhe



"""

"""
individual event wale me bas itna karo ki utils wale me le jao control aur vahan save karo
discardTeam and leaveTeam ke liye banana hai

requests dekhne ke liye bhi yahin par karo eachEvent me
"""
