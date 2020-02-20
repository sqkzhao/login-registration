from django.shortcuts import render, redirect
from django.contrib import messages
from login_app.models import *
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.validate_register(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(last_name=request.POST['last_name'], first_name=request.POST['first_name'], email=request.POST['email'], password=pw_hash, dob=request.POST['dob'])
        request.session['user_name'] = request.POST['first_name']
        messages.success(request, "Successfully registered (or logged in)!")
        return redirect('/success')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_name'] = user[0].first_name
        messages.success(request, "Successfully registered (or logged in)!")
        return redirect('/success')
        
def success(request):
    errors = User.objects.validate_success(request.session)
    if len(errors) > 0: # permission denied appears twice
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        return render(request, "success.html")

def logout(request):
    request.session.clear()
    return redirect('/')