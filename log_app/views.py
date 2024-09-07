from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'kyoyu_app/login.html')

def home(request):
    return render(request, 'kyoyu_app/home.html')

def make_kyoyusheet(request):
    return render(request, 'kyoyu_app/make_kyoyusheet.html')