from collections.abc import Iterable
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(default = "", null = False, unique=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse("chat-room", kwargs={"slug": self.slug})
    

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete = models.CASCADE)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_on', )

    def __str__(self):
        return self.message
    