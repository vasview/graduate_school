from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from main.views import StudentMenuView
from .forms import *
from .models import *


class ListStudyPlans(LoginRequiredMixin, StudentMenuView, View):
    template_name = 'study_plans/student_study_plans.html'

    def get_context_data(self, request, *args,**kwargs):
        context =  super().get_context_data(*args, **kwargs)
        user = request.user
        student = user.students.last()
        study_plans = student.study_plans.all()
        context['user'] = user
        context['student'] = student
        context['study_plans'] = study_plans
        return context

    def get(self,request,*args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

class ShowStudyPlan(StudentMenuView, View):
    template_name = 'study_plans/show_study_plan.html'

    def get_context_data(self, request, *args,**kwargs):
        context =  super().get_context_data(*args, **kwargs)
        user = request.user
        student = user.students.last()
        context['user'] = user
        context['student'] = student
        return context

    def get_study_plan(self):
        return get_object_or_404(StudyPlan, pk=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        context["study_plan"] = self.get_study_plan()
        return render(request, self.template_name, context)

class CreateStudyPlan(StudentMenuView, View):
    form_class = NewStudyPlan
    template_name = 'study_plans/create_study_plan.html'

    def get_context_data(self, request, *args,**kwargs):
        context =  super().get_context_data(*args, **kwargs)
        user = request.user
        student = user.students.last()
        context['user'] = user
        context['student_id'] = student.id
        return context

    def create_study_plan_work_scopes(self, study_plan_work):
        work_scopes = WorkScopeType.objects.filter(work_type=study_plan_work.work_type).order_by('sort')
        for scope in work_scopes:
            study_plan_work.study_work_scopes.create(work_scope=scope, 
                                                    subtitle=scope.title, 
                                                    is_section_title=True)

    def create_study_plan_works(self, study_plan):
        if study_plan.plan_type.year_of_study == 0:
            work_types = WorkType.objects.filter(active=True, is_genplan_visible=True)
        else:
            work_types = WorkType.objects.filter(active=True, is_visible=True)

        for work in work_types:
            study_plan_work = study_plan.study_plan_works.create(work_type=work)
            self.create_study_plan_work_scopes(study_plan_work)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        form = self.form_class(initial={'postgraduate': context['student_id']})
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        form = self.form_class(request.POST)
        if form.is_valid():
            study_plan = form.save()
            self.create_study_plan_works(study_plan)
            return redirect("student_study_plans:index")
        else:
            context['form'] = form
            return render(request, self.template_name, context)
