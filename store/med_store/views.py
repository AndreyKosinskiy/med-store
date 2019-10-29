from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

import datetime
from .forms import DocumentForm, ReportForm, SignUpForm, LogInForm

# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('med_store:login')


def login_view(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('med_store:index')
    else:
        form = LogInForm()
    return render(request, 'signup.html', {'form': form, "type_page": "login"})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print("form.is_valid(): ", form.is_valid())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('med_store:index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='med_store:login')
def index(request):
    if request.method == 'POST':
        # it is go to clean form metod
        a = datetime.datetime.now()
        if request.POST.get("add"):
            operation_btn = request.POST.get("add")
            operation_msg = "Push+"
        elif request.POST.get("sub"):
            operation_btn = request.POST.get("sub")
            operation_msg = "Get-"
        #
        form = DocumentForm(request.POST, request.FILES,
                            operation_btn=operation_btn)
        if form.is_valid():
            form = form.save(commit=False)
            # it is go to model method
            form.operation_btn = operation_btn
            form.user = request.user
            #
            form.save()
            messages.success(request,
                             f'<h1 class = "text-success">Операція Виконана {operation_msg}!</h1>',
                             extra_tags='safe')
            # return render(request, 'add_doc.html', {'form':  DocumentForm()})
            print("time for view: ",datetime.datetime.now()-a)
            return redirect('med_store:index')
    else:
        form = DocumentForm(operation_btn=None)
    return render(request, 'add_doc.html', {
        'form': form
    })

@login_required(login_url='med_store:login')
def report(request):
    form = ReportForm()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            table = form.save()
            return render(request, 'report.html', {
                'form': form, 'table': table
            })
    return render(request, 'report.html', {
        'form': form
    })
