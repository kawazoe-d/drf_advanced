from django.urls import path, include

from .views import ProductFrontendAPI, ProductBackendAPIView

urlpatterns = [
    path('', include('common.urls')),
    path('products/frontend', ProductFrontendAPI.as_view()),
    path('products/backend', ProductBackendAPIView.as_view()),
]