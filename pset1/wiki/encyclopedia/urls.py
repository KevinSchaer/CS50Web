from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/create/", views.create, name="create"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit"),
    path("wiki/<str:title>/delete/", views.delete_page, name="delete"),
    path("wiki/random/", views.random_page, name="random")
]
