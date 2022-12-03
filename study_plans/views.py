from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from main.views import StudentMenuView
from .forms import *
from .models import *


class ListStudyPlans(LoginRequiredMixin, StudentMenuView, ListView):
    model = StudyPlan
    template_name = 'study_plans/student_study_plans.html'
    context_object_name = 'study_plans'
    login_url = '/login/'

    def get_context_data(self, *args,**kwargs):
        context =  super().get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        user = self.request.user
        student = user.students.last()
        return StudyPlan.objects.filter(postgraduate=student)


class ShowStudyPlan(LoginRequiredMixin, StudentMenuView, DetailView):
    model = StudyPlan
    template_name = 'study_plans/show_study_plan.html'
    pk_url_kwarg = 'id'
    context_object_name = 'study_plan'
    login_url = '/login/'

    def get_context_data(self, *args,**kwargs):
        context =  super().get_context_data(*args, **kwargs)
        return context


class CreateStudyPlan(LoginRequiredMixin, StudentMenuView, CreateView):
    form_class = NewStudyPlan
    template_name = 'study_plans/create_study_plan.html'
    login_url = '/login/'
    # success_url = reverse_lazy("student_study_plans:index")

    def get_success_url(self):
        return reverse_lazy("student_study_plans:index")

    def get_context_data(self, *args,**kwargs):
        context = super(CreateStudyPlan, self).get_context_data(*args, **kwargs)
        return context

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        user = self.request.user
        initial['postgraduate'] = user.students.last()
        return initial
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CreateStudyPlan, self).get_form_kwargs(*args, **kwargs)
        user = self.request.user
        kwargs['postgraduate'] = user.students.last()
        return kwargs

    def create_study_plan_work_scopes(self, study_plan_work):
        work_scopes = WorkScopeType.objects.filter(work_type=study_plan_work.work_type).order_by('sort')
        for scope in work_scopes:
            study_plan_work.study_work_scopes.create(work_scope=scope)

    def create_study_plan_works(self, study_plan):
        if study_plan.plan_type.year_of_study == 0:
            work_types = WorkType.objects.filter(active=True, is_genplan_visible=True)
        else:
            work_types = WorkType.objects.filter(active=True, is_visible=True)

        for work in work_types:
            study_plan_work = study_plan.study_plan_works.create(work_type=work)
            self.create_study_plan_work_scopes(study_plan_work)

    def form_valid(self, form):
        study_plan = form.save()
        self.create_study_plan_works(study_plan)
        return HttpResponseRedirect(self.get_success_url())


class AddStudyWorkScopeDetails(LoginRequiredMixin, StudentMenuView, CreateView):
    form_class = StudyPlanScopeDetailsForm
    template_name = 'study_plans/add_work_scope_details.html'
    login_url = '/login/'

    def get_success_url(self):
        work_scope = self.get_study_work_scope()
        plan_id = work_scope.study_plan_work.study_plan_id
        return reverse_lazy("student_study_plans:show_study_plan", kwargs={'id': plan_id})

    def get_form_class(self):
        study_work_scope = self.get_study_work_scope()
        if study_work_scope.work_scope.code == 'subject' or study_work_scope.work_scope.code == 'exam':
            return StudyPlanSubjectDetailsForm
        else:
            return StudyPlanScopeDetailsForm

    def get_study_work_scope(self):
        return get_object_or_404(StudyWorkScope, pk=self.kwargs['id'])

    def get_context_data(self, *args,**kwargs):
        context =  super(AddStudyWorkScopeDetails, self).get_context_data(*args, **kwargs)
        return context

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        work_scope = self.get_study_work_scope()
        initial['study_work_scope'] = work_scope
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AddStudyWorkScopeDetails, self).get_form_kwargs(*args, **kwargs)
        work_scope = self.get_study_work_scope()
        kwargs['study_work_scope'] = work_scope
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

class DeleteStudyWorkScopeDetails(LoginRequiredMixin, StudentMenuView, DeleteView):
    model = StudyWorkScopeDetails
    pk_url_kwarg = 'id'
    template_name = 'confirm_delete.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вы точно хотите удалить краткое содержание и объем работы?'
        return context

    def get_object(self):
        return get_object_or_404(StudyWorkScopeDetails, pk=self.kwargs['id'])

    def get_success_url(self):
        scope_details = self.get_object()
        plan_id = scope_details.study_work_scope.study_plan_work.study_plan_id
        return reverse_lazy('student_study_plans:show_study_plan', kwargs={'id': plan_id})
