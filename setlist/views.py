from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test

from .models import SetList


def show_setlists(request):
    context = {
        "lists": SetList.objects.all(),
    }
    return render(request, "setlist/index.html", context)


def show_setlist(request, list_id):
    context = {
        "list": get_object_or_404(SetList, pk=list_id),
        "do_print": request.GET.get("print") == "1",
    }
    return render(request, "setlist/setlist.html", context)


def can_duplicate(user):
    return user.has_perm("setlist.add_setlist")


@user_passes_test(can_duplicate)
def duplicate_setlist(request, list_id):
    source = get_object_or_404(SetList, pk=list_id)
    dest = source.duplicate()
    return redirect(f"/django-admin/setlist/setlist/{dest.id}/change/")
