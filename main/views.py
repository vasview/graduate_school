import imp
from django.template import RequestContext
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from main.forms import *

class HomePage(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'index.html')

def user_login(request):
    next_page = ''
    if request.GET:
        next_page = request.GET['next']

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                if next_page == "":
                    return redirect('home')
                else:
                    return redirect(next_page)
            else:
                form.add_error(None, 'Ошибка входа')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form, 'next': next_page})

def user_logout(request):
    logout(request)
    return redirect(reverse_lazy('home'))
