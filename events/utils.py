from django.db.models import Count, Q
from events.models import *


def saveEvent(request):
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
        slug=uniqueEventName,
        eventName=eventName,
        eventDiscription=eventDiscription,
        eventImage=eventImage,
        location=location,
        coordinators=coordinators,
        contact=contact,
        eventType=eventType,
        maxTeamSize=maxTeamSize,
        minTeamSize=minTeamSize,
    )
    event.save()


def canParticipateInIndividualEvent(user, event):
    if event.eventType == "individual":
        entry = list(IndividualEventRegistration.objects.filter(event=event, user=user))
        if entry == []:
            return True
    return False


def isLeader(user, event):
    if event.eventType == "team":
        leaderEntries = list(
            TeamsRegistration.objects.filter(event=event, teamLeader=user, user=user)
        )
        if leaderEntries != []:
            return leaderEntries[0]
    return False


def isJoined(user, event):
    if event.eventType == "team":
        userConfirmEntry = list(
            TeamsRegistration.objects.filter(event=event, user=user, status=1)
        )
        if userConfirmEntry != []:
            if userConfirmEntry[0].teamLeader == user:
                return []
            return userConfirmEntry[0]
    return False

def membersInTeamIfLeader(user, event):
    members = list(TeamsRegistration.objects.filter(event = event, teamLeader = user))
    return len(members)-1

def getTeams(user, event):
    if event.eventType != "team":
        return None

    teams = TeamsRegistration.objects.filter(event=event).exclude(teamLeader=user)
    teams = teams.annotate(accepted_count=Count("id", filter=Q(status=1))).filter(
        accepted_count__lt=event.maxTeamSize
    )
    teams = teams.exclude(
        teamName__in=TeamsRegistration.objects.filter(
            user=user, event=event
        ).values_list("teamName", flat=True)
    )
    available_teams = teams.values_list(
        "teamName", "teamLeader__name", "teamLeader__email", "accepted_count"
    )

    if isLeader(user, event) or isJoined(user, event):
        return []

    return list(available_teams)


def getEventDataForUser(user, event):
    return {
        "uniqueEventName": event.uniqueEventName,
        "eventName": event.eventName,
        "eventDiscription": event.eventDiscription,
        "eventImage": event.eventImage.url if event.eventImage else None,
        "location": event.location,
        "coordinators": event.coordinators,
        "contact": event.contact,
        "eventType": event.eventType,
        "minTeamSize": event.minTeamSize,
        "dateAdded": event.dateAdded,
        "teams": getTeams(user, event),
        "canParticipateInIndividualEvent": canParticipateInIndividualEvent(user, event),
        "isLeader": isLeader(user=user, event=event),
        "isJoined": isJoined(user=user, event=event),
        "membersInTeamIfLeader": membersInTeamIfLeader(user=user, event=event)
    }


def createTeam(user, event, teamName):
    entries = TeamsRegistration.objects.filter(user=user)
    entries.delete()

    entryAsLeader = TeamsRegistration(
        event=event, teamLeader=user, teamName=teamName, user=user, status=1
    )
    entryAsLeader.save()
