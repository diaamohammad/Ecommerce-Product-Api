from django.shortcuts import render
from rest_framework import generics,viewsets,permissions
from .models import Category,Product,Review
from django.db.models import Q
from .services import ReviewService
from .serializers import( DisplayCategorySerializer,
                         ProductSerializer,
                         DisplayProductsSerializer,
                         AdminProductSerializer,
                         AdminCategorySerializer,
                         ReviewDisplaySerializer,
                         ReviewSerializer)




class DisplayCategory(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = DisplayCategorySerializer



class DisplayProducts(viewsets.ReadOnlyModelViewSet):

    
    def get_queryset(self):
        queryset = Product.objects.all()
        search = self.request.query_params.get('search')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search))
            
        return queryset
  
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DisplayProductsSerializer
        return ProductSerializer

    


class AdminCategoryview(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = AdminCategorySerializer
    permission_classes = [permissions.IsAdminUser]


class AdminProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = AdminProductSerializer
    permission_classes = [permissions.IsAdminUser]




class ReviewView(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):

        return Review.objects.filter(user=self.request.user)


    def perform_create(self, serializer):

        review =  ReviewService.add_review(
            product_id=serializer.validated_data["product"].id,
            user=self.request.user,
            rating=serializer.validated_data["rating"],
            comment=serializer.validated_data.get("comment"),

        )

        serializer.instance = review

    def perform_update(self, serializer):


        review = ReviewService.update_review(
            review_id=self.get_object().id,
            user=self.request.user,
            comment=serializer.validated_data.get("comment"),
            rating=serializer.validated_data.get("rating")
        )

        serializer.instance = review

    def perform_destroy(self, instance):
        ReviewService.delete_review(
            user=self.request.user,
            review_id=instance.id
        )


class ReviewDispalyView(generics.ListAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewDisplaySerializer
    