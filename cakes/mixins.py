from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Cake


class StaffOrOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        cake = self.get_object()
        user = self.request.user
        return user.is_staff or cake.owner_id == user.pk


class CakeOwnerMixin(LoginRequiredMixin, StaffOrOwnerMixin):
    """Combines authentication and ownership checks for cake edit/delete views.

    MRO ensures LoginRequiredMixin.dispatch() redirects unauthenticated users
    before UserPassesTestMixin ever calls test_func(), so anonymous users always
    land on the login page rather than a 403.
    """

    model = Cake
    slug_url_kwarg = 'slug'
