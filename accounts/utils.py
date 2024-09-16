from accounts.models import CustomUser
import random
from django.core.mail import send_mail
from django.conf import settings


def signupUser(request):
    email = request.POST.get("email")
    name = request.POST.get("name")
    rollno = request.POST.get("rollno")
    branch = request.POST.get("branch")
    year = request.POST.get("year")
    password = request.POST.get("password")
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


def generateOPT():
    return random.randint(100000, 999999)


def send_otp_email(user_email, otp):
    subject = "Your OTP for Password Reset"
    message = f"Hello Student,\nYour One-Time Password (OTP) for resetting your password is {otp}. It will expire in 10 minutes.\nThank you."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
