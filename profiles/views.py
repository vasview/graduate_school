from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import *
from .forms import *
from main.views import StudentMenuView, SupervisorMenuView

class ShowStudentProfile(LoginRequiredMixin, StudentMenuView, View):
    template_name = 'profiles/show_student_profile.html'
    login_url = '/login/'

    def get_context_data(self, request, *args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = request.user
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

class ShowSupervisorProfile(LoginRequiredMixin, SupervisorMenuView, View):
    template_name = 'profiles/show_supervisor_profile.html'
    login_url = '/login/'

    def get_context_data(self, request, *args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = request.user
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)
