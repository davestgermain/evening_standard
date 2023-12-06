import json
import hashlib
from tempfile import TemporaryFile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.core.files.storage import default_storage

from .models import SetList, SetSong, Song


def show_setlists(request):
    context = {
        "lists": SetList.objects.all(),
    }
    return render(request, "setlist/index.html", context)


def print_setlist(request, list_id):
    songlist = get_object_or_404(SetList, pk=list_id)
    if not request.user.is_authenticated:
        return redirect("/admin/")
    charts = []
    chart_ids = ""
    for song in songlist.get_ordered_songs():
        songcharts = list(song.charts.all())
        # if the song has multiple pages, and it starts on an odd page,
        # insert a blank page before
        if len(charts) % 2 != 0 and len(songcharts) % 2 == 0:
            charts.append(None)
            chart_ids += "-1"
        for s in songcharts:
            charts.append(s)
            chart_ids += str(s.id)

    path = "charts/{}_{}.pdf".format(
        songlist.title.lower().replace(" ", "_"),
        hashlib.md5(chart_ids.encode("utf8")).hexdigest(),
    )
    if not default_storage.exists(path):
        from PIL import Image, ImageOps

        page_size = (2550, 3300)

        blank_image = Image.new("RGB", page_size, color=(255, 255, 255)).convert("L")
        images = []
        for chart in charts:
            if chart is not None:
                image = ImageOps.pad(
                    Image.open(chart.file).convert("L"), page_size, color="#fff"
                )
                images.append(image)
            else:
                # blank page inserted before multi-page charts
                images.append(blank_image)

        with TemporaryFile() as temp_file:
            images[0].save(
                temp_file,
                format="pdf",
                save_all=True,
                append_images=images[1:],
                resolution=300,
            )
            temp_file.seek(0)
            default_storage.save(path, temp_file)
    return redirect(f"/media/{path}")


def show_setlist(request, list_id):
    songlist = get_object_or_404(SetList, pk=list_id)
    is_authenticated = request.user.is_authenticated
    context = {
        "can_change": is_authenticated,
        "list": songlist,
        "all_songs": Song.objects.exclude(
            pk__in=[s.id for s in songlist.songs.all()]
        ).order_by("title"),
    }
    return render(request, "setlist/setlist.html", context)


def show_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    used_in = song.setlist_set.all()
    context = {
        "can_change": request.user.is_authenticated,
        "song": song,
        "used_in": used_in,
        "is_authenticated": request.user.is_authenticated,
    }
    return render(request, "setlist/song.html", context)


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
