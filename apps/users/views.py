from rest_framework import viewsets
from django.contrib.auth import get_user_model


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
