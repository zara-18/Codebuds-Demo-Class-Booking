from django.http import HttpResponse
import phonenumbers
from django.shortcuts import render,redirect
from .data import options
from scheduleclass.models import Contact
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.cache import never_cache

@never_cache
def home_page(request): 
    if request.user.is_authenticated:   # 👈 already logged in
        return redirect("demo_class") 
    message = "" 
    if request.method == "POST": 
        phone = request.POST.get("phone", "").strip() 
        try: 
            parsed_number = phonenumbers.parse(phone, None) 
            if phonenumbers.is_valid_number(parsed_number): 
                normalized_phone = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164) 
                user, created = User.objects.get_or_create(username=normalized_phone)
                login(request, user) 
                return redirect("demo_class")
            else: message = "❌ Invalid phone number format!" 
        except phonenumbers.NumberParseException: 
            message = "❌ Could not parse phone number!" 
    return render(request, "index.html", {"options": options, "message": message}) 
       
@login_required(login_url='/') 
def demo_class(request):
    email=""
    message=""
    phone = request.user.username 
    if Contact.objects.filter(phone_number=phone).exists():
        message = "❌ Free Class booked already!"
    if request.method == "POST":
        date = request.POST.get("class-date") 
        email=request.POST.get("email", "").strip() 
        grade=request.POST.get("grade")
        if not Contact.objects.filter(phone_number=phone).exists() and date:
            try:
                parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
                Contact.objects.create(phone_number=phone, date=parsed_date , parent_email=email, grade=grade)
                message = "✅ Class booked successfully!"
            except ValueError:
                message = "❌ Invalid date format!"           
    return render(request,"democlass.html", {"message": message , "email":email})

def logout_view(request):
    logout(request)   # clear session
    return redirect("home")

def enroll_view(request):
    message = "" 
    if request.method == "POST": 
        phone = request.POST.get("phone", "").strip() 
        date = request.POST.get("class-date") 
        email=request.POST.get("email", "").strip() 
        grade=request.POST.get("grade")
        try: 
            parsed_number = phonenumbers.parse(phone, None) 
            if phonenumbers.is_valid_number(parsed_number): 
                normalized_phone = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164) 
                if not Contact.objects.filter(phone_number=normalized_phone).exists() and date:
                    try:
                        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
                        Contact.objects.create(phone_number=phone, date=parsed_date , parent_email=email, grade=grade)
                        message = "✅ Trial Class enrolled successfully!"
                    except ValueError:
                        message = "❌ Invalid date format!" 
                else:
                    message = "❌ Trial Class enrolled already!"      
            else:
                message = "❌ Invalid phone number format!" 
        except phonenumbers.NumberParseException: 
            message = "❌ Could not parse phone number!" 
    return render(request, "enroll.html", {"options": options, "message": message})