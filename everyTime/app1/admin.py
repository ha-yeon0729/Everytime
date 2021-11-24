from django.contrib import admin
from .models import member
from .models import friend
from .models import excel_db

admin.site.register(member)
admin.site.register(friend)
admin.site.register(excel_db)