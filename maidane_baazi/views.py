from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def say_salaam(request):
    # return HttpResponse('sanga yi!')
    return render(request, 'salam_alik.html',{'name':'Haroon'})