from django.urls import path
from .views import *

urlpatterns=[
    path('free-raffle/',FreeRaffle.as_view(),name='freeraffle'),
    path('instagram-raffle/',InstagramRaffle.as_view(),name='instagramraffle'),
    path('re-instagram-raffle/',reinstagramraffle,name='reinstagramraffle'),
    path('reference/',reference,name='reference'),
    path('instagram-raffle/result/<int:raffleid>/',InstagramRaffleResult.as_view(),name='instagramraffleresult'),
    path('instagram-raffle/total-comment/',TotalComment.as_view(),name='totalcomment'),
    path('instagram-raffle/raffle-query/',RaffleQuery.as_view(),name='rafflequery'),
]