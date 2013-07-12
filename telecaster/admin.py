from models import *
from django.contrib import admin


class StationAdmin(admin.ModelAdmin):
    model = Station
    search_fields = ['public_id', 'id']

admin.site.register(Station, StationAdmin)

