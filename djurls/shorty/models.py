from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F
from shorty.utils import encode_custom_base


class User(AbstractUser):
    pass


class ShortURL(models.Model):
    url = models.URLField(max_length=512)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    times_accessed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    accessed_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def short_key(self):
        return encode_custom_base(self.pk)

    def increment_accessed(self):
        self.times_accessed = F("times_accessed") + 1
        self.save()
