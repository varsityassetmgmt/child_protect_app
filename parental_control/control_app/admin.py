from django.contrib import admin


# admin.site.register(User)
# admin.site.register(RestrictedURL)

from django.contrib import admin
from .models import UserProfile, RestrictedURL

admin.site.register(UserProfile)
admin.site.register(RestrictedURL)