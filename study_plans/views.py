from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


class ListStudyPlans(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'study_plans/student_study_plans.html')

class ShowStudyPlan(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'study_plans/show_study_plan.html')

class CreateStudyPlan(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'study_plans/create_study_plan.html')
