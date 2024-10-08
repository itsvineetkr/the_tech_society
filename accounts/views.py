from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, get_backends
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.utils import timezone
from accounts.backends import EmailBackend
from accounts.models import CustomUser, UserOTP
from django.urls import reverse
from accounts.utils import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import os


def homepage(request):
    return render(request, "homepage/homepage.html")

@require_POST
def mark_notifications_as_seen(request):
    if request.user.is_authenticated:
        NotificationSeenStatus.objects.filter(user=request.user, seen=False).update(seen=True)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=401)


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

    context = user_participation_context(request.user)
    context["user"] = request.user
    return render(request, "accounts/profile.html", context=context)


def student(request, rollno):
    if rollno == request.user.rollno:
        return redirect("/profile")
    student = get_object_or_404(CustomUser, rollno=rollno)

    context = user_participation_context(student)
    context["student"] = student

    return render(request, "accounts/student.html", context=context)


def forgot_password(request):
    if request.method == "POST":
        if "sending_otp" in request.POST:
            email = request.POST.get("email")
            try:
                user = CustomUser.objects.get(email=email)
                if user:
                    otp = generate_OPT()
                    UserOTP.objects.filter(email=email).delete()
                    UserOTP.objects.create(
                        email=email, otp=otp, created_at=timezone.now()
                    )
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

        if "verify_otp" in request.POST:
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
                    messages.success(
                        request, "OTP is valid. You can now reset your password."
                    )
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

        if "password_change" in request.POST:
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
                messages.error(
                    request,
                    "Enter valid password! It must contain at least 8 characters including digits and alphabets.",
                )
                return render(
                    request,
                    "accounts/forgotPassword.html",
                    {
                        "sending_otp": False,
                        "verify_otp": False,
                        "password_change": True,
                    },
                )

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

    return render(
        request,
        "accounts/forgotPassword.html",
        {"sending_otp": True, "verify_otp": False, "password_change": False},
    )


@login_required
def update_profile(request):
    if request.method == "POST":
        update_profile_post(request)
        return redirect("profile")

    return render(request, "accounts/updateProfile.html")
