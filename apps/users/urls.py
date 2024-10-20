from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'users'
v1_router = DefaultRouter()
v1_router.register('v1', views.UserViewSet, basename='v1')

urlpatterns = [
    path('v1/sms_request/', views.sms_request, name='sms_request'),
]
urlpatterns += v1_router.urls
