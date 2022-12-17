from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
import json

from .models import *
from .forms import *
from main.views import StudentMenuView, SupervisorMenuView

class StudentWorkspace(LoginRequiredMixin, StudentMenuView, View):
    template_name = 'postgraduates/student_workspace.html'
    login_url = '/login/'

    def is_group_member(self, group):
        user = self.request.user
        return user.groups.filter(name=group).exists()

    def get_context_data(self, request, *args,**kwargs):
        context =  super().get_context_data(*args, **kwargs)
        user = request.user
        student = user.students.last()
        topic = student.topics.last()
        context['user'] = user
        context['student'] = student
        context['topic'] = topic
        return context

    def get(self, request, *args, **kwargs):
        if not self.is_group_member('Students'):
            return redirect('home')
        context = self.get_context_data(request)
        # assert False
        return render(request, self.template_name, context)

class EditDissertationTopic(LoginRequiredMixin, StudentMenuView, UpdateView):
    model = DissertationTopic
    form_class = EditDissertationTopic
    template_name = 'postgraduates/edit_dissertation_topic.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('postgraduates:student_workspace')

class ShowExplanatoryNote(LoginRequiredMixin, StudentMenuView, View):
    """
    shows explanatory note for student
    """
    model = ExplanatoryNote
    context_object_name = 'expl_note'
    template_name = 'postgraduates/show_explanatory_note.html'
    login_url = '/login/'

    def get_context_data(self, request, *args,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = request.user
        student = user.students.last()
        expl_note = student.explanatory_notes.last()
        context['expl_note'] = expl_note
        context['topic_approval_status'] = expl_note.get_status_css(expl_note.topic_approval_status)
        context['purpose_approval_status'] = expl_note.get_status_css(expl_note.purpose_approval_status)
        context['value_approval_status'] = expl_note.get_status_css(expl_note.value_approval_status)
        context['result_approval_status'] = expl_note.get_status_css(expl_note.result_approval_status)
        context['application_approval_status'] = expl_note.get_status_css(expl_note.application_approval_status)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

class EditExplanatoryNote(LoginRequiredMixin, StudentMenuView, UpdateView):
    model = ExplanatoryNote
    form_class = EditExplanatoryNote
    template_name = 'postgraduates/edit_explanatory_note.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        # id = self.object.postgraduate.id
        return reverse_lazy('postgraduates:show_explanatory_note')

class SupervisorStudentCard(LoginRequiredMixin, SupervisorMenuView, DetailView):
    """
    shows postgraduate card for supervisor
    """
    model = Postgraduate
    context_object_name = 'postgraduate'
    template_name = 'postgraduates/supervisor_student_card.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SupervisorStudentExplanatoryNote(LoginRequiredMixin, SupervisorMenuView, DetailView):
    """
    shows postgraduate explanatory note for supervisor
    """
    model = ExplanatoryNote
    context_object_name = 'expl_note'
    template_name = 'postgraduates/supervisor_student_explanatory_note.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic_approval_status_css'] = self.object.get_status_css(self.object.topic_approval_status)
        context['purpose_approval_status_css'] = self.object.get_status_css(self.object.purpose_approval_status)
        context['value_approval_status_css'] = self.object.get_status_css(self.object.value_approval_status)
        context['result_approval_status_css'] = self.object.get_status_css(self.object.result_approval_status)
        context['application_approval_status_css'] = self.object.get_status_css(self.object.application_approval_status)
        return context

class AjaxUApproveExplanatoryNote(LoginRequiredMixin, View):
    """
    let supervisor to approve one section of an explanatory note
    """
    model = ExplanatoryNote
    pk_url_kwarg = 'id'

    def get_object(self):
        return get_object_or_404(ExplanatoryNote, pk=self.kwargs['id'])

    def is_ajax_request(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'

    def update_note_section_status(self, section, status):
        expl_note = self.get_object()
        setattr(expl_note, section, status)
        expl_note.save()
        return expl_note

    def post(self, request, *args, **kwargs):
        if self.is_ajax_request():
            data = json.loads(self.request.body)
            section = data['section']
            status = int(data['approval_status'])
            expl_note = self.update_note_section_status(section, status)
            approval_status = getattr(expl_note, 'get_{}_display'.format(section))()
            info_status_css = expl_note.get_status_css(status)
            response = {
                'section': section,
                'approval_status': approval_status,
                'info_status_css': info_status_css
            }
            return JsonResponse(response)
        return redirect('home')