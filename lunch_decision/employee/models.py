from django.db import models
from django.contrib.auth.models import User
from restaurant.models import Menu


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=15, unique=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Vote(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('menu', 'employee')

    def __str__(self):
        return f"{self.employee.user.username} voted for {self.menu}"
