from rest_framework import serializers
from .models import User,Room,Reserve,Employee,Novelty



class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','password']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields='__all__'
        exclude=['user']
        
class NoveltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Novelty
        fields = '__all__'
        exclude=['employee']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['img','number','type','price_per_night','is_available','description']

class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        exclude=['user','room']

