from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .forms import ProfileForm, UserDisplayNameForm, UserRegistrationForm
from .models import Profile, User


class RegisterView(CreateView):
    """
    Handles user registration.

    Creates a new User and logs them in immediately after successful signup.
    """
    
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('cakes:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in immediately after registration so they land on the
        # home page as an authenticated user rather than hitting a login wall.
        login(self.request, self.object)
        messages.success(self.request, 'Welcome to Cake House DV.')
        return response


class ProfileDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard that edits two separate models (User + Profile) at once.

    TemplateView is used instead of UpdateView/FormView because there is no
    single model form — the page submits a UserDisplayNameForm and a ProfileForm
    together via prefixes, and both must be valid before either is saved.
    """

    template_name = 'accounts/profile_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ensure the user always has a profile (fallback for old accounts)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        context['profile_form'] = ProfileForm(
            instance=profile,
            user=self.request.user,
            prefix='p',
        )
        context['user_form'] = UserDisplayNameForm(instance=self.request.user, prefix='u')
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles form submission for both User and Profile forms.
        """
        profile, _ = Profile.objects.get_or_create(user=request.user)
        
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=request.user,
            prefix='p',
        )
        user_form = UserDisplayNameForm(request.POST, instance=request.user, prefix='u')
        # Validate both forms before saving anything
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated.')
            return HttpResponseRedirect(reverse('accounts:dashboard'))
        # Re-render with the submitted (invalid) forms so errors are shown.
        context = self.get_context_data()
        context['profile_form'] = profile_form
        context['user_form'] = user_form
        return self.render_to_response(context)


class PublicProfileDetailView(DetailView):
    model = User
    template_name = 'accounts/profile_public.html'
    context_object_name = 'profile_user'

    def get_queryset(self):
        # Prefetch favorite_tags through the profile to avoid N+1 on the public page.
        return User.objects.select_related('profile').prefetch_related('profile__favorite_tags')


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Simpler alternative to edit user account details.

    Only updates User fields (not Profile).
    """

    model = User
    fields = ('display_name', 'email')
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:dashboard')

    def get_object(self, queryset=None):
        # Always edit the currently logged-in user; ignore the URL pk.
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Account details saved.')
        return super().form_valid(form)
