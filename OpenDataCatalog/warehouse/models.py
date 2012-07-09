from django.contrib.auth.models import Group
from django.db import models


class Warehouse(models.Model):
    group = models.ForeignKey(Group)
    bucket_name = models.CharField(max_length=30)

    class Meta:
        permissions = (
                ('upload', 'Can upload files to the data warehouse'),
                )
