from django.db import models
from django.conf import settings

from uuid import uuid4

from hasher.hasher import Hasher


class Workspace(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hashed_value = models.CharField(db_index=True, default=Hasher.hash())
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='joined_workspaces')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Workspace'
        verbose_name_plural = 'Workspaces'

    def __str__(self):
        return f'{self.name}'
