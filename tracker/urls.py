from django.urls import path
from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.home, name="home"),
    path("clear_history/", views.clear_history, name="clear_history"),
    path("", views.home, name="home"),
]
