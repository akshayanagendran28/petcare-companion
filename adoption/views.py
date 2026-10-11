from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from .models import AdoptionListing
from .forms import AdoptionListingForm
from notifications.models import Notification

@login_required
def listing_list(request):
    """Catalog of pets available for Adoption and Sale."""
    queryset = AdoptionListing.objects.filter(status='ACTIVE')

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(pet_name__icontains=q) |
            Q(breed__icontains=q) |
            Q(location__icontains=q) |
            Q(description__icontains=q)
        )

    # Filter by Species
    species = request.GET.get('species', '')
    if species:
        queryset = queryset.filter(species__iexact=species)

    # Filter by Listing Type
    listing_type = request.GET.get('type', '')
    if listing_type in ['ADOPTION', 'SALE']:
        queryset = queryset.filter(listing_type=listing_type)

    # Filter by Gender
    gender = request.GET.get('gender', '')
    if gender:
        queryset = queryset.filter(gender=gender)

    # Filter by Max Price
    max_price = request.GET.get('max_price', '')
    if max_price:
        try:
            queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            pass

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'q': q,
        'species': species,
        'listing_type': listing_type,
        'gender': gender,
        'max_price': max_price,
        'total_count': queryset.count(),
    }
    return render(request, 'adoption/adoption_list.html', context)


def listing_detail(request, pk):
    """Detailed view for a specific adoption or sale listing."""
    listing = get_object_or_404(AdoptionListing.objects.select_related('owner'), pk=pk)
    related_listings = AdoptionListing.objects.filter(
        species=listing.species,
        status='ACTIVE'
    ).exclude(pk=listing.pk)[:3]

    context = {
        'listing': listing,
        'related_listings': related_listings,
    }
    return render(request, 'adoption/adoption_detail.html', context)


@login_required
def listing_create(request):
    """Publish a new pet adoption or sale listing."""
    if request.method == 'POST':
        form = AdoptionListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, f"Adoption listing for '{listing.pet_name}' is now live!")
            return redirect('adoption:listing_detail', pk=listing.pk)
    else:
        form = AdoptionListingForm(initial={
            'contact_phone': request.user.phone or '',
            'contact_email': request.user.email or '',
            'location': request.user.address or '',
        })

    return render(request, 'adoption/adoption_form.html', {'form': form, 'title': 'Create Pet Listing'})


@login_required
def listing_update_status(request, pk, new_status):
    """Owner can update the status of their listing."""
    listing = get_object_or_404(AdoptionListing, pk=pk)
    if listing.owner != request.user and not request.user.is_staff:
        raise PermissionDenied

    if new_status in ['ACTIVE', 'PENDING', 'ADOPTED', 'SOLD']:
        listing.status = new_status
        listing.save(update_fields=['status'])
        messages.success(request, f"Listing for '{listing.pet_name}' marked as {new_status.title()}.")

    return redirect('adoption:listing_detail', pk=listing.pk)
