from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['phone']


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(min_length=11, max_length=12)
    referral_code = serializers.CharField(read_only=True, source='referral_code.code')
    invited_users = UserShortSerializer(many=True, read_only=True)
    invited_by = UserShortSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'phone', 'referral_code', 'invited_users', 'invited_by', 'referral_code_used']


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


class ActivateReferralCodeSerializer(serializers.Serializer):
    referral_code = serializers.CharField(min_length=6, max_length=6)
    phone = serializers.CharField(min_length=11, max_length=12)

    def validate_code(self, code):
        if not get_user_model().objects.filter(referral_code__code=code).exists():
            raise serializers.ValidationError('Реферальный код не существует')
        return code

    def validate_phone(self, phone):
        if not get_user_model().objects.filter(phone=phone).exists():
            raise serializers.ValidationError('Пользователь не найден')

        if get_user_model().objects.get(phone=phone).referral_code_used:
            raise serializers.ValidationError('Вы уже активировали реферальный код')
        return phone
