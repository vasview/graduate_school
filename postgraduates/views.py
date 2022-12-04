from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import *
from .forms import *
from main.views import StudentMenuView

class StudentWorkspace(LoginRequiredMixin, StudentMenuView, View):
    template_name = 'postgraduates/student_workspace.html'
    login_url = '/login/'

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
        context = self.get_context_data(request)
        # assert False
        return render(request, self.template_name, context)

class StudentCard(LoginRequiredMixin, DetailView):
    model = Postgraduate
    context_object_name = 'postgraduate'
    template_name = 'postgraduates/student_card.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class
    #     return render(request, self.template_name, {'form': form})


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
    model = ExplanatoryNote
    context_object_name = 'expl_note'
    template_name = 'postgraduates/show_explanatory_note.html'
    login_url = '/login/'

    def get_context_data(self, request, *args,**kwargs):
        context =  super().get_context_data(*args, **kwargs)
        user = request.user
        student = user.students.last()
        expl_note = student.explanatory_notes.last()
        context['expl_note'] = expl_note
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        student = user.students.last()
        expl_note = student.explanatory_notes.last()
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