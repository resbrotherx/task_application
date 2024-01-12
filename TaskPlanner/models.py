from django.db import models
from django.db import models
from PIL import Image
from django.db.models import Max
from django.forms import DateTimeField
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# User = settings.AUTH_USER_MODEL
UserModel = get_user_model()



PRIYORITY_CHOICE = (
    ("medium", "Medium"),
    ("low", "Low"),
    ("high", "High"),
)


# Create your models here.
class Task(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    shared_with = models.ManyToManyField(User, related_name='received_tasks', blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField()
    due_time = models.TimeField()
    emoji = models.CharField(max_length=1, blank=True, null=True)
    emotion_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    pri_status = models.CharField(
        choices=PRIYORITY_CHOICE, max_length=30, default="medium")
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.title}'



class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    reciepient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def sender_message(from_user, to_user, body):
        sender_message = Messages(
            user=from_user,
            sender = from_user,
            reciepient = to_user,
            body = body,
            is_read = True
            )
        sender_message.save()
    
        reciepient_message = Messages(
            user=to_user,
            sender = from_user,
            reciepient = from_user,
            body = body,
            is_read = True
            )
        reciepient_message.save()
        return sender_message

    def get_message(user):
        users = []
        messages = Messages.objects.filter(user=user).values('reciepient').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': UserModel.objects.get(pk=message['reciepient']),
                'last': message['last'],
                'unread': Messages.objects.filter(user=user, reciepient__pk=message['reciepient'], is_read=False).count()
            })
        return users
