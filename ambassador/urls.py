from django.urls import path, include

from .views import ProductFrontendAPI, ProductBackendAPIView, LinkAPIView, StatsAPIView, RankingsAPIView

urlpatterns = [
    path('', include('common.urls')),
    path('products/frontend', ProductFrontendAPI.as_view()),
    path('products/backend', ProductBackendAPIView.as_view()),
    path('links', LinkAPIView.as_view()),
    path('stats', StatsAPIView.as_view()),
    path('rankings', RankingsAPIView.as_view()),
]