from django.contrib.auth.backends import ModelBackend


class PasswordChangeRequiredBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)

        if user and user.needs_password_change:
            user.needs_password_change = False
            user.save()

        return user
