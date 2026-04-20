from django.shortcuts import render
from rest_framework import viewsets,generics
from rest_framework.response import Response
from .models import Order,OrderItem
from rest_framework.views import APIView
from .serializers import CartSerializer
from .services import CartService 



class CartView(APIView):

    def post(self,request):
      serialize = CartSerializer(data=request.data)
      serialize.is_valid(raise_exception=True)
      data = serialize.validated_data

      user = request.user
      quantity = data["quantity"]
      product_uuid = data["product_uuid"]

      cart = CartService.add_product(
         user,
         quantity,
         product_uuid)   
         
      return Response({"message":"product added","cart":cart},status=201)
    

    def put(self,request):
       
       seriallizer = CartSerializer(data=request.data)
       seriallizer.is_valid(raise_exception=True )
       data = seriallizer.validated_data

       user = request.user
       quantity = data["quantity"]
       product_uuid = data["product_uuid"]

       cart = CartService.update_product(user,quantity,product_uuid)

       return Response({"message": "Product updated","cart":cart}, status=200)
    

    def get(self,request):
       items = CartService.list_cart(request.user)
       return Response(items)
    

    def delete(self,request):
       
       CartService.delete_cart(request.user)
       return  Response({"message":"cart deleted"})
      


class CheckoutView(APIView):

   def post(self,request):

      user = request.user
      address = request.data.get("address")
      phone = request.data.get("phone")

      order = CartService.checkout(user,address,phone)

      return Response({"message":"order created","order_id":order.id}, status=201 )



    

    


    

    
