"""Files app models

The interesting feature here is the if statement filters for empty directories
that are leaves on the filesystem tree. os.removedirs() deletes all empty folders
in above an empty leaf. If there are several empty leaves on a branch,
deleting the last empty leaf will cause os.removedirs() to walk up the branch.
So all empty dirs are gone in a single iteration of the loop with no recursion necessary!
"""
import os
from datetime import datetime
from pathlib import Path

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


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


@receiver(pre_delete, sender=File)
def remove_file(**kwargs):
    """Removes files from media folder"""

    # db record clearance
    instance = kwargs.get('instance')
    instance.file.delete(save=False)
    # media folder empty dirs clearance
    try:
        for p in Path("media").glob('**/*'):
            if p.is_dir() and len(list(p.iterdir())) == 0:
                os.removedirs(p)
    except FileNotFoundError:
        pass
