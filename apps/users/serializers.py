from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(min_length=11, max_length=12)
    referral_code = serializers.CharField(read_only=True, source='referral_code.code')
    invited_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    invited_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['phone', 'referral_code', 'invited_users', 'invited_by']


class UserAuthSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(min_length=11, max_length=12)
    sms = serializers.CharField(write_only=True, min_length=4, max_length=4)

    def validate_sms(self, sms):
        if sms != self.context['request'].session.get('sms'):
            raise serializers.ValidationError('Код не совпадает')
        return sms

    class Meta:
        model = get_user_model()
        fields = ['phone', 'sms']


class SmSRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=11, max_length=12)
