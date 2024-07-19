from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EmployeeEmployerForm,JobSeekerForm,LoginForm
from django.views.generic import View, TemplateView, ListView, CreateView,FormView,DetailView
from . forms import ProfileForm,RegistrationForm,AddressForm,MessageForm
from .models import User,Message
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.
class HomeView(TemplateView):
    template_name = 'user/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filter out superusers and exclude the logged-in user
        users = User.objects.filter(is_superuser=False).exclude(pk=self.request.user.pk)
        
        context['users'] = users  # Pass users queryset to the template
        return context




class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('accounts:register2')

    def form_valid(self, form):
        self.request.session['registration_data'] = form.cleaned_data
        return super().form_valid(form)

class Register2View(CreateView):
    template_name = 'accounts/register2.html'
    form_class = ProfileForm
    model = User

    def form_valid(self, form):
        registration_data = self.request.session.get('registration_data')
        if registration_data:
            user = User.objects.create_user(
                username=registration_data['username'],
                email=registration_data['email'],
                password=registration_data['password1'],
                first_name=registration_data['first_name'],
                last_name=registration_data['last_name'],
            )
            user.dob = form.cleaned_data['dob']
            user.gender = form.cleaned_data['gender']
            user.phone = form.cleaned_data['phone']
            user.bio = form.cleaned_data['bio']
            user.qualification= form.cleaned_data['qualification']
            user.smoke = form.cleaned_data['smoke']
            user.drinking = form.cleaned_data['drinking']
            user.rel_status = form.cleaned_data['rel_status']
            if 'profile_pic' in form.cleaned_data:
                user.profile_pic = form.cleaned_data['profile_pic']
            if 'short_reel' in form.cleaned_data:
                user.short_reel = form.cleaned_data['short_reel']
            user.save()
            login(self.request, user)
            return redirect('accounts:address')
        return super().form_invalid(form)




class EmploymentDetailsView(LoginRequiredMixin, FormView):
    template_name = 'accounts/register3.html'
    form_class_employee = EmployeeEmployerForm
    form_class_job_seeker = JobSeekerForm
    success_url = reverse_lazy('accounts:register4')  # Replace with your success URL

    def get_form(self, form_class=None):
        if self.request.method == 'POST':
            employment_status = self.request.POST.get('employment-status')

            if employment_status == 'Employee':
                form_class = self.form_class_employee
            elif employment_status == 'Job Seeker':
                form_class = self.form_class_job_seeker
            else:
                form_class = None

        return form_class or self.form_class_employee

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_form'] = self.form_class_employee()
        context['job_seeker_form'] = self.form_class_job_seeker()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form()
        if form_class:
            form = form_class(request.POST)
            if form.is_valid():
                return self.form_valid(form)
        return self.form_invalid(form_class)

class Register4View(CreateView):
    template_name = "accounts/register4.html"
    success_url = reverse_lazy('accounts:signin')
    
    def get(self, request):
        return render(request, self.template_name)
    

class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('accounts:home')  # Replace 'home' with your actual home page URL name

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        # Store the username in the session
        self.request.session['username'] = user.username
        return super().form_valid(form)
    
class MyProfileView(LoginRequiredMixin, DetailView):
    template_name = "user/my_profile.html"
    model = User  # Assuming you are using Django's built-in User model
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')  # Retrieve user_id from URL
        return get_object_or_404(User, pk=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class CustomLogoutView(View): 
    def get(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()
        return redirect(reverse_lazy('accounts:signin'))
    

class ProfileView(DetailView):
    model = User  # Specify the model to use (User in this case)
    template_name = 'user/profiles.html'  # Your template name

    def get_object(self):
        # Get the user object based on the captured ID (pk)
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, pk=pk)

    # Optionally, you can override other methods or attributes as needed
    context_object_name = 'profile' 
   


class AddressCreateView(FormView):
    template_name = 'accounts/address.html'
    form_class = AddressForm
    success_url = reverse_lazy('accounts:register3')

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        return self.render_to_response(self.get_context_data(form=form))
    
class AddressCreateView(FormView):
    template_name = 'accounts/address.html'
    form_class = AddressForm
    success_url = reverse_lazy('accounts:register3')

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        return HttpResponseRedirect(self.get_success_url())
    
class SendMessageView(View):
    template_name = 'user/message.html'

    def get(self, request, id):
        recipient = get_object_or_404(User, id=id)
        received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
        sent_messages = Message.objects.filter(sender=request.user, recipient=recipient).order_by('-timestamp')
        form = MessageForm()
        context = {
            'form': form,
            'recipient': recipient,
            'received_messages': received_messages,
            'sent_messages': sent_messages,
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        recipient = get_object_or_404(User, id=id)
        received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
        sent_messages = Message.objects.filter(sender=request.user, recipient=recipient).order_by('-timestamp')
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            messages.success(request, 'Message sent successfully.')
            return redirect('accounts:send_message', id=id)  # Redirect to the send_message page with id
        context = {
            'form': form,
            'recipient': recipient,
            'received_messages': received_messages,
            'sent_messages': sent_messages,
        }
        return render(request, self.template_name, context)