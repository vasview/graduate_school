from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import *
from .forms import *

 ##TODO need to create a profile page and root
menu = [{'title': 'Аспирантура', 'url_name': 'postgraduates:student_workspace'},
        {'title': 'Объяснительная записка', 'url_name': 'postgraduates:show_explanatory_note'},
        {'title': 'Мои планы', 'url_name': 'student_study_plans:index'},
        {'title': 'Мой профиль', 'url_name': 'postgraduates:student_workspace'},    
        {'title': 'Выход', 'url_name': 'logout'}
]

class StudentWorkspace(LoginRequiredMixin, View):
    template_name = 'postgraduates/student_workspace.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        user = request.user
        student = user.students.last()
        topic = student.topics.last()
        context = {
            'user': user, 
            'student': student, 
            'topic': topic,
            'menu': menu
        }
        # assert False
        return render(request, self.template_name, context)

class StudentCard(LoginRequiredMixin, View):
    form_class = StudendCardForm
    template_name = 'postgraduates/student_card.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,  request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(request, self.template_name, {'form': form})

class EditDissertationTopic(LoginRequiredMixin, UpdateView):
    model = DissertationTopic
    form_class = EditDissertationTopic
    template_name = 'postgraduates/edit_dissertation_topic.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def get_success_url(self):
        # id = self.object.postgraduate.id
        return reverse_lazy('postgraduates:student_workspace')

class ShowExplanatoryNote(LoginRequiredMixin, View):
    model = ExplanatoryNote
    context_object_name = 'expl_note'
    template_name = 'postgraduates/show_explanatory_note.html'
    login_url = '/login/'

    def get(self,request,*args, **kwargs):
        user = request.user
        student = user.students.last()
        expl_note = student.explanatory_notes.last()
        context = {
            'menu': menu,
            'expl_note': expl_note
        }
        return render(request, self.template_name, context)

class EditExplanatoryNote(LoginRequiredMixin, UpdateView):
    model = ExplanatoryNote
    form_class = EditExplanatoryNote
    template_name = 'postgraduates/edit_explanatory_note.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def get_success_url(self):
        # id = self.object.postgraduate.id
        return reverse_lazy('postgraduates:show_explanatory_note')