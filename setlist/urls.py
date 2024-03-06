from django.urls import path
from . import views


urlpatterns = [
    path("", views.show_setlists),
    path("<int:list_id>/", views.show_setlist),
    path("<int:list_id>/duplicate/", views.duplicate_setlist),
    path("<int:list_id>/edit/", views.edit_setlist),
    path("<int:list_id>/print/", views.print_setlist),
    path("song/<int:song_id>/", views.show_song),
    path("song/", views.chart_view),
]
