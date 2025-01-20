from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ServiceRequest, Customer
from .forms import ServiceRequestForm, SupportResponseForm
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from .forms import UserRegistrationForm
from django.contrib import messages




class SupportDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ServiceRequest
    template_name = 'service_requests/support_dashboard.html'
    context_object_name = 'service_requests'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        if self.request.user.is_staff:
            return ServiceRequest.objects.all()   
        
# Allow Support Staff to Respond to Service Requests
class ServiceRequestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ServiceRequest
    form_class = SupportResponseForm
    template_name = 'service_requests/update_service_request.html'
    success_url = reverse_lazy('support_dashboard')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)



class ServiceRequestCreateView(LoginRequiredMixin, CreateView):
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'service_requests/create_service_request.html'
    success_url = reverse_lazy('list_service_requests')

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        return super().form_valid(form)


class ServiceRequestListView(LoginRequiredMixin, ListView):
    model = ServiceRequest
    template_name = 'service_requests/list_service_requests.html'
    context_object_name = 'service_requests'

    def get_queryset(self):
        try:
            return ServiceRequest.objects.filter(customer=self.request.user.customer).order_by('-created_at')
        except AttributeError:
            return ServiceRequest.objects.none()


class ServiceRequestDetailView(LoginRequiredMixin, DetailView):
    model = ServiceRequest
    template_name = 'service_requests/service_request_detail.html'
    context_object_name = 'service_request'

    def get_queryset(self):
        return ServiceRequest.objects.filter(customer=self.request.user.customer)
    
class ServiceRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = ServiceRequest
    form_class = SupportResponseForm
    template_name = 'service_requests/update_service_request.html'
    context_object_name = 'service_request'

    def get_success_url(self):
        return reverse_lazy('list_service_requests')   

    def get_queryset(self):
        return ServiceRequest.objects.filter(customer=self.request.user.customer)   

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "A user with this username already exists.")
                return render(request, 'registration/signup.html', {'form': form})

            if User.objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists.")
                return render(request, 'registration/signup.html', {'form': form})
            
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  
            user.save()   
            print("Form Data:", form.cleaned_data)

 
            if not Customer.objects.filter(user=user).exists():
                 print("Phone Number:", form.cleaned_data.get('phone_number'))
                 print("Address:", form.cleaned_data.get('address'))
                 Customer.objects.create(
                    user=user,
                    phone_number=form.cleaned_data['phone_number'],
                    address=form.cleaned_data['address']
                )

            login(request, user)
            return redirect('list_service_requests')   
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
def my_account(request):
     
    customer = request.user.customer  
    return render(request, 'service_requests/my_account.html', {
        'user': request.user,
        'customer': customer,
    })