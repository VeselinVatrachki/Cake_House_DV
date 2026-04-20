from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, RedirectView

from cakes.forms import CakeForm, GalleryFilterForm
from cakes.models import Cake
from accounts.forms import DeleteConfirmForm
from review.models import Review


class HomeView(TemplateView):
    template_name = 'cakes/home.html'


class AboutView(TemplateView):
    template_name = 'cakes/about.html'


class GalleryView(ListView):
    model = Cake
    template_name = 'cakes/gallery.html'
    context_object_name = 'cakes'
    paginate_by = 12

    def get_queryset(self):
        qs = Cake.objects.select_related('category', 'owner').prefetch_related('tags')
        form = GalleryFilterForm(self.request.GET or None)
        if form.is_valid():
            q = form.cleaned_data.get('q')
            cat = form.cleaned_data.get('category')
            tag = form.cleaned_data.get('tag')
            sort = form.cleaned_data.get('sort')
            if q:
                qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
            if cat:
                qs = qs.filter(category=cat)
            if tag:
                qs = qs.filter(tags=tag)
            if sort == 'price_asc':
                qs = qs.order_by('price', '-created_at')
            elif sort == 'price_desc':
                qs = qs.order_by('-price', '-created_at')
            elif sort == 'name':
                qs = qs.order_by('name')
            else:
                qs = qs.order_by('-created_at')
        else:
            qs = qs.order_by('-created_at')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = GalleryFilterForm(self.request.GET or None)
        return context


class CakeDetailView(DetailView):
    model = Cake
    template_name = 'cakes/cake_detail.html'
    context_object_name = 'cake'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Cake.objects.select_related('category', 'owner').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = (
            Review.objects.filter(cake=self.object)
            .select_related('user')
            .order_by('-created_at')
        )
        context['reviews'] = reviews
        context['avg_rating'] = reviews.aggregate(a=Avg('rating'))['a'] or 0
        return context


class CakeCreateView(LoginRequiredMixin,CreateView):
    model = Cake
    form_class = CakeForm
    template_name = 'cakes/cake_form.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.has_perm('cakes.add_cake')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Cake created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class CakeUpdateView(UpdateView):
    form_class = CakeForm
    template_name = 'cakes/cake_form.html'
    slug_url_kwarg = 'slug'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Cake updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class CakeDeleteView(DetailView):
    model = Cake
    form_class = DeleteConfirmForm
    template_name = 'cakes/cake_confirm_delete.html'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('cakes:gallery')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        messages.info(self.request, 'Cake removed.')
        self.object.delete()
        return HttpResponseRedirect(self.success_url)


class SignUpRedirectView(RedirectView):
    permanent = False
    pattern_name = 'accounts:register'