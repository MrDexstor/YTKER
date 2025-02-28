from django.contrib import admin

from Core.models import TGUsers, Tags, UserTask

# Register your models here.
admin.site.register(TGUsers)
admin.site.register(Tags)
admin.site.register(UserTask)
