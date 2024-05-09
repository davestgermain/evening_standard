from django.contrib import admin
from shows.models import Show, Venue, Listen


class ListenAdmin(admin.ModelAdmin):
    list_display = ("start", "document", "ip_address", "referer")


admin.site.register(Venue)
admin.site.register(Show)
admin.site.register(Listen, ListenAdmin)
