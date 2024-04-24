from django.urls import path
from . import views

app_name = "tasks" # avoide names collision

urlpatterns = [
    path("", views.index, name = "index"),
    path("add", views.add, name = "add")
]