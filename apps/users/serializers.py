from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(read_only=True, source='user.referral_code')

    class Meta:
        model = get_user_model()
        fields = '__all__'
