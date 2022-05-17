from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json


def index(request):
    if request.user.is_authenticated:
        return render(request, 'chat/index.html', {})
    else:
        return redirect("login")

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': mark_safe(room_name),
        'username': mark_safe(request.user.username)
    })