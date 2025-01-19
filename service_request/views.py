from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import ServiceRequest
from .forms import ServiceRequestForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ServiceRequestCreateView(LoginRequiredMixin, CreateView):
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'service_requests/create_service_request.html'
    success_url = reverse_lazy('list_service_requests')  # Redirect to the request list upon success

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer  # Link the request to the logged-in customer
        return super().form_valid(form)

class ServiceRequestListView(LoginRequiredMixin, ListView):
    model = ServiceRequest
    template_name = 'service_requests/list_service_requests.html'
    context_object_name = 'service_requests'

    def get_queryset(self):
        return ServiceRequest.objects.filter(customer=self.request.user.customer).order_by('-created_at')

class ServiceRequestDetailView(LoginRequiredMixin, DetailView):
    model = ServiceRequest
    template_name = 'service_requests/service_request_detail.html'
    context_object_name = 'service_request'

    def get_queryset(self):
        # Limit access to requests belonging to the logged-in customer
        return ServiceRequest.objects.filter(customer=self.request.user.customer)
