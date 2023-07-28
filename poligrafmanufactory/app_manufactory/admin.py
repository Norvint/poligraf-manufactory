from django.contrib import admin

from app_manufactory.models import WorkCenter


@admin.register(WorkCenter)
class WorkCenterAdmin(admin.ModelAdmin):
    pass
