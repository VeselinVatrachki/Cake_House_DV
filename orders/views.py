from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin

from accounts.forms import DeleteConfirmForm
from .forms import OrderForm, OrderLineFormSet
from .models import Order


# Create your views here.
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('lines__cake')


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'line_formset' not in context:
            if self.request.method == 'POST':
                context['line_formset'] = OrderLineFormSet(self.request.POST)
            else:
                context['line_formset'] = OrderLineFormSet()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = OrderLineFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.render_to_response(self.get_context_data(form=form, line_formset=formset))

    def form_valid(self, form, formset=None):
        if formset is None:
            formset = self.get_context_data()['line_formset']
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        formset.instance = self.object
        formset.save()
        messages.success(self.request, 'Order placed. We will confirm soon.')
        return HttpResponseRedirect(self.get_success_url())


class OrderDetailOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Order

    def test_func(self):
        order = self.get_object()
        return order.user_id == self.request.user.pk or self.request.user.is_staff

class OrderDetailView(OrderDetailOwnerMixin, DetailView):
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.select_related('user').prefetch_related('lines__cake')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderDeleteView(OrderDetailOwnerMixin, FormMixin, DetailView):
    model = Order
    form_class = DeleteConfirmForm
    template_name = 'orders/order_confirm_delete.html'
    context_object_name = 'order'
    success_url = reverse_lazy('orders:list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'Order cancelled.')
        self.object.delete()
        return HttpResponseRedirect(self.success_url)

