from django.urls import path

from . import views

app_name = "wallet"

urlpatterns = [
    path('', views.WalletDetailView.as_view(), name='wallet-detail'),
    path('topup/', views.WalletTopupView.as_view(), name='wallet-topup'),
    path('withdraw/', views.WalletWithdrawView.as_view(), name='wallet-withdraw'),
    path('transfer/', views.WalletTransferView.as_view(), name='wallet-transfer'),
    path('transactions/', views.WalletTransactionListView.as_view(), name='wallet-transactions'),
]
