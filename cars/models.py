from django.db import models

# Create your models here.

class Car(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    age = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id', 'title', 'brand', 'price', 'age',)