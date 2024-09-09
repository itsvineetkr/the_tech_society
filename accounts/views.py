from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import SignInForm
from django.contrib.auth import logout, authenticate, get_backends
from django.contrib.auth import login as auth_login
from accounts.backends import EmailBackend
from accounts.models import CustomUser
from django.urls import reverse
import os


def homepage(request):
    return render(request, "homepage/homepage.html")


def signup(request):
    if request.method == "POST":
        form = SignInForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = SignInForm()

    return render(request, "accounts/signup.html", {"form": form})


def loginUser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            backend = get_backends()[0]
            auth_login(request, user, backend="accounts.backends.EmailBackend")
            return redirect("profile")
        else:
            return render(
                request, "accounts/login.html", {"error": "Invalid email or password."}
            )
    return render(request, "accounts/login.html")


def logoutUser(request):
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
