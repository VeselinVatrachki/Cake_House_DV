from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Cake


class StaffOrOwnerMixin(UserPassesTestMixin):
    def get_object(self, queryset=None):
        return super().get_object(queryset)

    def test_func(self):
        cake = self.get_object()
        user = self.request.user
        return user.is_staff or cake.owner_id == user.pk


class CakeOwnerMixin(LoginRequiredMixin, StaffOrOwnerMixin):
    model = Cake
    slug_url_kwarg = 'slug'
