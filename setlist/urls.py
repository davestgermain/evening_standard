from django.urls import path
from . import views


urlpatterns = [
    path("", views.show_setlists),
    path("<int:list_id>/", views.show_setlist),
    path("<int:list_id>/duplicate/", views.duplicate_setlist),
]
