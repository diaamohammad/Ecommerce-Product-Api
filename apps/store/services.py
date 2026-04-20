from .models import Product,Review
from orders.models import OrderItem
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class ReviewService():

    @staticmethod
    def check_rating(rating):
        if rating < 1 or rating > 5 :
            raise ValidationError("Invaild rating")

    @classmethod  
    def add_review(cls,product_id,user,rating,comment):

        cls.check_rating(rating)

        if Review.objects.filter(user=user,product=product_id).exists():
            raise ValidationError("Already reviewed")
        if OrderItem.objects.filter(order__user=user,product=product_id).exists():
            raise ValidationError("You must buy first")
        

        review = Review.objects.create(
            user=user,
            product=product_id,
            comment=comment,
            rating=rating
        )

        return review
    

    @classmethod
    def update_review(cls,review_id,user,rating=None,comment=None):

        review = get_object_or_404(Review,id=review_id)

        if review.user != user :
        
            raise ValidationError('you cannot update this review') 
        
        if rating is not None :
            cls.check_rating(rating) 
            review.rating=rating

        if comment is not None:
             review.comment=comment

        review.save()
        return review
    
    def delete_review(user,review_id):
        review = get_object_or_404(Review,user=user,id=review_id)
        review.delete()
        return review 
    

        

        
