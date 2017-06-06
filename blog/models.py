from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey('auth.User', related_name='user', on_delete=models.CASCADE, null=True)

    Hello_name = models.CharField(max_length=200 , blank=True, null=True)
    Task = models.TextField(max_length=200, blank=True, null=True)
    Phone_number = models.DecimalField(max_digits=11, decimal_places=0,  null=True)
    Weather = models.BooleanField(default=False)
    Traffic_jam = models.BooleanField(default=False)
    Currency = models.BooleanField(default=False)

    Date = models.DateTimeField(default=timezone.now)
    Time_send = models.DateTimeField( blank=True, null=True)

#DateTimeField(blank=True, null=True) #datetime.strftime(datetime.now(), "%H:%M")

    def __str__(self):
        return self.user
