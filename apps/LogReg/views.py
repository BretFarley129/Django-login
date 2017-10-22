# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

import bcrypt

# Create your views here.

def index(request):
    return render(request,'LogReg/index.html')

def success(request):
    context = {}
    context['stuff'] = User.objects.all()
    return render(request,'LogReg/success.html',context)

def register(request):
    first = request.POST['first']
    last = request.POST['last']
    email = request.POST['email']
    password = request.POST['password']
    confirm = request.POST['confirm']
    x = {'first': first,'last': last, 'email': email, 'password': password, 'confirm': confirm}
    errors = User.objects.validate(x)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first = first, last = last, email = email, password = hashed_password )
        return redirect('/success')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        user = User.objects.get(email = email)
        hash1 = user.password
    except:
        hash1 = request.POST['email']


    x = { 'email': email, 'password': password, 'hash1' : hash1}
    errors = User.objects.validateLogin(x)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
       return redirect('/success')