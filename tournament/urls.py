from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('tournaments/', views.TournamentList.as_view(), name="tournament-list"),
    path('tournaments/<int:pk>/', views.TournamentDetail.as_view(), name="tournament-detail"),
    path('tournaments/<int:pk>/make_pools/', views.MakePoolsEndpoint.as_view(), name="make-pools"),
    path('pools/', views.PoolList.as_view(), name="pool-list"),
    path('pools/<int:pk>/', views.PoolDetail.as_view(), name="pool-detail"),
    path('teams/', views.TeamList.as_view(), name="team-list"),
    path('teams/<int:pk>/', views.TeamDetail.as_view(), name="team-detail"),
    path('participants/', views.ParticipantList.as_view(), name="participant-list"),
    path('participants/<int:pk>/', views.ParticipantDetail.as_view(), name="participant-detail"),
    path('rounds/', views.RoundList.as_view(), name="round-list"),
    path('rounds/<int:pk>/', views.RoundDetail.as_view(), name="round-detail"),
    path('turns/', views.TurnList.as_view(), name="turn-list"),
    path('turns/<int:pk>/', views.TurnDetail.as_view(), name="turn-detail"),
    path('forms/', views.FormList.as_view(), name="form-list"),
    path('forms/<int:pk>/', views.FormDetail.as_view(), name="form-detail"),
    path('scores/', views.ScoreList.as_view(), name="score-list"),
    path('scores/<int:pk>/', views.ScoreDetail.as_view(), name="score-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
