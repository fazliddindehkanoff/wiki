from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("add", views.create, name="add"),
    path("random-page/", views.random_page, name="random-page"),
    path("search", views.search, name="search"),
]
