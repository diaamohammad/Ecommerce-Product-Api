from .models import Order,OrderItem
from apps.store.models import Product
import redis
from django.conf import settings
from rest_framework.views import APIView
import json
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.db import transaction


redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True
)





class CartService:
    

    @staticmethod
    def _get_key(user):
        return f"cart:{user.id}"
    

    @staticmethod
    def _serialize(cart:dict) -> str:
        return json.dumps(cart)
    

    
    @staticmethod
    def _deserialize(data:str |None) -> dict:
        if not data:
            return {}
        return json.loads(data)


    @classmethod
    def get_cart(cls,user):

        
        data = redis_client.get(cls._get_key(user))
        
        return cls._deserialize(data)
        
        

    
    @classmethod
    def save_cart(cls,user,cart:dict) -> None:
        key = cls._get_key(user)
        cart = cls._serialize(cart)
        redis_client.set(key,cart)
         

    
    @classmethod
    def delete_cart(cls,user):
        key = cls._get_key(user)
        redis_client.delete(key)
    


    
    @classmethod
    @transaction.atomic
    def list_cart(cls,user):

        cart = cls.get_cart(user)

        if not cart:
            return []
        product_ids = cart.keys()
        products = Product.objects.filter(uuid__in=product_ids)
        items=[]

        for product in products:

            product_id = str(product.uuid)
            name = product.name
            quantity = cart[str(product_id)]["quantity"]
            

            items.append({
                "id":product_id,
                "name":name,
                "quantity":quantity,
            })

        return items
            




    @classmethod
    def add_product(cls,user,product_uuid,quantity):

       
        cart = cls.get_cart(user)

        product= get_object_or_404(Product,uuid=product_uuid)

        product_id = str(product.uuid)

        if product.stock < quantity:
            raise ValidationError(" Not enough stock avilable")

        
        if product_id in cart:
            cart[product_id]["quantity"] += quantity
        else:
            cart[product_id] = {"quantity":quantity}

        cls.save_cart(user,cart)
        return cart
    

    
    @classmethod
    def update_product(cls,user,product_uuid,quantity):

        cart = cls.get_cart(user)

        product = get_object_or_404(Product,uuid=product_uuid)

        product_id =str(product.uuid)

        if product.stock < quantity:
            raise ValidationError("Not enough stock avilable")
        
        if product_id not in cart:
            raise ValidationError("product not in cart")
        
        cart[product_id]["quantity"] = quantity
        cls.save_cart(user,cart)
        return cart


    
    
    @classmethod
    def remove_product(cls,user,product_uuid):
        product = get_object_or_404(Product,uuid =product_uuid)
        cart = cls.get_cart(user)
        product_id = str(product.uuid)

        if product_id not in cart:
            raise ValidationError("Product not in cart")
        del cart[product_id]
        cls.save_cart(user,cart)
        return cart 
        

        

    @classmethod
    def list_cart(cls,user):

        cart = cls.get_cart(user)

        product_ids = cart.keys()

        products= Product.objects.filter(uuid__in=product_ids)
        
        items = []

        for product in products:
            
            name = product.name
            product_id = str(product.uuid)
            quantity = cart[product_id]["quantity"]
            

            items.append(
                
                {"name":name},
                {"quantity":quantity}
            )
        return items 


    

    @classmethod

    def checkout(cls,user,address,phone):

      cart = cls.get_cart(user)
        
      if not cart :
            raise ValidationError("Cart is empty")
      with transaction.atomic():  
        product_ids = cart.keys()

        products = Product.objects.select_for_update().filter(uuid__in=product_ids)

        products_map={str(product.uuid): product for product in products}        
        total_amount = 0

        
        for product_id,item in cart.items():
              
              if product_id not in products_map:
                  raise ValidationError("Some products no longer exist. ")
              
              quantity = item["quantity"]
              product = products_map[product_id]
              total_amount += product.price * quantity
              

              if product.stock < quantity:
                raise ValidationError("Stock is not enough")
              product.stock -= quantity
              product.save(update_fields=["quantity"])
        
            
        
        order = Order.objects.create(
            user=user,
            address=address,
            phone=phone,
            total_amount=total_amount,
            status="Pending",
            is_paid=False,
           )
        
        for product in products:

              product_id=str(product.uuid)
              quantity = cart[product_id]["quantity"]

              OrderItem.objects.create(

               quantity = quantity,
               price=product.price,
               order=order,
               product=product,

               )

        cls.delete_cart(user)

        return order
            
            









       

        

        
        
    