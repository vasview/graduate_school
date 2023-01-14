from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse, Http404, HttpResponseRedirect
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
    """ update dissertation topic of a student """
    # model = DissertationTopic
    form_class = EditDissertationTopicForm
    template_name = 'postgraduates/edit_dissertation_topic.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_object(self):
        return get_object_or_404(DissertationTopic, pk=self.kwargs['id'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('postgraduates:student_workspace')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.postgraduate = self.request.user.students.last()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CreateExplanatoryNote(LoginRequiredMixin, StudentMenuView, CreateView):
    """ create a section in the explanatory note for student """
    form_class = NewExplanatorySectionForm
    template_name = 'postgraduates/edit_explanatory_note.html'
    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('postgraduates:show_explanatory_note')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.postgraduate = self.request.user.students.last()
        self.object.is_custom = 1
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ShowExplanatoryNote(LoginRequiredMixin, StudentMenuView, View):
    """ shows explanatory note for student """
    template_name = 'postgraduates/show_explanatory_note.html'
    login_url = '/login/'

    def get_context_data(self, request, *args,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        user = request.user
        student = user.students.last()
        expl_note_sections = student.expl_note_sections.all()
        context['expl_note_sections'] = expl_note_sections
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)


class EditExplanatorySection(LoginRequiredMixin, StudentMenuView, UpdateView):
    """ edit explanatory note  section for student """
    form_class = EditExplanatorySectionForm
    template_name = 'postgraduates/edit_explanatory_note.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self):
        return get_object_or_404(ExplanatoryNoteSection, pk=self.kwargs['id'])

    def get_success_url(self):
        return reverse_lazy('postgraduates:show_explanatory_note')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.postgraduate = self.request.user.students.last()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class DeleteExplanatorySection(LoginRequiredMixin, StudentMenuView, DeleteView):
    """ delete a section in the explanatory note """
    model = ExplanatoryNoteSection
    pk_url_kwarg = 'id'
    template_name = 'confirm_delete.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вы точно хотите удалить раздел объяснительной записки?'
        return context

    def get_object(self):
        return get_object_or_404(ExplanatoryNoteSection, pk=self.kwargs['id'])

    def delete(self, request, *args, **kwargs):
        expl_note_section = self.get_object()
        if expl_note_section.approval_status != 5:
            return super(DeleteExplanatorySection, self).delete(request, *args, **kwargs)
        else:
            raise Http404("Вы не можете удалить раздел")

    def get_success_url(self):
        return reverse_lazy('postgraduates:show_explanatory_note')


class SupervisorStudentCard(LoginRequiredMixin, SupervisorMenuView, DetailView):
    """ shows postgraduate card for supervisor """
    model = Postgraduate
    context_object_name = 'postgraduate'
    template_name = 'postgraduates/supervisor_student_card.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SupervisorStudentExplanatoryNote(LoginRequiredMixin, SupervisorMenuView, View):
    """ shows postgraduate explanatory note for supervisor """
    template_name = 'postgraduates/supervisor_student_explanatory_note.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_postgraduate(self):
        return get_object_or_404(Postgraduate, pk=self.kwargs['id'])

    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        postgraduate = self.get_postgraduate()
        context['postgraduate'] = postgraduate
        context['expl_note_sections'] = postgraduate.expl_note_sections.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)


class AjaxUApproveExplanatoryNote(LoginRequiredMixin, View):
    """ let supervisor to approve one section of an explanatory note """
    model = ExplanatoryNoteSection
    pk_url_kwarg = 'id'

    def get_object(self):
        return get_object_or_404(ExplanatoryNoteSection, pk=self.kwargs['id'])

    def is_ajax_request(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'

    def update_note_section_status(self, status):
        expl_note_section = self.get_object()
        expl_note_section.approval_status = status
        expl_note_section.save(update_fields=['approval_status'])
        return expl_note_section

    def post(self, request, *args, **kwargs):
        if self.is_ajax_request():
            data = json.loads(self.request.body)
            status = int(data['approval_status'])
            expl_note_section = self.update_note_section_status(status)
            approval_status = expl_note_section.get_approval_status_display()
            info_status_css = expl_note_section.get_status_css()
            response = {
                'section_id': expl_note_section.id,
                'approval_status': approval_status,
                'info_status_css': info_status_css
            }
            return JsonResponse(response)
        return redirect('home')