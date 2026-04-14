from django.urls import path

from review import views

urlpatterns = [
    path('add/', views.add_review, name='add'),
]