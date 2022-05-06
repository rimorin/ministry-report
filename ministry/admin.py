from django.contrib import admin
from ministry.models import Report as PubReport


class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ("creation_date", "last_change_date")


# Register your models here.
admin.site.register(PubReport, ReportAdmin)
