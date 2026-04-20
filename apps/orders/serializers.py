from rest_framework import serializers
from .models import Order,OrderItem



class CartSerializer(serializers.Serializer):

      uuid = serializers.CharField(max=50)
      quantity = serializers.DecimalField()

      def validate_quantity(self,value):
            if value <= 0 :
                  raise serializers.ValidationError('quantity must be greater than 0')
            return value
           
       


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Order
        fields = ['phone','address']

    def validate(self, data):
          
          user = self.context['request'].user
          if Order.objects.filter(user=user,status="pending").exists:
                raise serializers.ValidationError
          return data
          



class OrderItemSerializer(serializers.ModelSerializer):
      
      class Meta:
            model=OrderItem
            fields = '__all__'

    

        
        
class OrderDisplaySerializer(serializers.ModelSerializer):
         
         items = OrderItemSerializer(many=True, read_only=True)

         class Meta:

               model = Order       
               fields =    '__all__'

         

