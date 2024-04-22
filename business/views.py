from rest_framework import viewsets
from .serializers import RoomSerializer,ReserveSerializer,UserSerializer,NoveltySerializer#UserLoginSerializer
from .models import Room,Reserve,Novelty
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework_simplejwt import tokens
from django.shortcuts import get_object_or_404
from .models import User
#from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class UserAuthViews(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset=User.objects.all()
    serializer_class=UserSerializer
    
    '''def get_object(self,pk):
        try: 
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND'''
            
    @action(detail=False,methods=['POST'])
    def register_user(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password=serializer.validated_data.get('password')
            user=serializer.save()
            user.set_password(password)
            user.save()
            
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False,methods=['POST'])
    def login_user(self,request, *args, **kwargs):
        username=request.data.get("username")
        password=request.data.get("password")
        log = authenticate(username=username,password=password)
        print(request.data)
        if log is not None:
            refresh=tokens.RefreshToken.for_user(log)
            serializer=UserSerializer(log)
            return_data={'user':serializer.data,'tokens':{'refresh':str(refresh),'access':str(refresh.access_token)}}
            return Response(return_data,status=status.HTTP_200_OK)
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    
    '''@action(detail=False,methods=['POST'])
    def login_user(self,request, *args, **kwargs):
        user=get_object_or_404(User,username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({'error':'Invalid Password'},status=status.HTTP_400_BAD_REQUEST)
        token=tokens.RefreshToken.for_user(user)
        serializer=UserSerializer(user)
        return Response({'refresh':str(token),'access':str(token.access_token),'user':serializer.data},status=status.HTTP_200_OK)'''
        
class RoomViews(viewsets.ModelViewSet):
    permission_classes=[IsAdminUser]
    queryset=Room.objects.all()
    serializer_class=RoomSerializer
    @swagger_auto_schema(
        operation_summary='Crear Habitacion',
        request_body=RoomSerializer,
        responses={201:RoomSerializer()}
    )
    
    def create(self, request, *args, **kwargs):
        serializer=RoomSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_406_NOT_ACCEPTABLE)
    
    @swagger_auto_schema(
        operation_summary='Listar Habitaciones',
        responses={200:RoomSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        rooms=Room.objects.all()
        serializer=RoomSerializer(rooms,many=True)   
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary='Actualizar Habitacion',
        responses={202:RoomSerializer()}
    )
    def update(self, request, *args, **kwargs):
        room=self.get_object()
        serializer=RoomSerializer(room,data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary='Quitar Habitacion',
        responses={404:RoomSerializer()}
    )
    def destroy(self, request, *args, **kwargs):
        room=self.get_object()
        self.perform_destroy(room)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        operation_summary="Lista de Habitaciones",
        responses={200:RoomSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        queryset=Room.objects.all()
        serializer=RoomSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ReserveViews(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Reserve.objects.all()
    serializer_class=ReserveSerializer

class NoveltyViews(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset=Novelty.objects.all()
    serializer_class=NoveltySerializer