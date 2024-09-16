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


def signup_user(request):
    email = request.POST.get("email")
    name = request.POST.get("name")
    rollno = request.POST.get("rollno")
    branch = request.POST.get("branch")
    year = request.POST.get("year")
    password = request.POST.get("password")
    if not password_validator(password):
        messages.error(request, "Enter valid password! It must contain at least 8 characters including digits and alphabets.")
        return None
    elif not email_validator(email):
        messages.error(request, "Enter valid email!")
        return None
    elif rollno > 1000000000000 and rollno < 9999999999999:
        messages.error(request, "Enter valid rollno")
        return None

    user = CustomUser(
        email=email,
        name=name,
        rollno=rollno,
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


def send_otp(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.get(email=email)
        if user:
            otp = generate_OPT()
            UserOTP.objects.create(email=email, otp=otp, created_at=timezone.now())
            send_otp_email(email, otp, user.name)
            request.session["email"] = email
            messages.success(
                request, "OTP sent to your mail. It will expire in 10 minutes."
            )
            return render(
                request,
                "accounts/forgotPassword.html",
                {
                    "sending_otp": False,
                    "verify_otp": True,
                    "password_change": False,
                },
            )
    except CustomUser.DoesNotExist:
        messages.error(request, "Enter a correct email address.")
        return render(
            request,
            "accounts/forgotPassword.html",
            {
                "sending_otp": True,
                "verify_otp": False,
                "password_change": False,
            },
        )


def verify_otp(request):
    otp = request.POST.get("otp")
    email = request.session.get("email")

    if not email:
        messages.error(request, "Session expired. Please try again.")
        return render(
            request,
            "accounts/forgotPassword.html",
            {
                "sending_otp": True,
                "verify_otp": False,
                "password_change": False,
            },
        )

    try:
        otp_record = UserOTP.objects.get(email=email, otp=otp)
        if otp_record.is_valid():
            messages.success(request, "OTP is valid. You can now reset your password.")
            return render(
                request,
                "accounts/forgotPassword.html",
                {
                    "sending_otp": False,
                    "verify_otp": False,
                    "password_change": True,
                },
            )
        else:
            messages.error(request, "OTP has expired.")
            return render(
                request,
                "accounts/forgotPassword.html",
                {
                    "sending_otp": True,
                    "verify_otp": False,
                    "password_change": False,
                },
            )
    except UserOTP.DoesNotExist:
        messages.error(request, "Invalid OTP.")
        return render(
            request,
            "accounts/forgotPassword.html",
            {
                "sending_otp": False,
                "verify_otp": True,
                "password_change": False,
            },
        )


def change_password(request):
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")
    email = request.session.get("email")

    if password != confirm_password:
        messages.error(request, "Passwords don't match!")
        return render(
            request,
            "accounts/forgotPassword.html",
            {
                "sending_otp": False,
                "verify_otp": False,
                "password_change": True,
            },
        )
    
    if not password_validator(password):
        messages.error(request, "Enter valid password! It must contain at least 8 characters including digits and alphabets.")

    try:
        user = CustomUser.objects.get(email=email)
        user.set_password(password)
        user.save()
        messages.success(request, "Password successfully changed.")
        del request.session["email"]
        return redirect("login")
    except CustomUser.DoesNotExist:
        messages.error(request, "An error occurred. Please try again.")
        return render(
            request,
            "accounts/forgotPassword.html",
            {
                "sending_otp": True,
                "verify_otp": False,
                "password_change": False,
            },
        )
