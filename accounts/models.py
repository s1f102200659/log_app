from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.db import models
# from log_app.models import Kindergarten


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', '管理者'),
        ('caregiver', '保育士'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    kindergarten = models.ForeignKey(
        'log_app.Kindergarten',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'  # オプション: 逆参照名を設定
    )
    # 必要に応じて他のフィールドを追加

    def __str__(self):
        return self.username
