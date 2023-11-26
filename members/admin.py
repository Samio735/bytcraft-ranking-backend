from django.contrib import admin

# Register your models here.

from .models import Member , Department , Activities 

admin.site.register(Member)
admin.site.register(Department)
admin.site.register(Activities)