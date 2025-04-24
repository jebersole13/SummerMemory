from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .model import Topic,Entry

def home(request):
    return render(request, 'index.html')

