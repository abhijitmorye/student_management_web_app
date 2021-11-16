from django.shortcuts import render

# Create your views here.


def sampleDemo(request):
    return render(request, 'demo.html')
