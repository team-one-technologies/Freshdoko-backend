from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User , Crop , Product
from .serializers import UserSerializer , CropSerializer ,ProductSerializer,ProductDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes



@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_type": user.user_type})
    return Response(serializer.errors, status=400)

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_type": user.user_type})
    return Response({"error": "Invalid credentials"}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    user=request.user
    serializer=UserSerializer(user)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_crop(request):
    """
    Allows a farmer to add crop information.
    Only accessible by authenticated farmers.
    """
    if request.user.user_type != 'farmer':
        return Response({"error": "You are not authorized to add crops."}, status=status.HTTP_403_FORBIDDEN)

    serializer = CropSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(farmer=request.user)  # Assign the logged-in farmer to the crop
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_crop(request, crop_id):
    """
    Allows a farmer to update their crop details.
    Only accessible by authenticated farmers.
    """
    try:
        crop = Crop.objects.get(id=crop_id, farmer=request.user)
    except Crop.DoesNotExist:
        return Response({"error": "Crop not found or not authorized to update."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CropSerializer(crop, data=request.data, partial=True)  # `partial=True` allows partial updates

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_crop(request, crop_id):
    """
    Allows a farmer to delete their crop.
    Only accessible by authenticated farmers.
    """
    try:
        crop = Crop.objects.get(id=crop_id, farmer=request.user)
    except Crop.DoesNotExist:
        return Response({"error": "Crop not found or not authorized to delete."}, status=status.HTTP_404_NOT_FOUND)

    crop.delete()
    return Response({"message": "Crop deleted successfully."}, status=status.HTTP_200_OK)




# View to get list of products
@api_view(["GET"])
@permission_classes([IsAuthenticated])  # Only authenticated users (customers) can view products
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

#to retrieve the product details of the selected product based on the slug 
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def product_detail(request,slug):
    product=Product.objects.get(slug=slug)
    serializer=ProductDetailSerializer(product)
    return Response(serializer.data)
    