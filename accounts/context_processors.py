from accounts.models import *


def notifications_processor(request):
    notifications = []
    user = request.user
    seen = True
    if user.is_authenticated:
        seen = NotificationSeenStatus.objects.get(user=user).seen
        user_notifications = UserSpecificNotification.objects.filter(user=user).values(
            "notification", "timeStamp", "notificationType" 
        )

        global_notifications = NotificationForAll.objects.all().values(
            "notification", "timeStamp", "notificationType"
        )
        notifications = user_notifications.union(global_notifications).order_by(
            "-timeStamp"
        )
    
    return {"notifications": notifications, "seen": seen}
