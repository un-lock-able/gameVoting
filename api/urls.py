from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("games/", views.list_games, name="All games list"),
    path("<int:game_id>/characters/", views.list_characters, name="List characters in game"),
    path("<int:game_id>/submit/", views.record_votes, name="Submit vote"),
    path("<int:game_id>/result/", views.vote_results, name="Vote result for game"),
]