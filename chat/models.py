from sqlite3 import Timestamp
from tkinter import CASCADE
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    room = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.author.username
    def last_10_messages(room_name):
        return Message.objects.filter(room=room_name).order_by('-timestamp').all()[:10]

class Consumer(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username.username
    def fetch_users(room_name):
        return Consumer.objects.filter(room=room_name).order_by('-timestamp').all()