from django.urls import path

from review import views

app_name = 'review'

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='list'),
    path('add/', views.ReviewCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='delete'),
]