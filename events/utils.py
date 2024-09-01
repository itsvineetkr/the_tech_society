from events.models import *
from django.db.models import Count


def getEventList():
    """
    Args: No Args
    Return: Returns a list having all the data of events in form of dict.

    Structure of each dict:
        {
            'uniqueEventName': event.uniqueEventName,
            'eventName': event.eventName,
            'eventDiscription': event.eventDiscription,
            'eventImage': event.eventImage.url if event.eventImage else None,
            'location': event.location,
            'coordinators': event.coordinators,
            'contact': event.contact,
            'eventType': event.eventType,
            'minTeamSize': event.minTeamSize,
            'dateAdded': event.dateAdded,
            'teams': [(teamName, teamLeaderName, teamLeaderEmail, count)] if event.type == 'team' else None
        }
    """
    events = AllEventList.objects.all()
    data = []
    for event in events:
        data.append(
            {
                'uniqueEventName': event.uniqueEventName,
                'eventName': event.eventName,
                'eventDiscription': event.eventDiscription,
                'eventImage': event.eventImage.url if event.eventImage else None,
                'location': event.location,
                'coordinators': event.coordinators,
                'contact': event.contact,
                'eventType': event.eventType,
                'minTeamSize': event.minTeamSize,
                'dateAdded': event.dateAdded,
            }
        )

        if event.eventType == "team":
            teams = (
                TeamsRegistration.objects.filter(event=event)
                .select_related('teamLeader')  # Join the related model to access its fields
                .values('teamName', 'teamLeader__name', 'teamLeader__email')  # Include name and email
                .annotate(registration_count=Count('teamName'))
                .filter(registration_count__lt=event.maxTeamSize)
            )

            teams_list = list(teams.values_list('teamName', 'teamLeader__name', 'teamLeader__email', 'registration_count'))
            data[-1]["teams"] = teams_list
        
        else:
            data[-1]["teams"] = None

    return data

