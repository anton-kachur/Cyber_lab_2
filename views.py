from django.shortcuts import render, redirect
from .models import Task2
from .forms import Task2Form
from django.views.generic.list import ListView


import matplotlib
import matplotlib.pyplot as plt, mpld3
import numpy as np

from django.shortcuts import render

# Create your views here.
'''
class Task1View(ListView):
    model =Task1
    template_name = 'layout.html'
    context_object_name = 'tasks'''

def index(request):	
	if request.method == "POST":
		form = Task2Form(request.POST)
		if form.is_valid():
			form.save()
			return redirect('about')
			
			
	form = Task2Form()
	context = {
		'form': form
	}
	return render(request, 'main/index.html', context)
	
def about(request):
	ejde = Task2.objects.all()
	return render(request, 'main/about.html', {'ejde': ejde})
