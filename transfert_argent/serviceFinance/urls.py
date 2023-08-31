from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('detailfinance/<int:pk>/', DetailTransactionView.as_view(), name="DetailTransactionView"),
    path('creatrefinance/', CreateTransactionView.as_view(), name="CreateTransactionView"),
    path('updatefinance/<int:pk>/', UpdateTransactionView.as_view(), name="UpdateTransactionView"),
    path('updatetransaction/<int:pk>/', ModifierTransactionView.as_view(), name="ModifierTransactionView"),
    path('deletefinance/<int:pk>/', DeleteTransactionView.as_view(), name="DeleteTransactionView"),
    path('listefinance/', ListeTransactionView.as_view(), name="ListeTransactionView"),
    path('toutelestransactions/', TransactionListAPIView.as_view(), name="TransactionListAPIView"),
    path('transactions/<int:utilisateur_id>/transaction/', TransactionListUserAPIView.as_view(), name='TransactionListUserAPIView'),
] 