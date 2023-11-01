from wagtail.models import Page, Collection
from wagtail.images.models import Image
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from wagtail.search import index
from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255)
    key = models.CharField(max_length=4, blank=True, null=True)
    notes = models.TextField(blank=True)
    charts = models.ManyToManyField(Image, blank=True)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/setlist/song/{self.id}/"


class SetList(models.Model):
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    songs = models.ManyToManyField(Song, through="SetSong")

    def get_absolute_url(self):
        return f"/setlist/{self.id}/"

    def duplicate(self):
        dest = SetList(notes=self.notes, title=f"{self.title} (copy)")
        dest.save()
        for obj in SetSong.objects.filter(setlist=self):
            SetSong.objects.create(
                setlist=dest,
                song=obj.song,
                sort_order=obj.sort_order,
            )
        return dest

    def __str__(self):
        return self.title


class SetSong(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    setlist = models.ForeignKey(SetList, on_delete=models.CASCADE)
    sort_order = models.IntegerField()

    class Meta:
        ordering = [
            "sort_order",
        ]
        unique_together = ("setlist", "sort_order")

    def __str__(self):
        return f"{self.sort_order} – {self.song}"
