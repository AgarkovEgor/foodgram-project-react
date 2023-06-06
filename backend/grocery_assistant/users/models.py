from django.contrib.auth.models import AbstractUser
from django.db import models

LEN_USERNAME = 15


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Юзернейм пользователя"
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия"
    )
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name="Электронная почта"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    

    @property
    def is_admin(self):
        return self.is_staff

    def __str__(self):
        return self.username[:LEN_USERNAME]


class Follow(models.Model):
    author = models.ForeignKey(
        CustomUser, 
        related_name="following", 
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    user = models.ForeignKey(
        CustomUser, 
        related_name="follower", 
        on_delete=models.CASCADE,
        verbose_name="Подписчик"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ['-id']
        constraints = (
            models.UniqueConstraint(fields=("author", "user"), name="unique_follow"),
        )
    def __str__(self):
        return (f'Пользователь {self.user} '
                f'подписан на автора {self.author}')    
