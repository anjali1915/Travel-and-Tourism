from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout as auth_logout
from .forms import loginForm, RegisterForm, ContactDetails, FormProfile
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django import forms
from registration_data.models import CustomUser
from django.core.cache import cache
from django.shortcuts import render
from BharatYatra.google_api import get_user_location, get_nearby_places, get_place_image
from django.http import JsonResponse
from contact.models import ContactData
from profileapp.models import User_Profile, User_post
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        form = loginForm(request.POST) #creates instance of form.py LoginForm.py class
        if form.is_valid():
            username = form.cleaned_data.get('username') #cleaned data checks the value entered by the user are in proper format 
            password = form.cleaned_data.get('password') #if not then clean the data, not add in db 
            remember_me = form.cleaned_data.get('remember_me')
            
            # Authenticate the user
            if not username or not password:
                messages.error(request, "Username and Password are required")
                return render(request, 'login_page.html', {'form': form})

            # Authenticate the user, check user is registered or not
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(f"User authenticated: {user.username}")
                # Log the user in, if user is allready registered 
                login(request, user)
                print(f"Authentication failed for username: {username}")
                # Set session to expire on browser close if 'remember_me' is not checked
                if not remember_me:
                    request.session.set_expiry(0)
                
                # Redirect to home page after successful login
                return redirect('profile_page')
            else:
                # Add error if authentication fails
                messages.error(request, "Invalid username or password")
    else:
        # Initialize an empty form if GET request
        form = loginForm()
    
    # Render the login page with the form
    return render(request, 'login_page.html', {'form': form})

def user_register(request):
    if request.method=="POST":
        register_data=RegisterForm(request.POST)
        if register_data.is_valid():
            name=register_data.cleaned_data.get('fullname')
            username=register_data.cleaned_data.get('username')
            email=register_data.cleaned_data.get('email')
            phone=register_data.cleaned_data.get('phone')
            password=register_data.cleaned_data.get('password')
            confirm_password=request.POST.get('confirm_password')
            gender=register_data.cleaned_data.get('gender')

            #password confirmation with confirm password
            if password != confirm_password:
                messages.error(request, "Password is not same") # Show an error message if password is not same
                return render(request, "register.html", {'register_data': register_data})
            
             # Check if username or email already exists
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
                return render(request, "register.html", {'register_data': register_data})
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
                return render(request, "register.html", {'register_data': register_data})
            
            # Create and save the user
            user = CustomUser(
                username=username,
                email=email,
                password=password,
                fullname=name,
                phone=phone,
                gender=gender 
            )
            user.set_password(password)  # Hash the password
            user.save()
            # Create a User_Profile instance
            User_Profile.objects.create(user=user)
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login_page')
        else:
            # Show an error message for invalid form
            messages.error(request, "Something went wrong. Please check the form.")
            if not register_data.is_valid():
                print(register_data.errors)  # Debug invalid form errors

    else:
        register_data = RegisterForm()  # Initialize empty form for GET requests

 # Initialize empty form

    return render(request, "register.html", {'register_data': register_data})

class SendMail(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html' 
    def get_subject(self):
        return "Your Password Reset Request"

def home(request):
    return render(request, "home_page.html")

def travel_view(request):
    """
    Handle travel view requests, including retrieving user location, nearby places,
    distance calculations, and place images, with caching for performance.
    """
    context = {}
    if request.method == 'GET':
        # Get latitude and longitude from GET parameters
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')

        if lat and lng:
            try:
                # Generate a unique cache key for the location
                cache_key = f"travel_data_{lat}_{lng}"
                cached_data = cache.get(cache_key)

                # Return cached data if available
                if cached_data:
                    return render(request, 'travel.html', cached_data)

                # Convert latitude and longitude to floats
                lat = float(lat)
                lng = float(lng)

                # Fetch user location (reverse geocode)
                location = get_user_location(lat, lng)

                # Fetch nearby places
                nearby_places = get_nearby_places(lat, lng)

                # Fetch images for nearby places
                for place in nearby_places:
                   if 'photos' in place and place['photos']:
                       place['image_url'] = get_place_image(place['photos'][0]['photo_reference'])
                   else:
                       place['image_url'] = None  # No image available
                # Prepare context data
                context = {
                    'location': location,
                    'nearby_places': nearby_places,
                }

                # Cache the context data for 1 hour
                cache.set(cache_key, context, timeout=3600)

                # Render the template with the context
                return render(request, 'travel.html', context)
            except Exception as e:
                # Log the exception for debugging and return an error response
                context['error'] = str(e)
                return render(request, 'travel.html', context)
        else:
            # If latitude and longitude are not provided, show an error or default message
            context['error'] = "Latitude and Longitude are required to fetch travel data."
            return render(request, 'travel.html', context)

    # For non-GET requests, simply render the template with an empty context
    return render(request, 'travel.html', context)

def contact_page(request):
    if request.method == 'POST':
        contact_data= ContactDetails(request.POST)
        if contact_data.is_valid():
            print("Form is valid")  # Debug statement
            ContactData.objects.create(
                name=contact_data.cleaned_data.get('name'),
                phone=contact_data.cleaned_data.get('phone'),
                email=contact_data.cleaned_data.get('email'),
                message=contact_data.cleaned_data.get('message'),
            )
            print("Data saved to database")  # Debug statement
            return render(request, "contact_us.html", {"success": True})
        else:
            print("Form is invalid") 
            print(contact_data.errors)  
    else:
        contact_data = ContactDetails()
        print("GET request received")  # Debug statement
    return render(request, "contact_us.html", {"form": contact_data})

def Post(request):
    return render(request, "post.html")

def social(request):
    return render(request, "social.html")

@login_required
def Profile_view(request):
    try:
        profile = User_Profile.objects.get(user=request.user)
    except User_Profile.DoesNotExist:
        return redirect('register')
        # Redirect to a profile creation page or show an error
    return render(request, 'profile_page.html', {'profile': profile})

def Profile_Edit(request):
    edit_profile = User_Profile.objects.get(user=request.user)
    if request.method == 'POST':
        edit_form = FormProfile(request.POST, request.FILES, instance=edit_profile)
        if edit_form.is_valid:
            edit_form.save()
            return redirect('profile_page')
    else:
        edit_form = FormProfile(instance=edit_profile)
    return render(request, "edit_profile.html", {'edit_form': edit_form})

def logout(request):
    auth_logout(request)
    return render(request, "login_page.html")