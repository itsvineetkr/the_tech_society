from accounts.models import *


def notifications_processor(request):
    notifications = []
    user = request.user
    if user.is_authenticated:
        userNotifications = UserSpecificNotification.objects.filter(user=user)
        globalNotifications = NotificationForAll.objects.all()
        notifications = userNotifications.union(globalNotifications).order_by(
            "-timeStamp"
        )

    return {"notifications": notifications}
