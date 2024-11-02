from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'users-v1'
router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('users/sms_request/', views.sms_request, name='sms_request'),
    path('users/activate_code/', views.activate_code, name='activate_code'),
    path('users/profile/', views.profile, name='profile'),
]
urlpatterns += router.urls
