from django.shortcuts import render
from .models import TwitterUser

# Create your views here.


def index(request):
    return render(request, 'index.html', {'user': request.user})


def edit_profile(request):
    pass
