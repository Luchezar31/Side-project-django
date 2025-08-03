from django.contrib.auth.models import AbstractUser
from django.db import models


class ForumAppUser(AbstractUser):
    points = models.IntegerField(
        null=True,
        blank=True
    )


