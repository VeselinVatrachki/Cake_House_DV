from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from cakes.models import Cake
from orders.models import Order


class Command(BaseCommand):
    help = 'Create exam groups with distinct permissions (idempotent).'

    def handle(self, *args, **options):
        cake_ct = ContentType.objects.get_for_model(Cake)
        order_ct = ContentType.objects.get_for_model(Order)

        cake_perms = Permission.objects.filter(
            content_type=cake_ct,
            codename__in=['add_cake', 'change_cake', 'delete_cake', 'view_cake'],
        )
        order_perms = Permission.objects.filter(
            content_type=order_ct,
            # Order Staff can view and update statuses but cannot delete orders.
            codename__in=['change_order', 'view_order'],
        )

        # get_or_create makes this safe to run multiple times without duplicating groups.
        editors, _ = Group.objects.get_or_create(name='Cake Editors')
        editors.permissions.set(cake_perms)

        order_staff, _ = Group.objects.get_or_create(name='Order Staff')
        order_staff.permissions.set(order_perms)

        self.stdout.write(self.style.SUCCESS('Groups "Cake Editors" and "Order Staff" are configured.'))
