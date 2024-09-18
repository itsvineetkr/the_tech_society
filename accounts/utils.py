import random
from accounts.models import CustomUser, UserOTP
from django.contrib import messages

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.utils import timezone
from django.shortcuts import render, redirect

from events.models import *


def signup_user(request):
    email = request.POST.get("email")
    name = request.POST.get("name")
    rollno = int(request.POST.get("rollno"))
    branch = request.POST.get("branch")
    year = request.POST.get("year")
    password = request.POST.get("password")
    phoneno = int(request.POST.get("phoneno"))

    if not password_validator(password):
        messages.error(
            request,
            "Enter valid password! It must contain at least 8 characters including digits and alphabets.",
        )
        return None
    elif not email_validator(email):
        messages.error(request, "Enter valid email!")
        return None
    elif phoneno > 9999999999 and phoneno < 5000000000:
        messages.error(request, "Enter valid phone number!")
        return None
    elif rollno < 1000000000000 and rollno > 9999999999999:
        messages.error(request, "Enter valid rollno!")
        return None

    user = CustomUser(
        email=email,
        name=name,
        rollno=rollno,
        phoneno=phoneno,
        branch=branch,
        year=year,
    )
    user.set_password(password)
    user.save()

    return user


def generate_OPT():
    return random.randint(100000, 999999)


def send_otp_email(email, otp, name):
    html_content = render_to_string(
        "accounts/otpTemplate.html", {"otp": otp, "name": name}
    )
    text_content = strip_tags(html_content)

    subject = "Your OTP Code to change password!"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()


def password_validator(password):
    length = 0
    specialChar = False
    numeric = False
    alpha = False
    for i in password:
        length += 1
        if i.isnumeric():
            numeric = True
            continue
        if i.isalpha():
            alpha = True
            continue
        specialChar = True

    if length >= 8 and numeric and alpha:
        return True
    return False


def email_validator(email):
    email_validator = EmailValidator()
    try:
        email_validator(email)
        return True
    except ValidationError:
        return False


def team_in_leader(user):
    teams = TeamsRegistration.objects.filter(
        teamLeader=user, user=user, event__eventDate__gte=timezone.now().date()
    )
    return teams if len(list(teams)) != 0 else False


def team_in_participated(user):
    teams = TeamsRegistration.objects.filter(
        user=user, status=1, event__eventDate__gte=timezone.now().date()
    ).exclude(teamLeader=user)
    return teams if len(list(teams)) != 0 else False


def team_pending_requests(user):
    teams = TeamsRegistration.objects.filter(
        user=user, status=0, event__eventDate__gte=timezone.now().date()
    )
    return teams if len(list(teams)) != 0 else False


def individual_participations(user):
    participations = IndividualEventRegistration.objects.filter(
        user=user, event__eventDate__gte=timezone.now().date()
    )
    return participations if len(list(participations)) != 0 else False


def user_participation_context(user):
    return {
        "teamInLeader": team_in_leader(user),
        "teamInParticipated": team_in_participated(user),
        "teamPendingRequest": team_pending_requests(user),
        "individualParticipations": individual_participations(user),
    }
