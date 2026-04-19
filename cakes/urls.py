from django.urls import path

from cakes import views

app_name = 'cakes'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('cake/add/', views.CakeCreateView.as_view(), name='add'),
    path('cake/<slug:slug>/', views.CakeDetailView.as_view(), name='detail'),
    path('cake/<slug:slug>/edit/', views.CakeUpdateView.as_view(), name='edit'),
    path('cake/<slug:slug>/delete/', views.CakeDeleteView.as_view(), name='delete'),
]