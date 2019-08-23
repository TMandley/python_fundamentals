from django.shortcuts import render, HttpResponse, redirect
from .models import User, Job
from django.contrib import messages
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
    return render(request, "login_reg_app/index.html")

def success(request):
    # print(Job.objects.filter(posted_by=User.objects.get(id=request.session['id'])))
    thisuser = User.objects.get(id=request.session['id'])
    mylist = []
    for i in Job.objects.filter(posted_by=thisuser):
        mylist.append(i.id)
    somejobs = Job.objects.filter(active_user=None)
    print(somejobs.filter(posted_by=thisuser))
    otherjobs = somejobs.exclude(posted_by=thisuser)
    # for job in somejobs:
    #     print(job.title)
    # print(somejobs)
    context = {
        'thisuser': thisuser,
        'myjobs': Job.objects.filter(posted_by=thisuser),
        'otherjobs': otherjobs,
        'activejobs': thisuser.active_jobs.all(),
        'somejobs': somejobs,
    }
    # print(Job.objects.all())
    return render(request, "login_reg_app/success.html", context)
    # return redirect('/')

def destroy(request):
    thisuser = None
    request.session.clear()
    return redirect('/')


def regvalidate(request):
    if request.method == "POST":
        # print(request.POST)
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
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        thisuser = User.objects.get(email=request.POST['email'])
        request.session['id'] = thisuser.id
        return redirect('/dashboard')
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
    # return redirect(f'/success/{thisuser.id}')

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
        # print(errors)
        # print('*'*100)
        if errors != {}:
            # print('I SHOULD NOT BE HERE RIGHT NOW')
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        thisuser = User.objects.get(email=request.POST['email'])
        request.session['id'] = thisuser.id
        # print(thisuser.id)
        return redirect('/dashboard')
    else:
        return redirect('/')
    return redirect('/dashboard')

def newjob(request):
    context = {
        'thisuser': User.objects.get(id=request.session['id']),
    }
    return render(request, 'login_reg_app/newjob.html', context)

def processnewjob(request):
    thisuser = User.objects.get(id=request.session['id'])
    if request.method == 'POST':
        thisuser = User.objects.get(id=request.session['id'])
        print(request.POST)
        print('*'*100)
        errors = Job.objects.job_validator(request.POST)
        if errors != {}:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/jobs/new')
        else:
            cats = request.POST['othercategory']
            if request.POST.get('check') == None:
                cats = request.POST['othercategory']
            else:
                for i in range(len(request.POST.getlist('check'))):
                    cats = cats + ' ' + request.POST.getlist('check')[i]
            # print(request.POST.getlist('check'))
            # print(cats)
            Job.objects.create(title=request.POST['title'], location=request.POST['location'], description=request.POST['description'],categories=cats, posted_by=thisuser)

    return redirect('/dashboard')

def processjobedit(request):
    if request.method == 'POST':
        thisuser = User.objects.get(id=request.session['id'])
        thisjob = Job.objects.get(id=request.POST['jobid'])
        num = thisjob.id
        errors = Job.objects.job_validator(request.POST)
        if errors != {}:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/jobs/edit/{num}')
        thisjob.title = request.POST['title']
        thisjob.location = request.POST['location']
        thisjob.description = request.POST['description']
        thisjob.save()
    return redirect(f'/jobs/edit/{num}')

def processaddjob(request, num):
    thisjob = Job.objects.get(id=num)
    thisuser = User.objects.get(id=request.session['id'])
    thisjob.active_user = thisuser
    thisjob.save()
    print(thisjob.active_user.first_name)
    return redirect('/dashboard')

def deletejob(request, num):
    thisjob = Job.objects.get(id=num)
    thisjob.delete()
    return redirect('/dashboard')

def giveup(request, num):
    thisjob = Job.objects.get(id=num)
    thisjob.active_user = None
    thisjob.save()
    return redirect('/dashboard')

def editjob(request, num):
    context = {
        'thisuser': User.objects.get(id=request.session['id']),
        'thisjob': Job.objects.get(id=num),
    }
    return render(request, 'login_reg_app/editjob.html', context)

def jobinfo(request, num):
    context = {
        'thisuser': User.objects.get(id=request.session['id']),
        'thisjob': Job.objects.get(id=num),
    }
    return render(request, 'login_reg_app/jobinfo.html', context)
