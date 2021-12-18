from django.urls import path
from . import views

urlpatterns=[
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register/check-username/', views.checkusername, name='checkusername'),
    path('register/member-register/', views.buyregister, name='buyregister'),
    path('register/contract/', views.logout, name='registercontract'),
    path('logout/', views.logout, name='logout'),
    path('<str:username>/profile/',views.profile, name='profile'),
    path('<str:username>/user-raffle/',views.userraffle, name='userraffle'),
    path('<str:username>/user-raffle/more-raffle/',views.usermoreraffle, name='usermoreraffle'),
    path('<str:username>/buy-processes/',views.userbuy, name='userbuy'),
    path('<str:username>/user-members/',views.usermembers, name='usermembers'),
    path('<str:username>/change-password/',views.changepassword, name='changepassword'),
    path('<str:username>/change-mail/',views.changemail, name='changemail'),
    path('<str:username>/settings/',views.settings, name='settings'),

]