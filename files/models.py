"""Files app models

The interesting feature here is the if statement filters for empty directories
that are leaves on the filesystem tree. os.removedirs() deletes all empty folders
in above an empty leaf. If there are several empty leaves on a branch,
deleting the last empty leaf will cause os.removedirs() to walk up the branch.
So all empty dirs are gone in a single iteration of the loop with no recursion necessary!
"""
import os
from pathlib import Path

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from files.utils.user_directory_path import user_directory_path


class File(models.Model):
    """The main files table"""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file_name = models.CharField(max_length=50, null=False, blank=False)
    file = models.FileField(upload_to=user_directory_path)
    headers = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    status = models.CharField(max_length=8, default="new")


@receiver(pre_delete, sender=File)
def remove_file(**kwargs):
    """Removes files from media folder"""

    # file is being deleted itself from containing folder
    # folder stays alive
    instance = kwargs.get('instance')
    instance.file.delete(save=False)
    # if one of media's folders gets empty, it is removed too
    try:
        for p in Path("media").glob('**/*'):
            if p.is_dir() and len(list(p.iterdir())) == 0:
                os.removedirs(p)
    except FileNotFoundError:
        pass
