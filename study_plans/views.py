from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .forms import *

class ListStudyPlans(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'study_plans/student_study_plans.html')

class ShowStudyPlan(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'study_plans/show_study_plan.html')

class CreateStudyPlan(View):
    form_class = NewStudyPlan
    template_name = 'study_plans/create_study_plan.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,  request.FILES)
        if form.is_valid():
            # form.save()
            return redirect("home")
        else:
            return render(request, self.template_name, {'form': form})
