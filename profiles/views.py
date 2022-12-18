from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages

from .models import *
from main.models import MenuItems
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

class PasswordChange(LoginRequiredMixin, View):
    form_class = SetPasswordForm
    template_name = 'profiles/password_reset_confirm.html'
    login_url = '/login/'

    def get_context_data(self, request, *args,**kwargs):
        # context = super().get_context_data(**kwargs)
        user = request.user
        user_group = user.groups.first()
        context = {
            'user': user,
            'form': self.form_class(user),
            'menu': MenuItems.objects.filter(is_active=True, seen_by=user_group.id)
        }
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = self.get_context_data(request)
            return render(request, self.template_name, context)
        return redirect('login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            form = self.form_class(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Ваш пароль был успешно изменен.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                context = self.get_context_data(request)
                return render(request, self.template_name, context)

