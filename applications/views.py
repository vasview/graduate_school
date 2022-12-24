from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib import messages

from main.models import *
from .models import *
from .forms import *
from postgraduates.models import Postgraduate, DissertationTopic, ExplanatoryNoteSectionType, ExplanatoryNoteSection
from main.views import AdministrationMenuView


class ListApplications(LoginRequiredMixin, AdministrationMenuView, ListView):
    model = Application
    context_object_name = 'applications'
    template_name = 'applications/index_application.html'
    login_url = '/login/'
    paginate_by = 10

    def is_group_member(self, group):
        user = self.request.user
        return user.groups.filter(name=group).exists()

    def get_queryset(self):
        return self.model.objects.all().order_by('-application_date', 'id')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, *args, **kwargs):
        if not self.is_group_member('Administration'):
            return redirect("home")
        return super(ListApplications, self).get(*args, **kwargs)


# class ShowApplication(LoginRequiredMixin, DetailView):
class ShowApplication(LoginRequiredMixin, AdministrationMenuView, DetailView):
    model = Application
    context_object_name = 'application'
    pk_url_kwarg = 'id'
    template_name = 'applications/show_application.html'
    login_url = '/login/'

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
            messages.success(request, "Ваш заявление успешно подано.")
            return redirect("home")
        else:
            return render(request, self.template_name, {'form': form})

# class EditApplication(LoginRequiredMixin, UpdateView):
class ChangeStatusApplication(AdministrationMenuView, View):
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

    def activate_user(self, user):
        pwd = ApplicationParameters.objects.get(code='new_default_pwd')
        user.is_active = True
        user.set_password(pwd.value)
        user.save()
        group, _created = Group.objects.get_or_create(name='Students')
        user.groups.add(group)
        return user

    def create_explanatory_note(serlf, student):
        expl_section_types = ExplanatoryNoteSectionType.objects.filter(active=True)
        for section in expl_section_types:
            ExplanatoryNoteSection.objects.create(
                postgraduate=student,
                title =section.name,
                sort = section.sort
            )
        return student.expl_note_sections

    def post(self, request, *args, **kwargs):
        application = self.get_object()
        status = request.POST.get('status')
        application.status = int(status)
        application.save(update_fields=['status'])
        if int(status) == 5:
            self.activate_user(application.user)
            student = self.create_student(application)
            DissertationTopic.objects.create(postgraduate=student)
            self.create_explanatory_note(student)

        # return redirect("applications")
        return redirect("show_application", id=application.id)

class SearchPostgraduateInApplication(AdministrationMenuView, View):
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
       