from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import *
from .forms import *

class StudentCard(View):
    form_class = StudendCardForm
    template_name = 'postgraduates/student_card.html'

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

class EditExplanatoryNote(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'postgraduates/edit_explanatory_note.html')

class ShowExplanatoryNote(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'postgraduates/show_explanatory_note.html')
