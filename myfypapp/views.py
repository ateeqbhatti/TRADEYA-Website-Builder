from django.views.generic import RedirectView
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from . import views
from .models import Pages
# from .forms import ContactForm
# from .models import Contact
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
import openai, os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_KEY", None)
 
def chatbot(request):
    chatbot_response = None
    if api_key is not None and request.method== 'POST':
        openai.api_key = api_key
        user_input= request.POST.get('user_input')
        prompt= user_input
        
        response = openai.Completion.create(
            engine = 'text-curie-001',
            prompt = prompt,
            max_tokens=256,
            # stop='.'
            temperature=0.5
        )
        chatbot_response=response["choices"][0]["text"]
        print(chatbot_response)
        
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        return HttpResponse(chatbot_response)
    else:
        return render(request, 'editor.html', {'response': chatbot_response})





# Create your views here.

# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             company_name = form.cleaned_data['company_name']
#             tagline = form.cleaned_data['tagline']
#             address = form.cleaned_data['address']
#             contact = form.cleaned_data['contact']
#             context = {'name': name, 'email': email,'company_name':company_name,'tagline':tagline,'address':address,'contact':contact}
#             return render(request, 'main_page/index.html', context)
#         messages.success(request, 'Your Record has been saved.')
            
#     else:
#         form = ContactForm()
#     return render(request, 'forms.html', {'form': form})

# def contact_list(request):
#     contacts = Contact.objects.all()
#     return render(request, 'client_data.html', {'contacts': contacts})
# def contact_detail(request, id):
#     contact = get_object_or_404(Contact, id=id)
#     return render(request, 'client_datanew.html', {'contact': contact, 'id': id})
# def contact_update(request, id):
#     contact = get_object_or_404(Contact, id=id)
#     form = ContactForm(request.POST or None, instance=contact)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Contact Updated successfully')
#         return redirect(reverse('contact_detail', args=[id]))
#     return render(request, 'forms.html', {'form': form})
# def contact_delete(request, id):
#     contact = get_object_or_404(Contact, id=id)
#     contact.delete()
#     return redirect(reverse('contact_list'))

# Editor Builder Display
def editor(request):
    if request.method == 'POST':
        # Call chatbot view to get response
        chatbot_response = views.chatbot(request)
        return render(request, 'editor.html', {'response': chatbot_response})
    else:
        return render(request, 'editor.html')


#Homepage
def main(request):
    return render(request, 'main_page/index.html')


# New User Creation
def signup(request):
    if request.method=='POST':
        #getting post parameteres
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        #creating checks
        if pass1!=pass2:
            messages.error(request,'Passwords do not match')
            return redirect('/')
        

        # creating user
        myuser= User.objects.create_user(name,email,pass1)
        myuser.first_name=name
        myuser.save()
        messages.success(request,'Your TRADEYA account has been successfully created')
        return redirect('/')
        
    else:
        return HttpResponse("404 Not Found") 

# User Login Checker whether it exists or not returning to same page  
def user_login(request):
    if request.method=='POST':
        loginusername=request.POST.get('loginusername')
        loginpass=request.POST.get('loginpass')
        user=authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request,user)
            request.session['loginusername']=loginusername
            messages.success(request,'Successfully Logged in')
            return redirect('/')
        else:
            messages.error(request,'Inavlid Credentials')
            return redirect('/')
  
# User Login Checker whether it exists or not and returning to Editor Builder page          
def user_login2(request):
    if request.method=='POST':
        loginusername=request.POST.get('loginusername')
        loginpass=request.POST.get('loginpass')
        user=authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request,user)
            request.session['loginusername']=loginusername
            messages.success(request,'Successfully Logged in')
            return redirect('/editor')
        else:
            messages.error(request,'Inavlid Credentials')
            return redirect('/')
        
# User Login Checker whether it exists or not and returning to User Data gathering for Auto Generation of Template                  
def user_login3(request):
    if request.method=='POST':
        loginusername=request.POST.get('loginusername')
        loginpass=request.POST.get('loginpass')
        user=authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request,user)
            request.session['loginusername']=loginusername
            messages.success(request,'Successfully Logged in')
            return redirect('/profile/add')
        else:
            messages.error(request,'Inavlid Credentials')
            return redirect('/') 
        
        
#Logging out the user        
def user_logout(request):
    logout(request)
    messages.success(request,'Successfully Logged out')
    return redirect('/')

#Changing user password        
def password_changed(request):
    messages.success(request,'Password Changed Successfully')
    return redirect('/')


# Collecting user's data in order to Auto generate Template 
@login_required
def profile_add(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        user_profile.name = request.POST.get('name')
        user_profile.phone = request.POST.get('phone')
        user_profile.company_name = request.POST.get('company_name')
        user_profile.email = request.POST.get('email')
        user_profile.address=request.POST.get('address')
        user_profile.category = request.POST.get('category')
        user_profile.save()
        return redirect('template_view')
    # ok so next task is in the place of  redirect profile i'll redirect user to my offered templates page , after selecting one he'll land in the editor with th key value pairs
    else:
        return render(request, 'profile_add.html', {'user_profile': user_profile})


# Viewing the Data Collected above
@login_required
def profile_view(request):    
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile_view.html', {'user_profile': user_profile})


# Available templates list view
def template_view(request):
    return render(request,'templates_view.html')

# Rendering Auto Generated Template 1 
def template1(request):
# remember this, this is the main point that wille be used in templates  render
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,'template1.html', {'user_profile': user_profile})

# Rendering Auto Generated Template 2
def template2(request):
# remember this, this is the main point that wille be used in templates  render
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,'template2.html', {'user_profile': user_profile})

# Rendering Auto Generated Template 3
def template3(request):
# remember this, this is the main point that wille be used in templates  render
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,'template3.html', {'user_profile': user_profile})


# Rendering Auto Generated Template 4
def template4(request):
# remember this, this is the main point that wille be used in templates  render
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request,'template4.html', {'user_profile': user_profile})


def error_404_view(request, exception):
    return render(request, '404.html', {})
