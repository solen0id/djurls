from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from djurls.shorty.models import ShortURL, User

admin.site.register(User, UserAdmin)
admin.site.register(ShortURL)
