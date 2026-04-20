from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormMixin

from accounts.forms import DeleteConfirmForm

from .forms import ReviewForm, ReviewSearchForm
from .models import Review


class ReviewListView(ListView):
    model = Review
    template_name = 'review/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 15

    def get_queryset(self):
        qs = Review.objects.select_related('cake', 'user').order_by('-created_at')
        form = ReviewSearchForm(self.request.GET or None)
        if form.is_valid():
            cake = form.cleaned_data.get('cake')
            min_r = form.cleaned_data.get('min_rating')
            if cake:
                qs = qs.filter(cake=cake)
            if min_r:
                qs = qs.filter(rating__gte=min_r)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = ReviewSearchForm(self.request.GET or None)
        return ctx


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_form.html'
    success_url = reverse_lazy('review:list')

    def get_initial(self):
        initial = super().get_initial()
        cake = self.request.GET.get('cake')
        if cake:
            initial['cake'] = cake
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            messages.success(self.request, 'Thank you for your review.')
            return super().form_valid(form)
        except IntegrityError:
            messages.error(
                self.request,
                'You already reviewed this cake. Edit your existing review instead.',
            )
            return self.form_invalid(form)


class ReviewOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Review

    def test_func(self):
        obj = self.get_object()
        return obj.user_id == self.request.user.pk or self.request.user.is_staff


class ReviewUpdateView(ReviewOwnerMixin, UpdateView):
    form_class = ReviewForm
    template_name = 'review/review_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cake'].disabled = True
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Review updated.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.cake.get_absolute_url()


class ReviewDeleteView(ReviewOwnerMixin, FormMixin, DetailView):
    model = Review
    form_class = DeleteConfirmForm
    template_name = 'review/review_confirm_delete.html'
    context_object_name = 'review'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        cake_url = self.object.cake.get_absolute_url()
        messages.info(self.request, 'Review deleted.')
        self.object.delete()
        return HttpResponseRedirect(cake_url)
