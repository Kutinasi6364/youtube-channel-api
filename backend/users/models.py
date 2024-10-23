from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # ユーザー名, メールアドレス, パスワード以外の追加項目
    bio = models.TextField(null=True, blank=True) # ユーザープロフィール情報
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)


    def __str__(self):
        return self.username