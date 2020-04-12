from django.db import models


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=52)
    email_id = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

class Kinder(models.Model):
    name = models.CharField(max_length=52)
    email_id = models.EmailField()
    regno = models.CharField(max_length=9)
    timetable = models.ImageField(upload_to='timetables/')

    def __str__(self):
        return self.name
