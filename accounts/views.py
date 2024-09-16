from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, get_backends
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.utils import timezone
from accounts.backends import EmailBackend
from accounts.models import CustomUser, UserOTP
from django.urls import reverse
from accounts.utils import *
import os


def homepage(request):
    return render(request, "homepage/homepage.html")


def signup(request):
    if request.method == "POST":
        user = signup_user(request)
        if user:
            auth_login(request, user, backend="accounts.backends.EmailBackend")
            messages.success(request, "User Registration Successful!")
            return redirect(reverse("homepage"))
    return render(request, "accounts/signup.html")


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user, backend="accounts.backends.EmailBackend")
            return redirect("profile")
        else:
            messages.error(request, "Incorrect email address or password.")
            return render(request, "accounts/login.html")
    return render(request, "accounts/login.html")


def logout_user(request):
    logout(request)
    return redirect(reverse("homepage"))


def profile(request):
    user = request.user
    if user.is_anonymous:
        return redirect("/login")

    if request.method == "POST":
        image = request.FILES.get("profile_picture")

        if image:
            if user.profile_picture:
                old_image_path = user.profile_picture.path
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
            user.profile_picture = image
            user.save()
            return redirect("/profile")

    return render(request, "accounts/profile.html", {"user": user})


def student(request, rollno):
    if rollno == request.user.rollno:
        return redirect("/profile")
    studentData = get_object_or_404(CustomUser, rollno=rollno)
    return render(
        request, "accounts/student.html", context={"studentData": studentData}
    )


def forgot_password(request):
    if request.method == "POST":
        if "sending_otp" in request.POST:
            send_otp(request)

        if "verify_otp" in request.POST:
            verify_otp(request)

        if "password_change" in request.POST:
            change_password(request)

    return render(
        request,
        "accounts/forgotPassword.html",
        {"sending_otp": True, "verify_otp": False, "password_change": False},
    )
