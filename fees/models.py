from django.db import models
from students.models import Student


class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    due_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.total_amount}"