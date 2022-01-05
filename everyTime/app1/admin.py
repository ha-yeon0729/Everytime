from django.contrib import admin
from .models import member
from .models import friend

admin.site.register(member)
admin.site.register(friend)