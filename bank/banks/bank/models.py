from django.db import models


class Password(models.Model):
    title = models.CharField(max_length=200)
    password = models.TextField(max_length=200)

    def __str__(self):
        return self.title