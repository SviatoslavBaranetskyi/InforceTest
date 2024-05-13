from django.utils import timezone

from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    description = models.TextField()

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    description = models.TextField()

    def __str__(self):
        return f"Menu for {self.restaurant.name} - {self.date}"


class Item(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name
