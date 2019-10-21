from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
    return render(request, 'signup.html', {'form': form,"type_page":"login"})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print("form.is_valid(): ",form.is_valid())
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('med_store:index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='med_store:login')
def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES,)
        document = None
        if form.is_valid():
            content = request.FILES['attachment']
            form.save()
            return render(request, 'add_doc.html', {
        'form':  DocumentForm()
    })
    else:
        form = DocumentForm()
    return render(request, 'add_doc.html', {
        'form': form
    })

@login_required(login_url='med_store:login')
def report(request):
    form = ReportForm()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            return form.save()
    return render(request, 'report.html', {
        'form': form
    })