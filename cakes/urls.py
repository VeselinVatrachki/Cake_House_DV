from django.urls import path

from cakes import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('cake/<int:cake_id>/', views.cake_detail, name='cake_detail'),
    path('add-cake/', views.add_cake, name='add_cake'),
    path('signup/', views.signup, name='signup'),
]