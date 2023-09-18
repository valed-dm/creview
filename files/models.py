from django.contrib.auth import get_user_model
from django.db import models


# from model_utils import Choices


# class UserFile(models.Model):
#     STATUS = Choices("new", "reloaded", "deleted")
#
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     fpath = models.CharField(max_length=300)
#     status = models.CharField(choices=STATUS, default=STATUS.new, max_length=8)


class File(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/%Y/%m/%d')
