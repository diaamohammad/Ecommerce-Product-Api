from django.db import models
from uuid import uuid4
from accounts.models import User
from django.core.validators import MinValueValidator,MaxValueValidator



class Category(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()


    def __str__(self):
        return self.name




class Product(models.Model):


    uuid = models.UUIDField(unique=True,default=uuid4)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='products')
    stock = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name



class Review(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta :

        unique_together = ['user','product']