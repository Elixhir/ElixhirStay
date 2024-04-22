from django.contrib import admin
from django.urls import path
from .views import RoomViews,ReserveViews,NoveltyViews,UserAuthViews
from rest_framework import routers

route=routers.DefaultRouter()
route.register(r'reserve',ReserveViews)
route.register(r'novelty',NoveltyViews)

urlpatterns = [
    path('room/',RoomViews.as_view({"get":"list","post":"create"})),
    path('room/<int:pk>/',RoomViews.as_view({"get":"retrieve","put":"update","delete":"destroy"})),
    path('register/',UserAuthViews.as_view({"post":"register_user"}), name='register'),
    path('login/',UserAuthViews.as_view({"post":"login_user"}, name='login'))
] + route.urls

