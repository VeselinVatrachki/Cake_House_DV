from django.urls import path

from accounts import views

# Namespace for this app (used in reverse() and templates)
app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('me/', views.ProfileDashboardView.as_view(), name='dashboard'),
    path('me/edit/', views.ProfileEditView.as_view(), name='edit'),
    path('user/<int:pk>/', views.PublicProfileDetailView.as_view(), name='public_profile')
]
