from rest_framework import serializers
from .models import Order,OrderItem,Cart,CartItem



class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Order
        fields = ['phone','address']

        
        
class OrderDisplaySerializer(serializers.ModelSerializer):

         class Meta:

               model = Order       
               fields =    ['__all__']


