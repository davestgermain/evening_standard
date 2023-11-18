from django.utils import timezone
from wagtail.models import Page, Collection
from wagtail.documents.models import Document
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from setlist.models import SetList

from wagtail.search import index
from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=5)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def map_url(self):
        loc = f"{self.address}, {self.city},{self.state} {self.zipcode}"
        loc = loc.replace(" ", "+")
        return f"https://maps.google.com/maps/dir//{loc}/"

    @property
    def best_url(self):
        if self.website:
            return self.website
        else:
            return self.map_url


class ShowIndex(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        shows = Show.objects.live().child_of(self)
        upcoming = shows.filter(start__gte=timezone.now()).order_by("start")
        if request.user.is_anonymous:
            upcoming = upcoming.filter(public=True)
        context["upcoming_shows"] = upcoming

        context["past_shows"] = shows.filter(start__lt=timezone.now()).order_by(
            "-start"
        )

        return context


class Show(Page):
    start = models.DateTimeField("Start Time")
    public = models.BooleanField("Public Show", default=True)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    body = RichTextField(blank=True)

    recordings = models.ForeignKey(
        Collection, blank=True, null=True, on_delete=models.SET_NULL
    )
    set_list = models.ForeignKey(
        SetList, blank=True, null=True, on_delete=models.SET_NULL
    )

    search_fields = Page.search_fields + [
        index.SearchField("venue"),
        index.SearchField("start"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("start"),
        FieldPanel("venue"),
        FieldPanel("body"),
        FieldPanel("public"),
        FieldPanel("set_list"),
        FieldPanel("recordings"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["is_past"] = self.start < timezone.now()
        if self.recordings:
            recordings = (
                Document.objects.filter(collection=self.recordings)
                .filter(tags__name="public")
                .order_by("file")
            )
            context["recordings"] = list(recordings)
        return context


class Listen(models.Model):
    document = models.ForeignKey(Document, on_delete=models.DO_NOTHING, null=True)
    start = models.DateTimeField(auto_now_add=True, db_index=True)
    ip_address = models.GenericIPAddressField()
    browser = models.CharField(max_length=255, default="unknown")
    referer = models.CharField(max_length=255, default="")
