from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.ServiceRequestCreateView.as_view(), name='create_service_requests'),  # For submitting new requests
    path('', views.ServiceRequestListView.as_view(), name='list_service_requests'),          # For listing all requests
    path('<int:pk>/', views.ServiceRequestDetailView.as_view(), name='service_requests_detail'),  # For viewing a specific request
]
