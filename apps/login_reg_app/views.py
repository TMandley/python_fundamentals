from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
    return render(request, "login_reg_app/index.html")

def success(request, num):
    if int(num) == int(request.session['id']):
        context = {
            'thisuser': User.objects.get(id=num)
        }
        return render(request, "login_reg_app/success.html", context)
    return redirect('/')

def destroy(request):
    thisuser = None
    request.session.clear()
    return redirect('/')


def regvalidate(request):
    if request.method == "POST":
        print(request.POST)
        # print('POST RECEIVED')
        # print('*'*100)
        errors = User.objects.basic_validator(request.POST)
        if errors != {}:
            # print('ERRORS FOUND')
            # print(errors)
            # print('*'*100)
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], birthday=request.POST['birthday'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        thisuser = User.objects.get(email=request.POST['email'])
        request.session['id'] = thisuser.id
        return redirect(f'/success/{thisuser.id}')
    if request.method == "GET":
        context = {}
        # print(request.GET)
        if not EMAIL_REGEX.match(request.GET['email']):
            context['email'] = 1
        try:
            findme = User.objects.get(email=request.GET['email'])
        except User.DoesNotExist:
            findme = None
        if findme:
            context['email'] = 2
        return render(request, 'login_reg_app/partials/checkreg.html', context)
    return redirect(f'/success/{thisuser.id}')

def regfnvalidate(request):
    context = {}
    if len(request.GET['first_name']) < 2:
        context['first_name'] = 1
    if len(request.GET['first_name']) > 2:
        context['first_name'] = 0
    return render(request, 'login_reg_app/partials/checkreg.html', context)

def reglnvalidate(request):
    context = {}
    if len(request.GET['last_name']) < 2:
        context['last_name'] = 1
    if len(request.GET['last_name']) > 2:
        context['last_name'] = 0
    return render(request, 'login_reg_app/partials/checkreg.html', context)


def logvalidate(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if errors != {}:
            # print('I SHOULD NOT BE HERE')
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        thisuser = User.objects.get(email=request.POST['email'])
        request.session['id'] = thisuser.id
        print(thisuser.id)
        return redirect(f'/success/{thisuser.id}')
    else:
        return redirect('/')
    return redirect(f'/success/{thisuser.id}')
