from django.shortcuts import render
from django.contrib.auth import get_user_model
# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def profile(request):
    request.user = get_user_model().objects.filter(phone=request.GET.get('phone')).first()
    return render(request, 'main/profile.html')
