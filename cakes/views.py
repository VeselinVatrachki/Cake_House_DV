from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from cakes.forms import CakeForm
from cakes.models import Cake
from accounts.forms import DeleteConfirmForm


class HomeView(TemplateView):
    template_name = 'cakes/home.html'


class AboutView(TemplateView):
    template_name = 'cakes/about.html'


class GalleryView(ListView):
    model = Cake
    template_name = 'cakes/gallery.html'
    context_object_name = 'cakes'
    paginate_by = 12


class CakeDetailView(DetailView):
    model = Cake
    template_name = 'cakes/cake_detail.html'
    context_object_name = 'cake'
    slug_url_kwarg = 'slug'


class CakeCreateView(LoginRequiredMixin,CreateView):
    model = Cake
    form_class = CakeForm
    template_name = 'cakes/cake_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Cake created successfully!')
        return super().form_valid(form)


class CakeUpdateView(UpdateView):
    form_class = CakeForm
    template_name = 'cakes/cake_form.html'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        messages.success(self.request, 'Cake updated successfully!')
        return super().form_valid(form)


class CakeDeleteView(DetailView):
    model = Cake
    form_class = DeleteConfirmForm
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('cakes:gallery')
