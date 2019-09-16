from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=128, unique=True)
    user_pwd = models.CharField(max_length=256)
    user_email = models.EmailField(unique=True)

    def __str__(self):
        return self.user_name