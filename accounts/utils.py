from accounts.models import *
from django.contrib import messages

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from django.utils import timezone
from django.shortcuts import render, redirect

import os
import random
from events.models import *
from PIL import Image


def rollno_validator(rollno):
    """
    Validates the roll number.

    Args: rollno (int): The roll number to validate.
    Returns: bool: True if the roll number is between 13 digits, False otherwise.
    """

    return rollno > 1000000000000 and rollno < 9999999999999


def phoneno_validator(phoneno):
    """
    Validates the phone number.

    Args: phoneno (int): The phone number to validate.
    Returns: bool: True if the phone number is valid, False otherwise.
    """

    return phoneno < 9999999999 and phoneno > 5000000000


def signup_user(request):
    """
    Handles user signup by validating email, rollno, phoneno, and password.
    Saves the user if all fields are valid.

    Args: request (HttpRequest): The HTTP request containing POST data.
    Returns: CustomUser: The created user object, or None if validation fails.
    """

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
    elif not phoneno_validator(phoneno):
        messages.error(request, "Enter valid phone number!")
        return None
    elif not rollno_validator(rollno):
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

    # if rollno == 2300521520054:
    #     user.profile_picture = "profile_pics/r.jpg"

    user.set_password(password)
    user.save()

    NotificationSeenStatus(user=user).save()

    return user


def generate_OPT():
    """
    Generates a 6-digit random OTP.

    Returns: int: A random 6-digit number.
    """

    return random.randint(100000, 999999)


def send_otp_email(email, otp, name):
    """
    Sends an OTP email with the provided OTP and name using the email template.

    Args:
        email (str): The recipient's email address.
        otp (int): The one-time password to send.
        name (str): The recipient's name.

    Returns: None
    """

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
    """
    Validates the password to ensure it has at least 8 characters, including digits and letters.

    Args: password (str): The password to validate.
    Returns: bool: True if the password meets the criteria, False otherwise.
    """

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
    """
    Validates the email format using Django's EmailValidator.

    Args: email (str): The email to validate.
    Returns: bool: True if the email format is valid, False otherwise.
    """

    email_validator = EmailValidator()
    try:
        email_validator(email)
        return True
    except ValidationError:
        return False


def team_in_leader(user):
    """
    Returns the teams where the user is the team leader and the event is upcoming.

    Args: user (CustomUser): The user to check for.
    Returns: QuerySet or bool: A QuerySet of teams if the user is a leader in upcoming events, False if no teams are found.
    """

    teams = TeamsRegistration.objects.filter(
        teamLeader=user, user=user, event__eventDate__gte=timezone.now().date()
    )
    return teams if len(list(teams)) != 0 else False


def team_in_participated(user):
    """
    Returns the teams where the user has participated in upcoming events (but is not the team leader).

    Args: user (CustomUser): The user to check for.
    Returns: QuerySet or bool: A QuerySet of teams if the user has participated, False if no teams are found.
    """

    teams = TeamsRegistration.objects.filter(
        user=user, status=1, event__eventDate__gte=timezone.now().date()
    ).exclude(teamLeader=user)
    return teams if len(list(teams)) != 0 else False


def team_pending_requests(user):
    """
    Returns pending team requests for the user in upcoming events.

    Args: user (CustomUser): The user to check for.
    Returns: QuerySet or bool: A QuerySet of pending team requests, False if none are found.
    """

    teams = TeamsRegistration.objects.filter(
        user=user, status=0, event__eventDate__gte=timezone.now().date()
    )
    return teams if len(list(teams)) != 0 else False


def individual_participations(user):
    """
    Returns the individual participations for the user in upcoming events.

    Args: user (CustomUser): The user to check for.
    Returns: QuerySet or bool: A QuerySet of individual participations, False if none are found.
    """

    participations = IndividualEventRegistration.objects.filter(
        user=user, event__eventDate__gte=timezone.now().date()
    )
    return participations if len(list(participations)) != 0 else False


def user_participation_context(user):
    """
    Gathers the user's participation context in teams and individual events.

    Args: user (CustomUser): The user to gather participation data for.
    Returns: dict: A dictionary containing the user's participation details in teams and individual events.
    """

    return {
        "teamInLeader": team_in_leader(user),
        "teamInParticipated": team_in_participated(user),
        "teamPendingRequest": team_pending_requests(user),
        "individualParticipations": individual_participations(user),
    }


def update_profile_post(request):
    """
    Handles profile update requests, including image compression for profile pictures.
    Updates user details if provided and valid.

    Args: request (HttpRequest): The HTTP request containing POST data and files.
    Returns: None
    """

    user = request.user

    name = request.POST.get("name")
    rollno = request.POST.get("rollno")
    phoneno = request.POST.get("phoneno")
    branch = request.POST.get("branch")
    year = request.POST.get("year")

    if "profile_picture" in request.FILES:
        profile_picture = request.FILES["profile_picture"]

        image = Image.open(profile_picture)

        max_size = (900, 900)
        image.thumbnail(max_size)

        temp_path = f"/tmp/{profile_picture.name}"
        if image.format == "JPEG":
            image.save(temp_path, "JPEG", quality=75, optimize=True)
        elif image.format == "PNG":
            image.save(temp_path, "PNG", optimize=True)
        else:
            image.save(temp_path)

        if user.profile_picture:
            old_image_path = user.profile_picture.path
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

        with open(temp_path, "rb") as compressed_image_file:
            profile_picture.name = (
                str(user.rollno) + "." + profile_picture.name.split(".")[-1]
            )
            user.profile_picture.save(profile_picture.name, compressed_image_file)

        os.remove(temp_path)

    if name and user.name != name:
        user.name = name

    if rollno and user.rollno != int(rollno) and rollno_validator(int(rollno)):
        user.rollno = int(rollno)

    if phoneno and user.phoneno != int(phoneno) and phoneno_validator(int(phoneno)):
        user.phoneno = int(phoneno)

    if branch and user.branch != branch:
        user.branch = branch

    if year and user.year != year:
        user.year = year

    user.save()


def push_notification(notification, user=None):
    if user:
        UserSpecificNotification(user=user, notification=notification).save()
        NotificationSeenStatus.objects.get(user=user).seen = False
        return None

    NotificationForAll(notification=notification).save()
    NotificationSeenStatus.objects.update(seen=False)
