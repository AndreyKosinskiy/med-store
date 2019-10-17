from django.shortcuts import render, redirect
from .forms import DocumentForm, ReportForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        document = None
        if form.is_valid():
            content = request.FILES['attachment']
            form.save()
            #return redirect('/')
            return render(request, 'add_doc.html', {
        'form':  DocumentForm()
    })
    else:
        form = DocumentForm()
    return render(request, 'add_doc.html', {
        'form': form
    })

def report(request):
    form = ReportForm()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        print(form.is_valid())
        print ( request.POST["start_date"] )
        print ( request.POST["end_date"] )
        print ( request.POST["store"] )
        if form.is_valid():
            form.save()
            return form.save()
    return render(request, 'report.html', {
        'form': form
    })