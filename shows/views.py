import operator
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils.http import http_date
from shows.models import Show

from wagtail.documents.models import Document


def mark_listen(request):
    doc = get_object_or_404(Document, pk=request.POST.get("document", 0))

    doc.listen_set.create(
        ip_address=request.META.get("HTTP_X_FORWARDED_FOR", "127.0.0.1"),
        browser=request.META["HTTP_USER_AGENT"],
        referer=request.META["HTTP_REFERER"],
    )
    return JsonResponse({"playing": True})


def calendar(request):
    from ics import Calendar, Event
    from datetime import timedelta

    thecal = Calendar()
    thecal.creator = "Evening Standard Jazz"
    past, upcoming = Show.show_list(request.user)
    shows = list(past) + list(upcoming)
    shows.sort(key=operator.attrgetter("start"), reverse=True)
    last_gig = 0

    for show in shows:
        evt = Event()
        evt.uid = "{}@evening_standard".format(show.id)
        evt.name = show.title
        evt.description = show.body
        evt.last_modified = show.last_published_at
        last_modified = evt.last_modified.timestamp()
        if last_modified > last_gig:
            last_gig = last_modified
        evt.url = show.full_url
        evt.begin = show.start
        evt.duration = timedelta(hours=2)
        evt.location = f"{show.venue.name}\n{show.venue.address}\n{show.venue.city} {show.venue.state}"
        thecal.events.add(evt)
    response = HttpResponse(thecal, content_type="text/calendar")
    if last_gig:
        response["Last-Modified"] = http_date(last_gig)
    return response
