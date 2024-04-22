from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    photo=models.ImageField()
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=50)
    
class Employee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    overlap=models.CharField(max_length=10)
    
class Novelty(models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    img=models.ImageField(upload_to='')
    description=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    
class Room(models.Model):
    img=models.ImageField(upload_to='')
    number=models.IntegerField()
    type=models.CharField(max_length=20)
    price_per_night=models.FloatField()
    is_available=models.BooleanField(default=True)
    description=models.TextField()

    def __str__(self) -> str:
        return '{}  ({})'.format(self.number,self.description)
    
class Reserve(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    price=models.FloatField()


 