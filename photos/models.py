from django.db import models

# Create your models here.

class Photo(models.Model):
    filename = models.CharField(max_length=255, default="")
    title = models.CharField(max_length=255, default="")
    description = models.TextField(default="")

class PurchaseLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    photo = models.ForeignKey(Photo)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class CouponCode(models.Model):
    code = models.CharField(max_length=255, unique=True)
    discount_percentage = models.DecimalField(max_digits=3, decimal_places=0)
