from django.shortcuts import render

def home(request):
    return render(request,'ecommerce/index.html')
# Create your views here.
