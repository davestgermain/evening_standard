from django.contrib import admin
from wagtail.images.models import Image

from . import models


def num_charts(song):
    return song.charts.count()


num_charts.short_description = "Number of Charts"


def num_songs(setlist):
    return setlist.songs.count()


num_songs.short_description = "Number of Songs"


class SetSongInline(admin.TabularInline):
    model = models.SetSong
    extra = 1


class SetListAdmin(admin.ModelAdmin):
    inlines = (SetSongInline,)
    list_display = ("title", num_songs)


class SongAdmin(admin.ModelAdmin):
    autocomplete_fields = ["charts"]
    list_display = ["title", num_charts]

    fields = [
        "title",
        "charts",
        "key",
        "notes",
    ]


class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]


def better_str(self):
    tags = ", ".join(str(t) for t in self.tags.all())
    return f"{self.title} ({tags})"


Image.__str__ = better_str

admin.site.unregister(Image)
admin.site.register(Image, ImageAdmin)
admin.site.register(models.Song, SongAdmin)
admin.site.register(models.SetList, SetListAdmin)
