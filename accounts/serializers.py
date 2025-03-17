
from rest_framework import serializers
from .models import User , Crop ,Product, ProductGallery
from django.utils.text import slugify
from cart.models import CartItem


class UserSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "username", "email", "user_type", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def get_items(self, user):
        from cart.serializers import NewCartItemSerializer  # Delay the import
        cartitems = CartItem.objects.filter(cart=user, cart_paid=True)[:10]
        serializer = NewCartItemSerializer(cartitems, many=True)
        return serializer.data



class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ['id', 'crop_gallery', 'crop_name', 'short_desc', 'batch_number', 'batch_quantity', 'harvest_date', 'storage_date']


# ProductGallery Serializer
class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = ['id', 'image']


# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    gallery = ProductGallerySerializer(many=True, required=False)  # Allow nested gallery images

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'slug', 'short_desc', 'weight', 'price', 'dimension', 
                  'batch_number', 'crop_batch_number', 'batch_quantity', 'storage_date', 
                  'packaging_date', 'farmer_name', 'farmer_desc', 'gallery']

    def create(self, validated_data):
        # Extract gallery data safely
        gallery_data = validated_data.pop('gallery', [])

        # Generate slug if missing
        if 'slug' not in validated_data or not validated_data['slug']:
            validated_data['slug'] = slugify(validated_data['product_name'])

        # Create product instance
        product = Product.objects.create(**validated_data)

        # Create associated gallery images if any
        for gallery_item in gallery_data:
            ProductGallery.objects.create(product=product, **gallery_item)

        return product
    

class ProductDetailSerializer(serializers.ModelSerializer):
    gallery = ProductGallerySerializer(many=True)  # Include related images

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'slug', 'short_desc', 'weight', 'price', 
            'dimension', 'batch_number', 'crop_batch_number', 'batch_quantity', 
            'storage_date', 'packaging_date', 'farmer_name', 'farmer_desc', 'gallery'
        ]

