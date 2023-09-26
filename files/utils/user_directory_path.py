"""Defines user's files target folder"""
from datetime import datetime


def user_directory_path(instance, file):
    """Creates a date structured folder path"""

    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day
    return 'user_{0}/{1}/{2}/{3}/{4}'.format(
        instance.user.id,
        year,
        month,
        day,
        file
    )
