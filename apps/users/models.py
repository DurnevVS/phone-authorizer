from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

import random
from string import ascii_letters, digits


class UserManager(UserManager):
    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The given phone must be set')

        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    email = None
    username = None
    first_name = None
    last_name = None

    phone = models.CharField(
        _('Номер телефона'),
        validators=[MinLengthValidator(11)],
        max_length=12,
        unique=True,
    )
    invited_by = models.ForeignKey(
        'self',
        verbose_name=_('Пригласивший'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invited_users',
    )
    invite_code_used = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.phone


def generate_referral_code():
    unique = False
    while not unique:
        code = ''.join(random.choices(ascii_letters + digits, k=6))
        unique = not UserReferralCode.objects.filter(code=code).exists()
    return code


class UserReferralCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referral_code')
    code = models.CharField(
        _('Реферальный код'),
        max_length=6,
        unique=True,
        default=generate_referral_code,
    )

    class Meta:
        verbose_name = _('Реферальный код')
        verbose_name_plural = _('Реферальные коды')

    def __str__(self):
        return f'{self.code}'


@receiver(post_save, sender=User)
def create_user_referral_code(sender, instance, created, **kwargs):
    if created:
        UserReferralCode.objects.create(user=instance)
