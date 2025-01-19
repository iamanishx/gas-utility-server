from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ServiceRequest, Customer
from .forms import ServiceRequestForm


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
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically create a customer profile for the new user
            Customer.objects.create(user=user)
            login(request, user)  # Log in the user after successful signup
            return redirect('list_service_requests')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def support_dashboard(request):
    """
    Displays a dashboard for support representatives to manage service requests.
    """
    if not request.user.is_staff:
        return redirect('service_requests:list_service_requests')

    service_requests = ServiceRequest.objects.all().order_by('-created_at')
    return render(request, 'service_requests/support_dashboard.html', {'service_requests': service_requests})
