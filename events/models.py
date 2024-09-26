from django.db import models
from django.utils import timezone
from django.conf import settings
from events.constants import EVENT_TYPE_CHOICES, STATUS_CHOICES, CLUBS_CHOICES
from django.urls import reverse


class AllEventList(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    eventName = models.CharField(max_length=100)
    eventDescription = models.TextField()
    eventImage = models.ImageField(upload_to="eventImages/")
    club = models.CharField(max_length=100, choices=CLUBS_CHOICES)
    location = models.CharField(max_length=100)
    coordinators = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    eventType = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES)
    eventDate = models.DateField()
    minTeamSize = models.IntegerField(default=1)
    maxTeamSize = models.IntegerField(default=1)
    dateAdded = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.eventName

    def get_absolute_url(self):
        return reverse("eachEvent", args=[self.slug])

    class Meta:
        ordering = ["-dateAdded"]


class IndividualEventRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(AllEventList, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event.eventName} | {self.user.name }"


class TeamsRegistration(models.Model):
    event = models.ForeignKey(AllEventList, on_delete=models.CASCADE)
    teamName = models.CharField(max_length=100)
    teamLeader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_lead_teams",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_registrations",
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.teamName
