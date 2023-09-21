"""Files app models"""

from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models


def user_directory_path(instance, file):
    """Prepares a path to save file in date structured folder"""

    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day
    return 'user_{0}/{1}/{2}/{3}/{4}'.format(instance.user.id, year, month, day, file)


class File(models.Model):
    """The main files table"""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file_name = models.CharField(max_length=50, null=False, blank=False)
    file = models.FileField(upload_to=user_directory_path)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    status = models.CharField(max_length=8, default="new")
