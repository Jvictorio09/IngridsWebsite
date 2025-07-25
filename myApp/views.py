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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail

@csrf_exempt
def send_free_guide(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        guide_link = "https://drive.google.com/file/d/1rhp0sk79IqAVqYIC8mbsjSt8Zi6boUqZ/view?usp=sharing"

        # Email content
        subject = "Your Free Guide: Starting Your Story"
        message = f"""Hi There,

Every great story begins with a single step, and this guide is here to help you take yours! 🌿📖  
In 'Starting Your Story: How to Begin Writing in Your Notebook', you'll discover simple yet powerful ways to start writing, find inspiration, and build a meaningful writing habit.  

📎 Your free guide is attached—download it and let your creativity flow!  
{guide_link}

If you have any questions or need more tips, feel free to reach out.

Happy writing!

Ingrid Cruysberghs
Guidance for You
"""

        try:
            send_mail(
                subject,
                message,
                "ingrid@ingridcruysberghs.com",  # Replace with your default email
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

@csrf_exempt
def create_paypal_order(request, product_id):
    """Creates a PayPal order."""
    product = Product.objects.get(id=product_id)
    access_token = get_paypal_access_token()

    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "EUR",
                "value": str(product.get_price())
            }
        }]
    }

    response = requests.post(
        f"{PAYPAL_API_BASE}/v2/checkout/orders",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json=order_data,
    )

    return JsonResponse(response.json())

from django.core.mail import send_mail

def send_product_link_to_buyer(email, name, product_id):
    try:
        product = Product.objects.get(id=product_id)
        if product.pdf_link:
            subject = f"Download Your Product: {product.name}"
            message = f"""
Hi {name or 'there'},

Thank you for purchasing {product.name}!

You can download your product here:
{product.pdf_link}

Enjoy!
– The Ingrid Team
"""
            send_mail(subject, message, 'noreply@yourdomain.com', [email])
    except Product.DoesNotExist:
        pass


@csrf_exempt
def capture_paypal_order(request):
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

    capture_data = response.json()

    try:
        buyer_email = capture_data["payer"]["email_address"]
        buyer_name = capture_data["payer"]["name"]["given_name"]
    except KeyError:
        buyer_email = None
        buyer_name = None

    # Optionally send email with product PDF link
    if buyer_email:
        send_product_link_to_buyer(buyer_email, buyer_name, data.get("product_id"))

    return JsonResponse(capture_data)
