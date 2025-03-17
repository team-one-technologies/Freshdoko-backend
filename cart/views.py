# cart/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Cart, CartItem , Transaction ,Order,OrderItem
from .serializers import CartSerializer, CartItemSerializer ,SimpleCartSerializer ,OrderItemSerializer,OrderSerializer
from accounts.models import Product
from accounts.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
import uuid 
from decimal import Decimal
from django.conf import settings
import requests
from django.utils import timezone


@api_view(['POST'])
def add_to_cart(request):
    try:
        cart_code = request.data.get("cart_code")
        product_id = request.data.get("product_id")

        if not cart_code or not product_id:
            return Response({"error": "cart_code and product_id are required"}, status=400)

        cart, created = Cart.objects.get_or_create(cart_code=cart_code)
        product = Product.objects.get(id=product_id)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)

        cartitem.quantity += 1  # Increment quantity
        cartitem.save()

        serializer = CartItemSerializer(cartitem)
        return Response({
            "data": serializer.data,
            "message": "Cart item created successfully"
        }, status=201)

    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def product_in_cart(request):
    cart_code = request.query_params.get("cart_code")
    product_id = request.query_params.get("product_id")

    try:
        cart = Cart.objects.get(cart_code=cart_code)
        product = Product.objects.get(id=product_id)
        product_exists_in_cart = CartItem.objects.filter(cart=cart, product=product).exists()
        return Response({'product_in_cart': product_exists_in_cart})

    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)


@api_view(['GET'])
def get_cart_stat(request):
    cart_code = request.query_params.get("cart_code")
    try:
        cart = Cart.objects.get(cart_code=cart_code, paid=False)
        serializer = SimpleCartSerializer(cart)
        return Response(serializer.data)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)


@api_view(['GET'])
def get_cart(request):
    cart_code = request.query_params.get("cart_code")
    try:
        cart = Cart.objects.get(cart_code=cart_code, paid=False)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)


@api_view(['PATCH'])
def update_quantity(request):
    try:
        cartitem_id = request.data.get("item_id")
        quantity = request.data.get("quantity")

        if not cartitem_id or quantity is None:
            return Response({"error": "item_id and quantity are required"}, status=400)

        quantity = int(quantity)  # Ensure quantity is an integer
        if quantity < 1:
            return Response({"error": "Quantity must be at least 1"}, status=400)

        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.quantity = quantity
        cartitem.save()

        serializer = CartItemSerializer(cartitem)
        return Response({
            "data": serializer.data,
            "message": "Cart item updated successfully!"
        }, status=200)

    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=404)

    except ValueError:
        return Response({"error": "Quantity must be a valid integer"}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
    

@api_view(['DELETE'])
def delete_cartitem(request):
    try:
        cartitem_id = request.data.get("item_id")

        if not cartitem_id:
            return Response({"error": "item_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        cartitem = CartItem.objects.get(id=cartitem_id)
        cartitem.delete()

        return Response({"message": "Cart item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        user = request.user
        cart = Cart.objects.get(cart_code=request.data.get("cart_code"), paid=True, user=user)

        # Create the order
        order = Order.objects.create(
            user=user,
            full_name=request.data.get("full_name"),
            email=request.data.get("email"),
            phone_number=request.data.get("phone_number"),
            delivery_address=request.data.get("delivery_address"),
            delivery_point=request.data.get("delivery_point"),
            delivery_date=request.data.get("delivery_date"),
            total_price=request.data.get("total_price"),
            payment_method=request.data.get("payment_method"),
            payment_confirmation_number=request.data.get("payment_confirmation_number"),
        )

        # Add items to the order
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )

        # Clear the cart
        cart.items.all().delete()
        cart.paid = False
        cart.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Cart.DoesNotExist:
        return Response({"error": "Cart not found or not paid"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_khalti_payment(request):
    try:
        # Generate a unique transaction reference
        tx_ref = str(uuid.uuid4())
        cart_code = request.data.get("cart_code")

        # Fetch cart
        cart = Cart.objects.get(cart_code=cart_code, paid=False)
        user = request.user

        # Calculate total amount in paisa (Khalti requires paisa)
        amount = sum([item.quantity * item.product.price for item in cart.items.all()])
        tax = Decimal("7.00")  # Example tax
        total_amount = int((amount + tax) * 100)  # Convert to paisa

        # Define purchase details
        purchase_order_id = tx_ref
        purchase_order_name = "FreshDoko Order"

        # Create transaction record
        transaction = Transaction.objects.create(
            ref=tx_ref,
            cart=cart,
            amount=total_amount,
            currency="NPR",
            user=user,
            status="pending",
        )

        # Khalti API payload
        khalti_payload = {
            "return_url": f"{settings.BASE_URL}/payment-status/",
            "website_url": settings.BASE_URL,
            "amount": total_amount,  # Amount in paisa
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": purchase_order_name,
            "customer_info": {
                "name": user.username,
                "email": user.email,
                "phone": user.phone,
            },
            "amount_breakdown": [
                {"label": "Subtotal", "amount": int(amount * 100)},
                {"label": "Tax", "amount": int(tax * 100)},
            ],
            "product_details": [
                {
                    "identity": str(item.product.id),
                    "name": item.product.name,
                    "total_price": int(item.quantity * item.product.price * 100),
                    "quantity": item.quantity,
                    "unit_price": int(item.product.price * 100),
                }
                for item in cart.items.all()
            ],
        }

        # Set up headers
        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        # Make the API request to Khalti
        response = requests.post(
            "https://dev.khalti.com/api/v2/epayment/initiate/",
            json=khalti_payload,
            headers=headers,
        )

        # Check if the request was successful
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=response.status_code)

    except Cart.DoesNotExist:
        return Response({"error": "Cart not found or already paid"}, status=status.HTTP_404_NOT_FOUND)

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def khalti_payment_callback(request):  
    """
    Verifies the payment status from Khalti and updates transaction details accordingly.
    """

    # Extract parameters from the request
    payment_status = request.data.get("status")
    tx_ref = request.data.get("tx_ref")
    transaction_id = request.data.get("transaction_id")

    if not tx_ref or not transaction_id:
        return Response(
            {"message": "Invalid request. Missing transaction reference or ID."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if payment_status != "successful":
        return Response(
            {"message": "Payment was not successful.", "subMessage": "Transaction failed or was cancelled."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Verify transaction with Khalti API
        headers = {"Authorization": f"Key {settings.KHALTI_SECRET_KEY}"}
        response = requests.get(
            f"https://api.khalti.com/v2/epayment/lookup/?pidx={transaction_id}",
            headers=headers,
        )

        if response.status_code != 200:
            return Response(
                {"message": "Failed to verify the transaction.", "subMessage": "Could not confirm payment status."},
                status=response.status_code,
            )

        response_data = response.json()

        # Ensure transaction exists in our database
        transaction = Transaction.objects.filter(ref=tx_ref).first()
        if not transaction:
            return Response(
                {"message": "Transaction not found.", "subMessage": "Invalid transaction reference."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Confirm transaction details
        if response_data.get("status") == "Completed" and Decimal(response_data["total_amount"]) == transaction.amount and response_data["currency"] == transaction.currency:
            # Update transaction status
            transaction.status = "completed"
            transaction.save()

            # Mark cart as paid
            cart = transaction.cart
            cart.paid = True
            cart.user = request.user
            cart.save()

            # Create an order from the cart
            order_data = {
                 "cart_code": cart.cart_code,
                 "full_name": request.user.get_full_name(),
                 "email": request.user.email,
                 "phone_number": request.user.phone_number,
                "delivery_address": request.data.get("delivery_address"),
                "delivery_point": request.data.get("delivery_point"),
                "delivery_date": request.data.get("delivery_date"),
                "total_price": str(transaction.amount / 100),  # Convert back to the original currency
                "payment_method": "Khalti",
                "payment_confirmation_number": transaction_id,
                }

            # Call the create_order view
            create_order(request._request)

            return Response(
                {"message": "Payment successful", "subMessage": "You have successfully made the payment."},
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"message": "Payment verification failed.", "subMessage": "Transaction details mismatch."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except requests.exceptions.RequestException as e:
        return Response(
            {"error": "Khalti verification request failed", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    except Exception as e:
        return Response(
            {"error": "An unexpected error occurred", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payoneer_payment(request):
    try:
        # Generate a unique transaction reference
        tx_ref = str(uuid.uuid4())
        cart_code = request.data.get("cart_code")

        # Fetch the cart and user details
        cart = Cart.objects.get(cart_code=cart_code, paid=False)
        user = request.user

        # Calculate the total amount in your preferred currency
        amount = sum([item.quantity * item.product.price for item in cart.items.all()])
        tax = Decimal("2.33")  # Example tax value
        total_amount = amount + tax  # This is the net amount before tax

        # Define transaction and order details
        purchase_order_id = tx_ref
        purchase_order_name = "FreshDoko Order"

        # Create transaction record
        transaction = Transaction.objects.create(
            ref=tx_ref,
            cart=cart,
            amount=total_amount,
            currency="EUR",  # Example: EUR (you can use your desired currency)
            user=user,
            status="pending",
        )

        # Payoneer API payload
        payoneer_payload = {
            "integration": "HOSTED",
            "transactionId": tx_ref,
            "country": "FR",  # Example country
            "channel": "WEB_ORDER",
            "system": {
                "id": "123def343ed4ba1cb",
                "type": "MARKETPLACE",
                "code": "SHOPSYSTEM",
                "version": "ShopSystemV1.0"
            },
            "division": "main_division",
            "callback": {
                "returnUrl": f"{settings.BASE_URL}/payment-success/",
                "summaryUrl": f"{settings.BASE_URL}/payment-summary/",
                "cancelUrl": f"{settings.BASE_URL}/payment-cancel/",
                "notificationUrl": f"{settings.BASE_URL}/payment-notification/",
            },
            "customer": {
                "email": user.email,
                "name": {
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                },
            },
            "payment": {
                "reference": f"order nr. {cart_code}",
                "amount": float(total_amount),
                "currency": "EUR",
            },
            "products": [
                {
                    "code": item.product.code,
                    "name": item.product.name,
                    "amount": float(item.product.price),
                    "quantity": item.quantity,
                }
                for item in cart.items.all()
            ],
            "operationType": "CHARGE",
            "ttl": 60,
        }

        # Send the payment initiation request to Payoneer's hosted API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.PAYONEER_API_KEY}",  # Ensure you have the API Key
        }

        # Make the API request to Payoneer
        response = requests.post(
            "https://api.payoneer.com/payment/hosted/initiate",  # Example URL 
            json=payoneer_payload,
            headers=headers,
        )

        # Check if the request was successful
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=response.status_code)

    except Cart.DoesNotExist:
        return Response({"error": "Cart not found or already paid"}, status=status.HTTP_404_NOT_FOUND)

    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def payoneer_payment_callback(request):
    """
    Verifies the payment status from Payoneer and updates transaction details accordingly.
    """

    # Extract parameters from the request
    payment_status = request.data.get("status")
    transaction_id = request.data.get("transactionId")
    tx_ref = request.data.get("transactionRef")

    if not tx_ref or not transaction_id:
        return Response({"message": "Invalid request. Missing transaction reference or ID."}, status=status.HTTP_400_BAD_REQUEST)

    if payment_status != "SUCCESS":
        return Response({"message": "Payment was not successful."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Verify transaction with Payoneer API
        headers = {"Authorization": f"Bearer {settings.PAYONEER_API_KEY}"}
        verification_url = f"https://api.payoneer.com/payment/status/{transaction_id}"  # Example verification URL
        response = requests.get(verification_url, headers=headers)

        if response.status_code != 200:
            return Response({"message": "Failed to verify the transaction."}, status=response.status_code)

        response_data = response.json()

        # Ensure transaction exists in our database
        transaction = Transaction.objects.filter(ref=tx_ref).first()
        if not transaction:
            return Response({"message": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)

        if response_data.get("status") == "Completed" and response_data["amount"] == transaction.amount:
        # Update transaction status
            transaction.status = "completed"
            transaction.save()

            # Mark cart as paid
            cart = transaction.cart
            cart.paid = True
            cart.save()

            # Create an order from the cart
            order_data = {
                "cart_code": cart.cart_code,
                "full_name": request.user.get_full_name(),
                "email": request.user.email,
                "phone_number": request.user.phone_number,
                "delivery_address": request.data.get("delivery_address"),
                "delivery_point": request.data.get("delivery_point"),
                "delivery_date": request.data.get("delivery_date"),
                "total_price": str(transaction.amount),
                "payment_method": "Payoneer",
                "payment_confirmation_number": transaction_id,
             }

             # Call the create_order view
            create_order(request._request)


            return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "Payment verification failed."}, status=status.HTTP_400_BAD_REQUEST)

    except requests.exceptions.RequestException as e:
        return Response({"error": "Payoneer verification request failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
