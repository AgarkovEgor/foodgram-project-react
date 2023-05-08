from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
   
    @property
    def is_admin(self):
        return self.is_staff


class Follow(models.Model):
    author = models.ForeignKey(
        CustomUser,
        related_name='following',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser,
        related_name='follower',
        on_delete=models.CASCADE
    )
    class Meta:
        constraints = (models.UniqueConstraint(
            fields=('author', 'user'), name='unique_follow'),)