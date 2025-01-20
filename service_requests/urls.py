'''
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('service-requests/new/', views.ServiceRequestCreateView.as_view(), name='create_service_request'),
    path('service-requests/', views.ServiceRequestListView.as_view(), name='list_service_requests'),
    path('service-requests/<int:pk>/', views.ServiceRequestDetailView.as_view(), name='service_request_detail'),
]
'''
from django.urls import path
from . import views
from django.shortcuts import redirect  # Import redirect function
from django.contrib.auth.views import LogoutView


# app_name = 'service_requests'

urlpatterns = [
    path('', lambda request: redirect('list_service_requests')),  # Redirect root URL to service-requests
    path('new/', views.ServiceRequestCreateView.as_view(), name='create_service_request'),
    path('service-requests/', views.ServiceRequestListView.as_view(), name='list_service_requests'),
    path('<int:pk>/', views.ServiceRequestDetailView.as_view(), name='service_request_detail'),
    path('signup/', views.signup, name='signup'),  
    path('support-dashboard/', views.support_dashboard, name='support_dashboard'),  # Support dashboard URL
    path('my-account/', views.my_account, name='my_account'),  # My Account page
    
    ]

