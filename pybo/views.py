from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<h1>안녕하세요.</h1> pybo에 오신것을 환영합니다.")