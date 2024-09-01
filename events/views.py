from django.shortcuts import render, redirect
from events.models import *
from events.utils import getEventList
from accounts.models import *


def addEvent(request):
    if request.method == "POST":
        uniqueEventName = request.POST.get("uniqueEventName")
        eventName = request.POST.get("eventName")
        eventDiscription = request.POST.get("eventDiscription")
        eventImage = request.FILES.get("eventImage")
        location = request.POST.get("location")
        coordinators = request.POST.get("coordinators")
        contact = int(request.POST.get("contact"))
        eventType = request.POST.get("eventType")
        maxTeamSize = request.POST.get("maxTeamSize")
        minTeamSize = request.POST.get("minTeamSize")

        maxTeamSize = maxTeamSize if maxTeamSize else 1
        minTeamSize = minTeamSize if minTeamSize else 1

        event = AllEventList(
            uniqueEventName=uniqueEventName,
            eventName=eventName,
            eventDiscription=eventDiscription,
            eventImage=eventImage,
            location=location,
            coordinators=coordinators,
            contact=contact,
            eventType=eventType,
            maxTeamSize=maxTeamSize,
            minTeamSize=minTeamSize
        )

        event.save()

    return render(request, "events/addEvent.html")


def eventList(request):
    user = request.user
    if request.method == 'POST':
        if user.is_anonymous:
            return redirect('/login')
        
        if 'individualRegister' in request.POST:
            uniqueEventName = request.POST.get("eventName")
            event = AllEventList.objects.get(uniqueEventName = uniqueEventName)
            entry = IndividualEventRegistration(user = user, event = event)
            entry.save()
        
        if 'teamEvent' in request.POST:
            uniqueEventName = request.POST.get("eventName")
            event = AllEventList.objects.get(uniqueEventName = uniqueEventName)
            teamParticipateType = request.POST.get("teamParticipateType")
            
            if teamParticipateType == 'createTeam':
                team = TeamsRegistration(
                    event = event,
                    teamName = request.POST.get("teamNameCreate"),
                    teamLeader = user,
                    user = user,
                    status = 1
                )
                team.save()
            
            else:
                teamName = request.POST.get("teamParticipateType")
                teamLeader = TeamsRegistration.objects.filter(teamName = teamName)[0].teamLeader

                entry = TeamsRegistration(
                    event = event,
                    teamName = teamName,
                    teamLeader = teamLeader,
                    user = user,
                    status = 0
                )
                entry.save()
    events = getEventList()
    return render(request, "events/eventList.html", {"events": events})



"""
event add kewal admin kar paye
event count me status 0 wale na include ho
ek leader ki ek event me ek hi team hogi
ek team me banda ek hi baar ja skta hai dubara vo team show na ho
team leader ko koi team show na kyunki vo khud participated as leader of a team hai (usko aana hai to profile me jake naam pichhe le)
individual me bhi participate karne ke baad participate ki button na dikhe



"""