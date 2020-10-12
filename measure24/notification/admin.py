from django.contrib import admin

from measure24.notification.models import Words

import nested_admin


class NotificationWordsAdmin(nested_admin.NestedModelAdmin):
    fields = ['word', ]


admin.site.register(Words, NotificationWordsAdmin)
