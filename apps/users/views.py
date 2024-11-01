import random
import time
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest

from .serializers import UserSerializer, UserAuthSerializer, SmSRequestSerializer, ActivateReferralCodeSerializer


@api_view(['POST'])
def sms_request(request: HttpRequest):
    serializer = SmSRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    time.sleep(2)
    sms = ''.join([str(random.randint(0, 9)) for _ in range(4)])

    request.session['sms'] = sms
    request.session.save()

    return Response({'sms': sms}, status=status.HTTP_200_OK)


@api_view(['POST'])
def activate_code(request: HttpRequest):
    serializer = ActivateReferralCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = get_user_model().objects.get(phone=serializer.validated_data['phone'])
    referral_code = user.refferal_code
    user.invited_by = get_user_model().objects.filter(refferal_code=referral_code).first()
    user.referral_code_used = True
    user.save()

    return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserAuthSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        user, created = get_user_model().objects.get_or_create(phone=serializer.validated_data['phone'])
        if not created:
            return Response({'token': user.auth_token.key}, status=status.HTTP_200_OK, headers=headers)

        token = Token.objects.create(user=user).key
        return Response({**serializer.data, 'token': token}, status=status.HTTP_201_CREATED, headers=headers)
