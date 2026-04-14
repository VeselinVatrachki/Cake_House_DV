from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CakeForm
from .models import Cake


def home(request):
    return render(request, 'cakes/home.html')


def about(request):
    return render(request, 'cakes/about.html')


def gallery(request):
    cake_list = Cake.objects.all()

    paginator = Paginator(cake_list, 6)  # Show 6 cakes per page
    page_number = request.GET.get('page')
    cakes = paginator.get_page(page_number)

    return render(request, 'cakes/gallery.html', {
        'cakes': cakes
    })


def cake_detail(request, cake_id):
    cake = get_object_or_404(Cake, pk=cake_id)
    reviews = cake.reviews.all()

    stats = reviews.aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )

    context = {
        'cake': cake,
        'reviews': reviews,
        'avg_rating': stats['avg_rating'],
        'total_reviews': stats['total_reviews'],
    }

    return render(request, 'cakes/cake_detail.html', context)


@login_required
@staff_member_required
def add_cake(request):
    form = CakeForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('cakes:gallery')

    return render(request, 'cakes/add_cake.html', {
        'form': form
    })


def signup(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('cakes:home')

    return render(request, 'registration/signup.html', {
        'form': form
    })