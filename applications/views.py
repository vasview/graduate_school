from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q

from main.models import *
from .models import *
from .forms import *
from postgraduates.models import Postgraduate, DissertationTopic, ExplanatoryNote

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
    model = Application
    template_name = 'applications/index_application.html'
    login_url = '/login/'
    # paginate_by = 10

    def get(self, request, *args, **kwargs):
        applications = self.model.objects.all().order_by('-application_date', 'id')
        return render(request, self.template_name, {'applications': applications})

# class ShowApplication(LoginRequiredMixin, DetailView):
class ShowApplication(DetailView):
    model = Application
    context_object_name = 'application'
    pk_url_kwarg = 'id'
    template_name = 'applications/show_application.html'
#     login_url = '/login/'

class NewApplication(View):
    form_class = NewApplicationForm
    template_name = 'applications/new_application.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,  request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            return render(request, self.template_name, {'form': form})

# class EditApplication(LoginRequiredMixin, UpdateView):
class ChangeStatusApplication(View):
    # template_name = 'applications/edit_application.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Application, id=id)

### TODO need to sort it out the set_success_url is not working
    # def get_success_url(self):
    #     apl_id = self.kwargs.get('id')
    #     return redirect('show_application', id=apl_id)
    
    def create_student(self,application):
        student = Postgraduate(student=application.user, specialty=application.specialty,
                    form_of_study=application.form_of_study, number_of_years=application.number_of_years,
                    start_date=application.approval_date)
        student.save()
        return student

    def post(self, request, *args, **kwargs):
        application = self.get_object()
        status = request.POST.get('status')
        application.status = int(status)
        application.save(update_fields=['status'])
        if int(status) == 5:
            pwd = ApplicationParameters.objects.get(code='new_default_pwd')
            application.user.is_active = True
            application.user.set_password(pwd.value)
            application.user.save()
            student = self.create_student(application)
            DissertationTopic.objects.create(postgraduate=student)
            ExplanatoryNote.objects.create(postgraduate=student)
        
        # return redirect("applications")
        return redirect("show_application", id=application.id)

class SearchPostgraduateInApplication(View):
    template_name = 'applications/index_application.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if ('query' in request.GET) and request.GET['query'].strip():
            query_string=request.GET['query'].strip()
            students = User.objects.filter(
                    Q(first_name__icontains=query_string) | Q(last_name__icontains=query_string)
            ) 
            # .filter(contact_type='STD')
            applications = Application.objects.filter(user__in=students).order_by('-application_date', 'id')
            return render(request, self.template_name, {'applications': applications})
        return redirect('applications')
       