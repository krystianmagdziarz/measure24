import nested_admin
from django.contrib import admin
from configuration.models import Configuration


class ConfigurationAdmin(nested_admin.NestedModelAdmin):
    fields = ['name', 'active', 'sentry_sdk']


admin.site.register(Configuration, ConfigurationAdmin)
