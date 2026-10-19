from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import Pet
from .forms import PetForm

@login_required
def pet_list(request):
    """Lists all pets belonging to the logged-in user."""
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pets/pet_list.html', {'pets': pets})


@login_required
def pet_create(request):
    """Creates a new pet profile and generates QR Pet ID."""
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, f"Pet profile for '{pet.name}' created with unique QR ID!")
            return redirect('pets:pet_detail', pk=pet.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        # Pre-fill breed if coming from Breed Detection module
        initial_breed = request.GET.get('breed')
        initial_species = request.GET.get('species', 'Dog')
        initial = {}
        if initial_breed:
            initial['breed'] = initial_breed
            initial['species'] = initial_species
        form = PetForm(initial=initial)

    return render(request, 'pets/pet_form.html', {'form': form, 'title': 'Add New Pet'})


@login_required
def pet_detail(request, pk):
    """Displays detailed pet profile with QR code, health summary, and quick actions."""
    pet = get_object_or_404(Pet, pk=pk)
    if pet.owner != request.user and not request.user.is_staff:
        raise PermissionDenied

    from health.models import VaccinationRecord, HealthRecord, WeightRecord, MedicineRecord
    vaccinations = VaccinationRecord.objects.filter(pet=pet).order_by('-administered_date')[:4]
    medical_records = HealthRecord.objects.filter(pet=pet).order_by('-record_date')[:4]
    weight_history = WeightRecord.objects.filter(pet=pet).order_by('recorded_date')
    medicines = MedicineRecord.objects.filter(pet=pet, is_active=True)

    context = {
        'pet': pet,
        'vaccinations': vaccinations,
        'medical_records': medical_records,
        'weight_history': weight_history,
        'medicines': medicines,
    }
    return render(request, 'pets/pet_detail.html', context)



@login_required
def pet_update(request, pk):
    """Updates an existing pet profile."""
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{pet.name}' details updated successfully!")
            return redirect('pets:pet_detail', pk=pet.pk)
    else:
        form = PetForm(instance=pet)
    return render(request, 'pets/pet_form.html', {'form': form, 'title': f'Edit {pet.name}'})


@login_required
def pet_delete(request, pk):
    """Deletes a pet profile."""
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        name = pet.name
        pet.delete()
        messages.info(request, f"Pet '{name}' was deleted.")
        return redirect('pets:pet_list')
    return render(request, 'pets/pet_confirm_delete.html', {'pet': pet})


@login_required
def pet_id_card(request, pk):
    """Generates printable & downloadable digital Pet ID Card."""
    pet = get_object_or_404(Pet, pk=pk)
    if pet.owner != request.user and not request.user.is_staff:
        raise PermissionDenied
    return render(request, 'pets/pet_id_card.html', {'pet': pet})


def emergency_pet_profile(request, pk):
    """
    Public emergency profile accessible when a lost pet's QR code is scanned.
    No login required so first-responders / finders can contact owner immediately.
    """
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, 'pets/emergency_profile.html', {'pet': pet})
