from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView

from .forms import UserRegistrationForm, ProfileForm, UserDisplayNamesForm
from .models import User
from accounts.tasks import send_welcome_notification

class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('cakes:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)

        send_welcome_notification.delay(self.object.id)

        messages.success(self.request, 'Welcome to Cake House DV.')
        return response


class ProfileDashBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileForm(
            instance=self.request.user.profile,
            user=self.request.user,
            prefix='profile'
        )
        context['user_form'] = UserDisplayNamesForm(
            instance=self.request.user,
            prefix='user'
        )
        return context

    def post(self, request, *args, **kwargs):
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,
            user=request.user,
            prefix='profile'
        )
        user_form = UserDisplayNamesForm(
            request.POST,
            instance=request.user,
            prefix='user'
        )
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated successfully!')
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        context = self.get_context_data()
        context['profile_form'] = profile_form
        context['user_form'] = user_form
        return self.render_to_response(context)


class PublicProfileDetailView(DetailView):
    model = User
    template_name = 'accounts/profile_public.html'
    context_object_name = 'profile_user'

    def get_queryset(self):
        return User.objects.select_related('profile').prefetch_related('profile__favorite_tags')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('display_name', 'email')
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:dashboard')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Account details saved')
        return super().form_valid(form)





