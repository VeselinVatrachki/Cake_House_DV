from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .forms import ProfileForm, UserDisplayNameForm, UserRegistrationForm
from .models import Profile, User


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('cakes:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Welcome to Cake House DV.')
        return response


class ProfileDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        ctx['profile_form'] = ProfileForm(
            instance=profile,
            user=self.request.user,
            prefix='p',
        )
        ctx['user_form'] = UserDisplayNameForm(instance=self.request.user, prefix='u')
        return ctx

    def post(self, request, *args, **kwargs):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=request.user,
            prefix='p',
        )
        user_form = UserDisplayNameForm(request.POST, instance=request.user, prefix='u')
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated.')
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        ctx = self.get_context_data()
        ctx['profile_form'] = profile_form
        ctx['user_form'] = user_form
        return self.render_to_response(ctx)


class PublicProfileDetailView(DetailView):
    model = User
    template_name = 'accounts/profile_public.html'
    context_object_name = 'profile_user'

    def get_queryset(self):
        return User.objects.select_related('profile').prefetch_related('profile__favorite_tags')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Alternative single-page edit using UpdateView (dashboard uses TemplateView)."""

    model = User
    fields = ('display_name', 'email')
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:dashboard')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Account details saved.')
        return super().form_valid(form)
