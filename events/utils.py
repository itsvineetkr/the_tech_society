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
    club = request.POST.get("club")
    maxTeamSize = request.POST.get("maxTeamSize")
    minTeamSize = request.POST.get("minTeamSize")
    eventDate = request.POST.get("eventDate")
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
        club=club,
        eventDate=eventDate,
        maxTeamSize=maxTeamSize,
        minTeamSize=minTeamSize,
    )
    event.save()


def individualTeamParticipation(user, event):
    if event.eventType == "individual":
        entry = list(IndividualEventRegistration.objects.filter(event=event, user=user))
        if entry != []:
            return entry[0]
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
    members = list(TeamsRegistration.objects.filter(event=event, teamLeader=user))
    return len(members) - 1


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
        "teamName", "teamLeader__name", "teamLeader__email", "teamLeader__rollno", "accepted_count"
    )

    if isLeader(user, event) or isJoined(user, event):
        return []

    return list(available_teams)


def getPendingReq(user, event):
    entries = TeamsRegistration.objects.filter(user=user, event=event)
    pendingRequests = list(entries.filter(status=0))
    if pendingRequests == []:
        return False
    return pendingRequests


def createTeam(user, event, teamName):
    entries = TeamsRegistration.objects.filter(user=user, event=event)
    joinedTeams = entries.filter(status=1)
    pendingTeams = entries.filter(status=0)
    entries.delete()

    entryAsLeader = TeamsRegistration(
        event=event, teamLeader=user, teamName=teamName, user=user, status=1
    )
    entryAsLeader.save()
    return {"joinedTeams": joinedTeams, "pendingTeams": pendingTeams}


def joinTeam(user, event, teamName):
    teamLeader = TeamsRegistration.objects.filter(teamName=teamName)[0].teamLeader
    entry = TeamsRegistration(
        event=event,
        teamName=teamName,
        teamLeader=teamLeader,
        user=user,
        status=0,
    )
    entry.save()


def teamJoinRequestsIfLeader(user, event):
    requests = list(
        TeamsRegistration.objects.filter(teamLeader=user, event=event, status=0)
    )
    return False if requests == [] else requests


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
        "maxTeamSize": event.maxTeamSize,
        "dateAdded": event.dateAdded,
        "eventDate": event.eventDate,
        "teams": getTeams(user, event),
        "individualTeamParticipation": individualTeamParticipation(user, event),
        "isLeader": isLeader(user=user, event=event),
        "isJoined": isJoined(user=user, event=event),
        "isPending": getPendingReq(user, event),
        "membersInTeamIfLeader": membersInTeamIfLeader(user=user, event=event),
        "teamJoinRequestsIfLeader": teamJoinRequestsIfLeader(user=user, event=event),
    }


def handleParticipationPosts(request, event):
    user = request.user

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
