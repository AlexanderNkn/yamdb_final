from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


ROLE_CHOICES = (("user", "user"), ("moderator", "moderator"), ("admin", "admin"))


class User(AbstractUser):
    """
    A custom user model to customize it if the need arises.
    """

    bio = models.TextField(blank=True, null=True, verbose_name="description")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    # email required
    email = models.EmailField(_("email address"))
