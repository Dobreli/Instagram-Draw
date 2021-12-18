from django.urls import path
from . import views

urlpatterns=[
    path('member-buy/<int:id>/', views.BuyMember.as_view(), name='buymembers'),
    path('payment-transfer/<int:id>/', views.paymenttransfer, name='paymenttransfer'),
    path('payment-credit/<int:id>/', views.paymentcredit, name='paymentcredit'),
]