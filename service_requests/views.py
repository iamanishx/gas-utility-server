from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ServiceRequest, Customer
from .forms import ServiceRequestForm
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest
from .forms import CustomUserCreationForm





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
def support_dashboard(request):
    """
    Displays a dashboard for support representatives to manage service requests.
    """
    if not request.user.is_staff:
        # Only allow staff members to access this page
        return redirect('list_service_requests')

    # Get all service requests to display on the dashboard
    service_requests = ServiceRequest.objects.all().order_by('-created_at')
    
    return render(request, 'service_requests/support_dashboard.html', {
        'service_requests': service_requests
    })
@login_required
def my_account(request):
    """
    Display the details of the logged-in user's profile.
    """
    customer = request.user.customer  # Assuming the User is linked to a Customer profile
    return render(request, 'service_requests/my_account.html', {'customer': customer})
