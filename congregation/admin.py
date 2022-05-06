from django.contrib import admin
from congregation.models import Congregation, Group, Publisher

admin.site.register(Congregation, admin.ModelAdmin)
admin.site.register(Group, admin.ModelAdmin)
admin.site.register(Publisher, admin.ModelAdmin)
