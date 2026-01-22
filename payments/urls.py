from django.urls import path
from .views import payment_list, invoice_create, invoice_update, invoice_delete

urlpatterns = [
    # Template Views
    path('payments/list/', payment_list, name='payment_list'),
    path('payments/invoices/create/', invoice_create, name='invoice_create'),
    path('payments/invoices/<int:pk>/edit/', invoice_update, name='invoice_update'),
    path('payments/invoices/<int:pk>/delete/', invoice_delete, name='invoice_delete'),
]
