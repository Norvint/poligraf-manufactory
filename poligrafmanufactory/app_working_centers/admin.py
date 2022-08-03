from django.contrib import admin

from app_working_centers.models import WorkingCenter, WorkingCenterNode


class WorkingCenterNodesInLine(admin.TabularInline):
    model = WorkingCenterNode


@admin.register(WorkingCenter)
class WorkingCenterAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title']
    inlines = [WorkingCenterNodesInLine]


@admin.register(WorkingCenterNode)
class WorkingCenterNodeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'work_center']
    list_filter = ['work_center',]
