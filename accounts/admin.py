from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Message

admin.site.register(User, UserAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'timestamp')
admin.site.register(Message, MessageAdmin)