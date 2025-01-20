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


class SupportDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ServiceRequest
    template_name = 'service_requests/support_dashboard.html'
    context_object_name = 'service_requests'

    def test_func(self):
        # Only allow staff members to access this view
        return self.request.user.is_staff

    def get_queryset(self):
        # Get all service requests for staff review
        return ServiceRequest.objects.all().order_by('-created_at')


# Allow Support Staff to Respond to Service Requests
class ServiceRequestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ServiceRequest
    form_class = SupportResponseForm
    template_name = 'service_requests/update_service_request.html'
    success_url = reverse_lazy('support_dashboard')

    def test_func(self):
        # Restrict this view to staff members only
        return self.request.user.is_staff

    def form_valid(self, form):
        # Handle the response or status update
        form.instance.last_updated_by = self.request.user
        return super().form_valid(form)



class ServiceRequestCreateView(LoginRequiredMixin, CreateView):
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'service_requests/create_service_request.html'
    success_url = reverse_lazy('list_service_requests')

    def form_valid(self, form):
        # Link the request to the currently logged-in customer's account
        form.instance.customer = self.request.user.customer
        return super().form_valid(form)


class ServiceRequestListView(LoginRequiredMixin, ListView):
    model = ServiceRequest
    template_name = 'service_requests/list_service_requests.html'
    context_object_name = 'service_requests'

    def get_queryset(self):
        # Filter service requests based on the logged-in customer
        try:
            return ServiceRequest.objects.filter(customer=self.request.user.customer).order_by('-created_at')
        except AttributeError:
            return ServiceRequest.objects.none()


class ServiceRequestDetailView(LoginRequiredMixin, DetailView):
    model = ServiceRequest
    template_name = 'service_requests/service_request_detail.html'
    context_object_name = 'service_request'

    def get_queryset(self):
        # Restrict access to service requests owned by the logged-in customer
        return ServiceRequest.objects.filter(customer=self.request.user.customer)
    
class ServiceRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = ServiceRequest
    form_class = SupportResponseForm
    template_name = 'service_requests/update_service_request.html'
    context_object_name = 'service_request'

    def get_success_url(self):
        return reverse_lazy('service_requests:list_service_requests')  # Redirect after successful update

    def get_queryset(self):
        return ServiceRequest.objects.filter(customer=self.request.user.customer)  # Ensure only the current user's requests can be updated

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the User instance
            user = form.save()
            user.email = request.POST.get('email', '')  # Add the email to the user instance
            user.save()

            # Check if a Customer instance already exists for this User
            if not Customer.objects.filter(user=user).exists():
                # Create a new Customer instance
                Customer.objects.create(
                    user=user,
                    phone_number=request.POST.get('phone_number', ''),
                    address=request.POST.get('address', '')
                )

            # Log in the user after signup
            login(request, user)
            return redirect('list_service_requests')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

 
@login_required
def my_account(request):
    """
    Display the details of the logged-in user's profile.
    """
    customer = request.user.customer  # Assuming the User is linked to a Customer profile
    return render(request, 'service_requests/my_account.html', {'customer': customer})
