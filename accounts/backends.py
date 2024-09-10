from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Fetch user by email
            user = UserModel.objects.get(email=email)
            # Validate password and ensure user is active
            if user.is_staff:
                if user.check_password(password) and user.is_active:
                    return user
            else:
                if user.password == password and user.is_active:
                    return user
        except UserModel.DoesNotExist:
            return None
        return None