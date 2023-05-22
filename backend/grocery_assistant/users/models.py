from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    class Meta:
        ordering = ("id",)

    @property
    def is_admin(self):
        return self.is_staff

    def __str__(self):
        return self.username[:15]


class Follow(models.Model):
    author = models.ForeignKey(
        CustomUser, related_name="following", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser, related_name="follower", on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("author", "user"), name="unique_follow"),
        )
