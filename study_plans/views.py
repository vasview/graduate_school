from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .forms import *


menu = [{'title': 'Аспирантура', 'url_name': 'postgraduates:student_workspace'},
        {'title': 'Объяснительная записка', 'url_name': 'postgraduates:show_explanatory_note'},
        {'title': 'Мои планы', 'url_name': 'student_study_plans:index'},
        {'title': 'Мой профиль', 'url_name': 'postgraduates:student_workspace'},    
        {'title': 'Выход', 'url_name': 'logout'}
]


class ListStudyPlans(View):
    template_name = 'study_plans/student_study_plans.html'

    def get(self,request,*args, **kwargs):
        context = {
            'menu': menu
        }
        return render(request, self.template_name, context = context)

class ShowStudyPlan(View):
    template_name = 'study_plans/show_study_plan.html'

    def get(self,request,*args, **kwargs):
        context = {
            'menu': menu
        }
        return render(request, self.template_name, context = context)

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
