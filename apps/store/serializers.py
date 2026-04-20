from rest_framework import serializers
from .models import Category,Product,Review


class DisplayCategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category
        fields = '__all__'



class DisplayProductsSerializer(serializers.ModelSerializer):


    class Meta:

        model = Product
        fields = ['name','description']



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name','description','price','image']



class AdminCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
      



class AdminProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
       


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields=['product','comment','rating']



class ReviewDisplaySerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()


    class Meta:
        model = Review
        fields = ['id','user','product','comment','rating','created_at']



class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):
        if not