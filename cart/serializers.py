# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem ,Order,OrderItem

# class CartItemSerializer(serializers.ModelSerializer):
#     # Include product name and price in the serialized data
#     product_name = serializers.CharField(source='product.product_name', read_only=True)
#     product_price = serializers.DecimalField(source='product.price',max_digits=10,decimal_places=2, read_only=True)

#     class Meta:
#         model = CartItem
#         fields = ['id', 'cart', 'product', 'quantity', 'product_name', 'product_price', 'total_price']

#     def get_total_price(self, obj):
#         return obj.total_price


# class CartSerializer(serializers.ModelSerializer):
#     # Serialize cart items with nested CartItemSerializer
#     items = CartItemSerializer(many=True, read_only=True)
#     total_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
#     item_count = serializers.IntegerField(read_only=True)

#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'created_at', 'updated_at', 'items', 'total_price', 'item_count']

class CartItemSerializer(serializers.ModelSerializer):
    product = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.serializers import ProductSerializer  # Delay the import
        self.fields['product'] = ProductSerializer(read_only=True)

    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'total', 'product', 'quantity']

    def get_total(self, cartitem):
        price = cartitem.product.price * cartitem.quantity
        return price



class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(read_only=True,many=True)
    sum_total= serializers.SerializerMethodField()
    num_of_items=serializers.SerializerMethodField()
    class Meta:
        model= Cart
        fields=['id', 'cart_code',"items",'sum_total','num_of_items', 'created_at', 'updated_at']
    
    def get_sum_total(self,cart):
        items=cart.items.all()
        total=sum([item.product.price* item.quantity for item in items ])
        return total
    
    def get_num_of_items(self,cart):
        items=cart.items.all()
        total=sum([item.quantity for item in items])
        return total

    
class SimpleCartSerializer(serializers.ModelSerializer):
    num_of_items=serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields=['id',"cart_code","num_of_items" ]

    def get_num_of_items(self,cart):
        num_of_items=sum([item.quantity for item in cart.items.all() ])
        return num_of_items
    
class NewCartItemSerializer(serializers.ModelSerializer):
    from accounts.serializers import ProductSerializer
    product = ProductSerializer(read_only=True)
    order_id = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "order_id", "order_date"]

    def get_order_id(self, cartitem):
        return cartitem.cart.cart_code

    def get_order_date(self, cartitem):
        return cartitem.cart.modified_at


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'full_name', 'email', 'phone_number', 'delivery_address', 
                  'delivery_point', 'delivery_date', 'total_price', 'payment_method', 'payment_confirmation_number', 
                  'created_at', 'updated_at', 'items']


