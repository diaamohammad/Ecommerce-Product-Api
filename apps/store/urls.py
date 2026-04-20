from django.urls import path,include
from .views import DisplayCategory,DisplayProducts,AdminCategoryview,AdminProductView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'products',DisplayProducts,basename='products')
router.register(r'admin/products',AdminProductView,basename='admin-products')
router.register(r'admin/categories',AdminCategoryview,basename='admin-category')



urlpatterns = [
    path('categories/',DisplayCategory.as_view(),name='display_category'),
    path('',include(router.urls)),
    
]