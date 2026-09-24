from django.db import models

from batches.models import Batch


class Student(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    parent_name = models.CharField(
        max_length=100
    )

    parent_phone = models.CharField(
        max_length=15
    )

    batch = models.ForeignKey(
        Batch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )

    profile_image = models.ImageField(
        upload_to='student_profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name