from .models import Invoice, Payment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import InvoiceForm

def is_admin(user):
    return user.role == 'ADMIN'

@login_required
def payment_list(request):
    user = request.user
    if user.role == 'STUDENT':
        payments = Payment.objects.filter(invoice__student=user)
        invoices = Invoice.objects.filter(student=user)
    else:
        payments = Payment.objects.all()
        invoices = Invoice.objects.all()
    return render(request, 'payments/payment_list.html', {'payments': payments, 'invoices': invoices})

@login_required
@user_passes_test(is_admin)
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice created successfully.')
            return redirect('payment_list')
    else:
        form = InvoiceForm()
    return render(request, 'payments/invoice_form.html', {'form': form, 'title': 'Create Invoice'})

@login_required
@user_passes_test(is_admin)
def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice updated successfully.')
            return redirect('payment_list')
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'payments/invoice_form.html', {'form': form, 'title': 'Edit Invoice'})

@login_required
@user_passes_test(is_admin)
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, 'Invoice deleted successfully.')
        return redirect('payment_list')
    return render(request, 'payments/confirm_delete.html', {'object': invoice})
