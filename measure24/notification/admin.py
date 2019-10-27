import nested_admin
from django.contrib import admin
from .models import Words


class NotificationWordsAdmin(nested_admin.NestedModelAdmin):
    fields = ['word', ]


admin.site.register(Words, NotificationWordsAdmin)