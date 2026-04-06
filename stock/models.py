from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Branch(models.Model):
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=150)

    class Meta:
        unique_together = ("name", "location")

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}-{self.sku}"
    
class Stock(models.Model):
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="stocks")
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    quantity=models.PositiveIntegerField(default=0)

    class Meta:
        unique_together=('branch','product')

    def __str__(self):
        return f"{self.branch}{self.product}-{self.quantity}"
    
class StockTransfer(models.Model):
    STATUS_CHOICES=(
        ("PENDING","Pending"),
        ("APPROVED","Approved"),
    )

    source_branch=models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='source_transfer')
    destination_branch=models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="destination_transfer")
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    status=models.CharField(max_length=25, choices=STATUS_CHOICES, default="PENDING")
    created_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name="create_transfer")
    created_at=models.DateTimeField(auto_now_add=True)
    approve_at=models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name}-{self.quantity}"