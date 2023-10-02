from django.urls import path

from .views import ProfileUpdateView, ProfileDetailView, MailRegisterView, MailLoginView

urlpatterns = [
    path('user/<str:slug>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('accounts/signup/', MailRegisterView.as_view(), name='signup'),
    path('account/login/', MailLoginView.as_view(), name='login'),
]