from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from events.models import *
from events.utils import *
from accounts.models import *
from events.constants import CLUBS_CHOICES


def add_event(request):
    if request.user.club_admin == "NORMAL":
        return redirect("/")

    if request.method == "POST":
        response = save_event(request)
        if response:
            messages.success(request, "Event Added!")
    return render(request, "events/addEvent.html", {"clubs": CLUBS_CHOICES})


def event_list(request):
    today = timezone.now().date()
    events = AllEventList.objects.filter(eventDate__gte=today)

    return render(
        request, "events/eventList.html", {"events": events, "clubs": CLUBS_CHOICES}
    )


def each_event(request, slug):
    user = request.user
    event = get_object_or_404(AllEventList, slug=slug)
    data = get_event_data_for_user(user=user, event=event)

    if request.method == "POST":
        if user.is_anonymous:
            return redirect("/login")

        handle_participation_posts(request, event)
        return redirect(request.path)

    return render(request, "events/eachEvent.html", {"event": data})


def handle_data(request):
    if request.user.club_admin == "NORMAL":
        return redirect("/")

    club = request.user.club_admin
    individualEvents = AllEventList.objects.filter(club=club, eventType="individual")
    teamEvents = AllEventList.objects.filter(club=club, eventType="team")

    if request.method == "POST" and "individual" in request.POST:
        if request.POST.get("event") == "all":
            data = individual_event_data(club, all=True)
        else:
            event = AllEventList.objects.get(eventName=request.POST.get("event"))
            data = individual_event_data(club, event=event)

        buffer = to_xlsx_buffer(data=data, eventType="individual")

        response = HttpResponse(
            buffer,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="data.xlsx"'

        return response

    if request.method == "POST" and "team" in request.POST:
        if request.POST.get("event") == "all":
            data = team_event_data(club, all=True)
        else:
            event = AllEventList.objects.get(eventName=request.POST.get("event"))
            data = team_event_data(club, event=event)

        buffer = to_xlsx_buffer(data=data, eventType="team")

        response = HttpResponse(
            buffer,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="data.xlsx"'

        return response

    if request.method == "POST" and "remove" in request.POST:
        eventName = request.POST.get("event")
        AllEventList.objects.get(eventName=eventName).delete()

    return render(
        request,
        "events/handle_data.html",
        {"individualEvents": individualEvents, "teamEvents": teamEvents},
    )
