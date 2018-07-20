from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import *

def index(req):
    return render(req, 'index.html', {'users': User.objects.all()})

def registration(req):
    print('check1')

    if req.method == 'POST':
        errors = User.objects.validate(req.POST)
        if not errors:            
            user = User.objects.create_user(req.POST)            
            req.session['user_id'] = user.id
        if errors:
            for key, value in errors.items():
                print(messages.error(req,value))
                print(errors.items)

        return redirect('/')
            
def login(req):
    errors = User.objects.validateLogin(req.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(req, value)
        return redirect('/')
    else:
        username = User.objects.get(email = req.POST['email']).first_name
        user_id = User.objects.get(email = req.POST['email']).id
        req.session['user_id'] = user_id
        req.session['user'] = username
        return redirect('/dashboard')

def dashboard(req):
    print("check")
    return render(req, 'dashboard.html', {'items': Item.objects.all()})

def create(req):
    req.session['user_id']
    return render(req,'create.html', {'items': Item.objects.all()})

def itemCreate(req):
    if req.method == 'POST':
        errors = Item.objects.validateItem(req.POST)
        if not errors:
            req.session['user_id']
            req.session['first_name']
            items = Item.objects.create_item(req.POST)
            return redirect('/dashboard')
        if errors:
            for key, value in errors.items():
                print(messages.error(req,value))
                print(errors.items)
            return redirect('/create')

def wish_items(req):
    print("check")
    return render(req,'wish_items.html', {'items': Item.objects.all()} )

def remove(req):
    
    return redirect('/dashboard')

def delete(req):
    
    return redirect('/dashboard')

def logout(req):
    req.session['id'] = 0
    return redirect('/')