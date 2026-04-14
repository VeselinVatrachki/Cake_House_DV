from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


from forms import ReviewForm


@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('cakes:gallery')
    else:
        form = ReviewForm()

    return render(request, 'review/add_review.html', {'form': form})