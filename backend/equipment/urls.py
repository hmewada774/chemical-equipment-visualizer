from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, FileUploadView, LatestSummaryView, HistoryView, ReportPDFView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('summary/', LatestSummaryView.as_view(), name='summary'),
    path('history/', HistoryView.as_view(), name='history'),
    path('report/', ReportPDFView.as_view(), name='report'),
]
