from django.db import models
from django.contrib.auth.models import User
import uuid

class StartupIdea(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='startup_images/', null=True, blank=True)
    business_model = models.TextField(blank=True)
    value_proposition = models.TextField(blank=True)
    target_audience = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)
    original_idea = models.ForeignKey('self',null=True,blank=True,on_delete=models.SET_NULL,related_name='variants')
    list_display = ('id', 'user', 'short_description', 'created_at', 'has_original')

def has_original(self, obj):
    return bool(obj.original_idea)
