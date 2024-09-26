from django.contrib import admin
from accounts.models import *


admin.site.register(CustomUser)
admin.site.register(UserOTP)
admin.site.register(NotificationSeenStatus)
admin.site.register(NotificationForAll)
admin.site.register(UserSpecificNotification)