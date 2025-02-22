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


def shop(request):
    return render(request, 'myApp/shop.html')

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
