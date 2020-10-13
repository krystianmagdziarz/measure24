from django.contrib import admin

from measure24.notification.models import Words, Mentions

import nested_admin


class NotificationWordsAdmin(nested_admin.NestedModelAdmin):
    fields = ['word', ]


class NotificationMentionsAdmin(nested_admin.NestedModelAdmin):
    fields = ['word', 'message', 'permalink', 'used']


admin.site.register(Words, NotificationWordsAdmin)
admin.site.register(Mentions, NotificationMentionsAdmin)
