from django.contrib import admin
from wagtail.images.models import Image
from wagtail.documents.models import Document

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
    autocomplete_fields = ["song"]


class SetListAdmin(admin.ModelAdmin):
    inlines = (SetSongInline,)
    list_display = ("title", num_songs)


class SongAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    autocomplete_fields = ["charts", "recordings"]
    list_display = ["title", num_charts]

    fields = [
        "title",
        "charts",
        "recordings",
        "key",
        "notes",
    ]


class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]


class DocumentAdmin(admin.ModelAdmin):
    search_fields = ["title"]


def better_image_str(self):
    tags = ", ".join(str(t) for t in self.tags.all())
    return f"{self.title} ({tags})"


def better_document_str(self):
    return f"{self.title} – {self.collection}"


Image.__str__ = better_image_str
Document.__str__ = better_document_str

admin.site.unregister(Image)
admin.site.unregister(Document)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(models.Song, SongAdmin)
admin.site.register(models.SetList, SetListAdmin)
