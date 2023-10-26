from django.contrib import admin
from . import models



class SetSongInline(admin.TabularInline):
    model = models.SetSong
    extra = 1


class SetListAdmin(admin.ModelAdmin):
    inlines = (SetSongInline,)


admin.site.register(models.Song)
admin.site.register(models.SetList, SetListAdmin)
