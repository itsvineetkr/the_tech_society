from django.db.models import Count, Q
from events.models import *
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser


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
    return TeamsRegistration.objects.filter(event=event, teamLeader=user, status=1).exclude(user=user)


def membersInTeamIfJoined(user, event):
    if isJoined(user, event):
        teamName = TeamsRegistration.objects.get(event=event, user=user, status=1).teamName
        entries = TeamsRegistration.objects.filter(event=event, teamName=teamName).exclude(user=user)
        members =[]
        for i in entries:
            members.append(i.user)
        return members

def getTeams(user, event):
    if event.eventType != "team":
        return None

    allteams = TeamsRegistration.objects.filter(event=event)

    teams = []
    for i in allteams:
        if i.teamLeader == i.user:
            count = 1
            canAdd = True
            for j in allteams:
                if i.teamLeader == j.teamLeader and j.user == user:
                    canAdd = False
                if i.teamLeader == j.teamLeader and j.user != i.teamLeader and j.status == 1:
                    count += 1
            if canAdd:
                teams.append([i.teamName, i.teamLeader.name, i.teamLeader.email, i.teamLeader.rollno, count])

    print(teams)
    return teams


def getPendingReq(user, event):
    entries = TeamsRegistration.objects.filter(user=user, event=event)
    pendingRequests = list(entries.filter(status=0))
    if pendingRequests == []:
        return False
    return pendingRequests


def createTeam(user, event, teamName):
    entries = TeamsRegistration.objects.filter(user=user, event=event)
    pendingTeams = entries.filter(status=0)
    entries.delete()

    entryAsLeader = TeamsRegistration(
        event=event, teamLeader=user, teamName=teamName, user=user, status=1
    )
    entryAsLeader.save()
    return {"pendingTeams": pendingTeams}


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


def rollbackCondition(event):
    three_days_later = timezone.now() + timedelta(days=3)
    return event.eventDate >= three_days_later.date()
    

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
        "membersInTeamIfJoined": membersInTeamIfJoined(user=user, event=event),
        "teamJoinRequestsIfLeader": teamJoinRequestsIfLeader(user=user, event=event),
        "rollbackCondition": rollbackCondition(event)
    }   


def handleParticipationPosts(request, event):
    user = request.user

    # Individual Partcipation Posts

    if "participate_in_individual_event" in request.POST:
        IndividualEventRegistration(user=user, event=event).save()

    if "discard_individual_participation" in request.POST:
        IndividualEventRegistration.objects.filter(user=user, event=event).delete()


    # Team Participation Posts 


    if "discard_pending_requests" in request.POST:
        TeamsRegistration.objects.get(
            event = event,
            user = user,
            teamName = request.POST.get("discard_pending_requests")
        ).delete()

    if "create_team" in request.POST:
        teamName = request.POST.get("teamName_to_be_created")
        createTeam(user, event, teamName)

    if "join_team" in request.POST:
        teamName = request.POST.get("teamName")
        joinTeam(user, event, teamName)

    if "accept_request" in request.POST:
        userWantToJoin = request.POST.get("accept_request")
        entry = TeamsRegistration.objects.get(
            event=event, user=userWantToJoin, teamLeader=user
        )
        entry.status = 1
        entry.save()
        TeamsRegistration.objects.filter(event=event, user=userWantToJoin, status=0).delete()

    if "discard_team" in request.POST:
        TeamsRegistration.objects.filter(teamLeader=user, event=event).delete()

    if "leave_team" in request.POST:
        TeamsRegistration.objects.get(user=user, event=event, status=1).delete()

    if "remove_member" in request.POST:
        member = CustomUser.objects.get(rollno=request.POST.get("remove_member"))
        TeamsRegistration.objects.get(event=event, teamLeader=user, user=member).delete()

