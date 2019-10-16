from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        document = None
        if form.is_valid():
            content = request.FILES['attachment']
            form.save()
            return redirect('/')
    else:
        form = DocumentForm()
    return render(request, 'add_doc.html', {
        'form': form
    })

def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        document = None
        if form.is_valid():
            content = request.FILES['attachment']
            form.save()
            return redirect('/')
    else:
        form = DocumentForm()
    return render(request, 'report.html', {
        'form': form
    })