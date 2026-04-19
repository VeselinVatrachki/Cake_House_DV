from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from accounts.forms import DeleteConfirmForm
from review.forms import ReviewForm
from review.models import Review


class ReviewListView(ListView):
    model = Review
    template_name = 'review/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_form.html'
    success_url = reverse_lazy('review:list')

    def get_initial(self):
        return {'cake': self.kwargs['cake_id']}

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            messages.success(self.request, 'Thank you for your review!')
            return super().form_valid(form)
        except IntegrityError:
            messages.error(
                self.request,
                'You have already reviewed this cake. Edit your review instead.'
            )
        return self.form_invalid(form)


class ReviewOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Review

    def test_func(self):
        obj = self.get_object()
        return obj.user_id == self.request.user.pk or self.request.user.is_staff

class ReviewUpdateView(UpdateView):
    form_class = ReviewForm
    template_name = 'review/review_form.html'
    success_url = reverse_lazy('review:list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cake'].disabled = True
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Review updated.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.cake.get_absolute_url()


class ReviewDeleteView(DetailView):
    model = Review
    form_class = DeleteConfirmForm
    template_name = 'review/review_confirm_delete.html'
    success_url = reverse_lazy('review:list')
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

