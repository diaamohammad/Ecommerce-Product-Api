from django.db import models
from apps.accounts.models import User
from apps.store.models import Product
import uuid


class Cart(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    


class CartItem(models.Model):

    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):

    STATUS_CHOICES = (('Pending','Pending'),
                      ('Processing','Processing'),
                      ('Shipped','Shipped'),
                      ('Delivered','Delivered'),
                      ('Cancelled','Cancelled'),)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='orders')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Order is  {self.user.first_name}"


class OrderItem(models.Model):

   
    product = models.ForeignKey(Product,null=True,on_delete=models.SET_NULL,related_name='order_items')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    quantity = models.PositiveIntegerField(default=1)

    
    def __str__(self):
        return f"{self.order.order_code} - item"
