from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

# Custom authentication backend that authenticates users based on their email
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Retrieve the user with the given email (username) and is_active=True
            user = UserModel.objects.get(email=username, is_active=True)
        except UserModel.DoesNotExist:
            # If no user is found, return None to indicate authentication failure
            return None
        else:
            # If a user is found, check if the provided password is correct
            if user.check_password(password):
                # If the password is correct, return the authenticated user
                return user
        # If the password is incorrect or no user is found, return None to indicate authentication failure
        return None
