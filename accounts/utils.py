from accounts.models import CustomUser


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
        password=password,
    )
    user.save()

    return user
