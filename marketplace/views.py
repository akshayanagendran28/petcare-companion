from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import CaretakerProfile
from reviews.models import Review

@login_required
def caretaker_list(request):
    """Caretaker marketplace directory with multi-criteria search and filter."""
    queryset = CaretakerProfile.objects.select_related('user').all()

    # Search by name, bio, or location
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(user__address__icontains=q) |
            Q(services_offered__icontains=q) |
            Q(bio__icontains=q)
        )

    # Filter by Availability
    availability = request.GET.get('availability', '')
    if availability:
        queryset = queryset.filter(availability_status=availability)

    # Filter by Max Hourly Rate
    max_price = request.GET.get('max_price', '')
    if max_price:
        try:
            queryset = queryset.filter(hourly_rate__lte=float(max_price))
        except ValueError:
            pass

    # Filter by Minimum Rating
    min_rating = request.GET.get('min_rating', '')
    if min_rating:
        try:
            queryset = queryset.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    # Filter by Minimum Experience
    min_exp = request.GET.get('min_exp', '')
    if min_exp:
        try:
            queryset = queryset.filter(experience_years__gte=float(min_exp))
        except ValueError:
            pass

    # Filter by Service
    service = request.GET.get('service', '')
    if service:
        queryset = queryset.filter(services_offered__icontains=service)

    # Sorting
    sort_by = request.GET.get('sort', '-rating')
    if sort_by in ['-rating', 'hourly_rate', '-hourly_rate', '-experience_years']:
        queryset = queryset.order_by(sort_by)

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'q': q,
        'availability': availability,
        'max_price': max_price,
        'min_rating': min_rating,
        'min_exp': min_exp,
        'service': service,
        'sort_by': sort_by,
        'total_count': queryset.count(),
    }
    return render(request, 'marketplace/caretaker_list.html', context)


@login_required
def caretaker_detail(request, pk):
    """Detailed profile for a caretaker with booking CTA and verified reviews."""
    caretaker = get_object_or_404(CaretakerProfile.objects.select_related('user'), pk=pk)
    reviews = Review.objects.filter(caretaker=caretaker).select_related('reviewer', 'booking').order_by('-created_at')

    context = {
        'caretaker': caretaker,
        'reviews': reviews,
    }
    return render(request, 'marketplace/caretaker_detail.html', context)
