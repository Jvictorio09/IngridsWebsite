from django.shortcuts import render

def index(request):
    return render(request, 'myApp/index.html', {'range': range(1, 7)})

def about(request):
    return render(request, 'myApp/about.html')

def bookings(request):
    return render(request, 'myApp/bookings.html')


def readings(request):
    return render(request, 'myApp/readings.html')

def business(request):
    return render(request, 'myApp/business.html')

def guidanceplan(request):
    return render(request, 'myApp/guidanceplan.html')


def contact(request):
    return render(request, 'myApp/contact.html')


from django.shortcuts import render

def team_view(request):
    team_members = [
        {"name": "Jessica Brown", "position": "Sycho Founder", "image": "assets/images/team/team-3-1.jpg", "details_url": "team-details.html", "stars": 4},
        {"name": "Locus Singh", "position": "Sycho Founder", "image": "assets/images/team/team-3-2.jpg", "details_url": "team-details.html", "stars": 4},
        {"name": "Alesa Brown", "position": "Sycho Founder", "image": "assets/images/team/team-3-3.jpg", "details_url": "team-details.html", "stars": 4},
    ]
    return render(request, 'team_template.html', {"team_members": team_members})



from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def send_free_guide(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        guide_link = "https://docs.google.com/document/d/1y2drh4SuOeIyjhgQLDVRBDWu_LQ76HtLyd3v3zW20yY/edit?usp=sharing"

        # Email content
        subject = "Your Free Guide: Starting Your Story"
        message = f"""
        Hi {name},

        Thank you for signing up! 🎉

        Here is your free guide to get started:  
        📄 {guide_link}

        Happy writing! ✍️
        - The Team
        """
        
        try:
            send_mail(
                subject,
                message,
                "juliavictorio16@gmail.com",  # Change to your default email
                [email],
                fail_silently=False,
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request method"})


from django.shortcuts import render
from .models import Product

def shop(request):
    products = Product.objects.all()
    return render(request, 'myApp/shop.html', {'products': products})

from django.shortcuts import render
from .models import Product

def testshop(request):
    products = Product.objects.all()
    return render(request, 'myApp/testshop.html', {'products': products})

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'myApp/product_detail.html', {'product': product})


import json
import requests
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product

# Fetch PayPal credentials securely
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PAYPAL_API_BASE = os.getenv("PAYPAL_API_BASE")

def get_paypal_access_token():
    """Fetches PayPal API Access Token securely."""
    response = requests.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
    )
    return response.json()["access_token"]

import requests
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Product
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def create_paypal_order(request, product_id):
    """Creates a PayPal order dynamically based on the selected product."""
    
    product = get_object_or_404(Product, id=product_id)  # Fetch product details
    url = f"{settings.PAYPAL_API_BASE}/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_paypal_access_token()}"
    }

    data = {
    "intent": "CAPTURE",
    "purchase_units": [
        {
            "reference_id": str(product.id),
            "description": product.name,
            "amount": {
                "currency_code": "USD",
                "value": str(product.price),  # Total amount
                "breakdown": {
                    "item_total": {
                        "currency_code": "USD",
                        "value": str(product.price)  # Ensure this matches the total
                    }
                }
            },
            "items": [
                {
                    "name": product.name,
                    "sku": str(product.id),
                    "unit_amount": {
                        "currency_code": "USD",
                        "value": str(product.price)
                    },
                    "quantity": 1
                }
            ]
        }
    ]
}


    response = requests.post(url, headers=headers, json=data)
    
    try:
        response_json = response.json()
        logger.error(f"PayPal API Response: {response_json}")  # Log PayPal's response
    except Exception as e:
        logger.error(f"Error decoding PayPal response: {e}")
        return JsonResponse({"error": "Invalid PayPal response"}, status=400)

    if response.status_code == 201:
        return JsonResponse(response_json)
    else:
        return JsonResponse(response_json, status=response.status_code)
    

@csrf_exempt
def create_paypal_cart_order(request):
    """Creates a PayPal order for multiple products in the cart."""
    try:
        data = json.loads(request.body)
        cart_items = data.get("items", [])
        total_price = data.get("total", 0.00)

        if not cart_items:
            return JsonResponse({"error": "Cart is empty"}, status=400)

        url = f"{PAYPAL_API_BASE}/v2/checkout/orders"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_paypal_access_token()}"
        }

        purchase_units = [{
            "amount": {
                "currency_code": "USD",
                "value": str(total_price),
                "breakdown": {
                    "item_total": {
                        "currency_code": "USD",
                        "value": str(total_price)
                    }
                }
            },
            "items": cart_items
        }]

        data = {
            "intent": "CAPTURE",
            "purchase_units": purchase_units
        }

        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        
        logger.error(f"PayPal API Response: {response_json}")  # Log PayPal's response
        
        if response.status_code == 201:
            return JsonResponse(response_json)
        else:
            return JsonResponse(response_json, status=response.status_code)

    except Exception as e:
        logger.error(f"Error creating PayPal cart order: {e}")
        return JsonResponse({"error": "Something went wrong"}, status=500)    


@csrf_exempt
def capture_paypal_order(request):
    """Captures PayPal order after approval."""
    data = json.loads(request.body)
    order_id = data.get("orderID")
    access_token = get_paypal_access_token()

    response = requests.post(
        f"{PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
    )

    return JsonResponse(response.json())


import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product

import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product

from django.http import JsonResponse

def add_to_cart(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        product_id = str(data.get("product_id"))
        product_name = data.get("name")
        product_price = data.get("price")

        cart = request.session.get("cart", {})

        if product_id in cart:
            cart[product_id]["quantity"] += 1
        else:
            cart[product_id] = {
                "name": product_name,
                "price": product_price,
                "quantity": 1,
                "image_url": f"/media/products/{product_id}.jpg"  # Update with actual image path logic
            }

        request.session["cart"] = cart
        request.session.modified = True  # ✅ Ensure session updates

        return JsonResponse({
            "success": True,
            "cart_count": len(cart),
            "cart_items": list(cart.values())  # ✅ Return cart items
        })

    return JsonResponse({"success": False}, status=400)


from django.http import JsonResponse

def cart_view(request):
    cart = request.session.get("cart", {})
    cart_items = list(cart.values())  # Convert session dict to list

    return JsonResponse({"cart_items": cart_items})


import json
from django.http import JsonResponse

def remove_from_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")

            cart = request.session.get("cart", {})

            if product_id in cart:
                del cart[product_id]  # Remove the item
                request.session["cart"] = cart

            total_price = sum(float(item["price"]) * item["quantity"] for item in cart.values())

            return JsonResponse({"success": True, "total_price": total_price})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def cart_view(request):
    cart = request.session.get("cart", {})
    total_price = sum(float(item["price"]) * item["quantity"] for item in cart.values())

    print("Cart Data in Session:", cart)  # Debugging

    return render(request, "myApp/cart.html", {"cart": cart, "total_price": total_price})
