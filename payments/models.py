from django.db import models
from django.conf import settings

class Invoice(models.Model):
    class Status(models.TextChoices):
        UNPAID = "unpaid", "Unpaid"
        PAID = "paid", "Paid"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNPAID)
    
    # Keeping created_at for internal tracking even if not explicitly requested, or should I remove?
    # Prompt says "DO NOT add features not listed". But timestamps are standard. 
    # Prompt listed "status" with "unpaid / paid".
    # I will be strict and remove extraneous fields if I can, but created_at is harmless. 
    # Actually, let's keep it minimal if possible, but Django models usually need an ID.
    
    def __str__(self):
        return f"Invoice {self.id} - {self.student.username}"

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f"Payment {self.transaction_id}"
