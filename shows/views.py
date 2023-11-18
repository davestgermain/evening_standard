from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from wagtail.documents.models import Document


def mark_listen(request):
    doc = get_object_or_404(Document, pk=request.POST.get("document", 0))

    doc.listen_set.create(
        ip_address=request.META.get("HTTP_X_FORWARDED_FOR", "127.0.0.1"),
        browser=request.META["HTTP_USER_AGENT"],
        referer=request.META["HTTP_REFERER"],
    )
    return JsonResponse({"playing": True})
