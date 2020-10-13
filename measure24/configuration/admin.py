import nested_admin

from django.contrib import admin
from measure24.configuration.models import Configuration
from solo.admin import SingletonModelAdmin


admin.site.register(Configuration, SingletonModelAdmin)
