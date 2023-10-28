import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

from .models import SetList, SetSong, Song


def show_setlists(request):
    context = {
        "lists": SetList.objects.all(),
    }
    return render(request, "setlist/index.html", context)


def show_setlist(request, list_id):
    songlist = get_object_or_404(SetList, pk=list_id)
    context = {
        "list": songlist,
        "do_print": request.GET.get("print") == "1",
        "all_songs": Song.objects.exclude(
            pk__in=[s.id for s in songlist.songs.all()]
        ).order_by("title"),
    }
    return render(request, "setlist/setlist.html", context)


def can_duplicate(user):
    return user.has_perm("setlist.add_setlist")


def can_edit(user):
    return user.has_perm("setlist.change_setlist")


@user_passes_test(can_duplicate)
def duplicate_setlist(request, list_id):
    source = get_object_or_404(SetList, pk=list_id)
    dest = source.duplicate()
    return redirect(f"/setlist/{dest.id}/")


@user_passes_test(can_edit)
def edit_setlist(request, list_id):
    source = get_object_or_404(SetList, pk=list_id)
    data = json.loads(request.body)

    if data["title"] != source.title:
        source.title = data["title"]

    new_order = data["order"]
    songs = list(SetSong.objects.filter(setlist=source))
    for song in songs:
        song.sort_order = -song.sort_order
        song.save()

    while songs:
        song = songs.pop()
        try:
            song.sort_order = new_order.pop(str(song.song_id))
        except KeyError:
            song.delete()
        else:
            song.save()

    if songs:
        # something was deleted
        for song in songs:
            song.delete()
    # add missing songs
    if new_order:
        for song_id, sort_order in new_order.items():
            SetSong.objects.create(
                setlist=source, song_id=int(song_id), sort_order=sort_order
            )
    return JsonResponse({"saved": True})
