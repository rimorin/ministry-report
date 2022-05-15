from django.contrib import admin
from congregation.models import Congregation, Group, Publisher
from ministry.models import Report


class ReportInline(admin.TabularInline):
    model = Report
    readonly_fields = (
        "hours",
        "placements",
        "videos",
        "return_visits",
        "bible_studies",
        "remarks",
    )
    can_delete = False
    extra = 0
    max_num = 0


class PubInline(admin.TabularInline):
    model = Publisher
    fields = ("id", "name", "status")
    readonly_fields = ("id", "name", "status")
    can_delete = False
    extra = 0
    max_num = 0


class PubAdmin(admin.ModelAdmin):
    inlines = [
        ReportInline,
    ]


class GroupAdmin(admin.ModelAdmin):
    inlines = [
        PubInline,
    ]


class GroupInline(admin.TabularInline):
    model = Group
    fields = ("id", "name")
    readonly_fields = ("id", "name")
    can_delete = False
    extra = 0
    max_num = 0


class CongAdmin(admin.ModelAdmin):
    inlines = [
        GroupInline,
    ]


admin.site.register(Congregation, CongAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Publisher, PubAdmin)
