from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import UserReferralCode

admin.site.register(UserReferralCode)
admin.site.register(get_user_model())
