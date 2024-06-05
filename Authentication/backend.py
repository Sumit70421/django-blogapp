from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class FileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            with open('credentials.txt', 'r') as f:
                for line in f:
                    saved_username, saved_password = line.strip().split(',')
                    if saved_username == username and saved_password == password:
                        try:
                            user = User.objects.get(username=username)
                        except User.DoesNotExist:
                            # Create a new user object if it doesn't exist
                            user = User(username=username)
                        return user
        except FileNotFoundError:
            pass

        return None