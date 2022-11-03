from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import *
from .forms import *

#class ListApplications(LoginRequiredMixin, ListView):
    # model = Application
    # context_object_name = 'applications'
    # template_name = 'applications/index.html'
    # login_url = '/login/'
    # paginate_by = 10

    # def get_queryset(self):
    #     queryset = Application.objects.all
    #     return queryset
class ListApplications(View):
    form_class = AllApplicationsForm
    template_name = 'applications/index_application.html'

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

class ShowApplication(LoginRequiredMixin, DetailView):
    model = Application
    context_object_name = 'application'
    pk_url_kwarg = 'id'
    template_name = 'applications/show_application.html'
    login_url = '/login/'

class NewApplication(View):
    form_class = NewApplicationForm
    template_name = 'applications/new_application.html'

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

class EditApplication(LoginRequiredMixin, UpdateView):
    form_class = UpdateApplicationForm
    template_name = 'applications/edit_application.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_object(self):
        id = self.kwargs.get('id')
        application = Application.objects.get(pk=id)
        return get_object_or_404(Application, id=application.id)

    def get_success_url(self):
        id = self.kwargs.get('id')
        return reverse_lazy('show_application', kwargs={'id': id})