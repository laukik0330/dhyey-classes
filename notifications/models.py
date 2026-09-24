from django.db import models
from django.contrib.auth.models import User

from students.models import Student


class Notification(models.Model):

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        if self.student:
            return f"{self.title} - {self.student.name}"

        return f"{self.title} - All Students"