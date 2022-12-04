from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q

from postgraduates.models import Postgraduate
from .models import *
from .forms import *

class ListSupervisorStudents(ListView):
    # form_class = SupervisorStudentsForm
    template_name = 'faculties/supervisor_page.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        postgraduates = Postgraduate.objects.all()
        return render(request, self.template_name, {'postgraduates': postgraduates})

class SearchSupervisorStudents(View):
    template_name = 'faculties/supervisor_page.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if ('query' in request.GET) and request.GET['query'].strip():
            query_string=request.GET['query'].strip()
            students = User.objects.filter(
                    Q(first_name__icontains=query_string) | Q(last_name__icontains=query_string)
            ) 
            # .filter(contact_type='STD')
            postgraduates = Postgraduate.objects.filter(student__in=students)
            return render(request, self.template_name, {'postgraduates': postgraduates})
        return redirect('supervisor_students')
