from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.views.decorators.http import require_POST
from datetime import timedelta, datetime
from decimal import Decimal

from pets.models import Pet
from .models import HealthRecord, VaccinationRecord, MedicineRecord, WeightRecord, AllergyRecord
from .forms import HealthRecordForm, VaccinationForm, MedicineForm, WeightForm, AllergyForm
from .weight_analytics import (
    get_breed_target_range,
    calculate_weight_status,
    generate_realistic_weight_history_for_pet
)


def get_pet_weight_payload(pet, range_param='all'):
    """Helper to construct comprehensive chart data & statistics for a pet."""
    weights_qs = WeightRecord.objects.filter(pet=pet).order_by('recorded_date')

    # If no records exist, auto-generate realistic baseline
    if not weights_qs.exists():
        generate_realistic_weight_history_for_pet(pet)
        weights_qs = WeightRecord.objects.filter(pet=pet).order_by('recorded_date')

    today = timezone.now().date()
    cutoff_map = {
        '1m': today - timedelta(days=30),
        '3m': today - timedelta(days=90),
        '6m': today - timedelta(days=180),
        '1y': today - timedelta(days=365),
    }

    filtered_qs = weights_qs
    if range_param in cutoff_map:
        filtered_qs = weights_qs.filter(recorded_date__gte=cutoff_map[range_param])
        if not filtered_qs.exists():
            # Fallback to all if the filtered window has no points
            filtered_qs = weights_qs

    records = list(filtered_qs)
    labels = [w.recorded_date.strftime('%b %d, %Y') for w in records]
    data = [float(w.weight_kg) for w in records]
    notes = [w.notes or 'Weight check' for w in records]
    raw_dates = [w.recorded_date.strftime('%Y-%m-%d') for w in records]

    # Target breed benchmarks
    target_info = get_breed_target_range(pet.species, pet.breed, pet.weight)
    min_target = target_info['min_kg']
    max_target = target_info['max_kg']

    # Compute key statistical metrics
    current_w = data[-1] if data else float(pet.weight or 0.0)
    start_w = data[0] if data else current_w
    diff_kg = round(current_w - start_w, 2)
    diff_pct = round(((diff_kg / start_w) * 100), 1) if start_w > 0 else 0.0
    min_w = min(data) if data else current_w
    max_w = max(data) if data else current_w
    avg_w = round(sum(data) / len(data), 2) if data else current_w

    status_data = calculate_weight_status(current_w, min_target, max_target)

    return {
        'success': True,
        'pet_id': pet.id,
        'pet_name': pet.name,
        'species': pet.species,
        'breed': pet.breed,
        'labels': labels,
        'data': data,
        'notes': notes,
        'dates_raw': raw_dates,
        'ideal_min': min_target,
        'ideal_max': max_target,
        'ideal_label': target_info['label'],
        'ideal_short_label': target_info['short_label'],
        'stats': {
            'current_weight': current_w,
            'start_weight': start_w,
            'change_kg': diff_kg,
            'change_kg_display': f"{'+' if diff_kg > 0 else ''}{diff_kg} kg",
            'change_pct': diff_pct,
            'change_pct_display': f"{'+' if diff_pct > 0 else ''}{diff_pct}%",
            'min_weight': min_w,
            'max_weight': max_w,
            'avg_weight': avg_w,
            'status': status_data['status'],
            'short_status': status_data['short_status'],
            'status_color': status_data['color'],
            'badge_class': status_data['badge_class'],
            'icon': status_data['icon'],
            'total_entries': len(data),
            'selected_range': range_param,
        }
    }


@login_required
def health_dashboard(request, pet_id):
    """Unified health dashboard for a pet."""
    pet = get_object_or_404(Pet, pk=pet_id)
    if pet.owner != request.user and not request.user.is_staff:
        raise PermissionDenied

    vaccinations = VaccinationRecord.objects.filter(pet=pet).order_by('next_due_date')
    medical_records = HealthRecord.objects.filter(pet=pet).order_by('-record_date')
    medicines = MedicineRecord.objects.filter(pet=pet).order_by('-is_active', '-start_date')
    weight_history = WeightRecord.objects.filter(pet=pet).order_by('-recorded_date')
    allergies = AllergyRecord.objects.filter(pet=pet)

    today = timezone.now().date()
    urgent_vaccine_reminders = [v for v in vaccinations if v.reminder_status in ['OVERDUE', 'DUE_SOON']]
    user_pets = Pet.objects.filter(owner=request.user).order_by('id')

    # Weight breed analytics
    target_info = get_breed_target_range(pet.species, pet.breed, pet.weight)
    weight_status = calculate_weight_status(float(pet.weight or 0), target_info['min_kg'], target_info['max_kg'])

    context = {
        'pet': pet,
        'user_pets': user_pets,
        'vaccinations': vaccinations,
        'medical_records': medical_records,
        'medicines': medicines,
        'weight_history': weight_history,
        'allergies': allergies,
        'urgent_reminders': urgent_vaccine_reminders,
        'today': today,
        'target_info': target_info,
        'weight_status': weight_status,
    }

    return render(request, 'health/health_dashboard.html', context)


@login_required
def add_health_record(request, pet_id, record_type):
    """Add a specific health item (vaccination, condition, medicine, weight, allergy)."""
    pet = get_object_or_404(Pet, pk=pet_id, owner=request.user)

    form_map = {
        'vaccination': (VaccinationForm, 'Vaccination Entry'),
        'medical': (HealthRecordForm, 'Medical Condition / Checkup'),
        'medicine': (MedicineForm, 'Medication Prescription'),
        'weight': (WeightForm, 'Weight Log'),
        'allergy': (AllergyForm, 'Allergy Profile'),
    }

    if record_type not in form_map:
        return redirect('health:dashboard', pet_id=pet.pk)

    FormClass, title = form_map[record_type]

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.pet = pet
            record.save()
            
            # If weight was added, update pet current weight
            if record_type == 'weight':
                pet.weight = record.weight_kg
                pet.save(update_fields=['weight'])

            # Log to MongoDB NoSQL document collection
            try:
                from config.mongodb import log_vital_to_mongodb
                log_vital_to_mongodb(
                    pet_id=pet.id,
                    pet_name=pet.name,
                    weight_kg=getattr(record, 'weight_kg', None),
                    notes=f"{title}: {getattr(record, 'notes', '') or getattr(record, 'diagnosis', '') or getattr(record, 'vaccine_name', '')}",
                    recorded_by=request.user.username if request.user.is_authenticated else None
                )
            except Exception:
                pass

            messages.success(request, f"{title} added successfully for {pet.name}!")
            return redirect('health:dashboard', pet_id=pet.pk)
    else:
        form = FormClass()

    context = {
        'pet': pet,
        'form': form,
        'title': f"Add {title}",
        'record_type': record_type,
    }
    return render(request, 'health/record_form.html', context)


@login_required
def reminders_view(request):
    """Global vaccination and medicine reminders for all user pets."""
    user_pets = Pet.objects.filter(owner=request.user)
    today = timezone.now().date()
    upcoming_horizon = today + timedelta(days=30)

    vaccinations = VaccinationRecord.objects.filter(
        pet__in=user_pets,
        next_due_date__lte=upcoming_horizon
    ).select_related('pet').order_by('next_due_date')

    active_meds = MedicineRecord.objects.filter(
        pet__in=user_pets,
        is_active=True
    ).select_related('pet').order_by('end_date')

    overdue_count = sum(1 for v in vaccinations if v.reminder_status == 'OVERDUE')
    due_soon_count = sum(1 for v in vaccinations if v.reminder_status == 'DUE_SOON')

    context = {
        'vaccinations': vaccinations,
        'active_meds': active_meds,
        'overdue_count': overdue_count,
        'due_soon_count': due_soon_count,
        'today': today,
    }
    return render(request, 'health/reminders.html', context)


@login_required
def weight_data_api(request, pet_id):
    """JSON endpoint for dynamic Chart.js weight graph with range filtering and analytics."""
    pet = get_object_or_404(Pet, pk=pet_id)
    if pet.owner != request.user and not request.user.is_staff:
        raise PermissionDenied

    range_param = request.GET.get('range', 'all').lower()
    payload = get_pet_weight_payload(pet, range_param)
    return JsonResponse(payload)


@login_required
@require_POST
def add_weight_ajax(request, pet_id):
    """Real-time AJAX endpoint to log weight and return fresh chart dataset immediately."""
    pet = get_object_or_404(Pet, pk=pet_id)
    if pet.owner != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    weight_str = request.POST.get('weight_kg', '').strip()
    date_str = request.POST.get('recorded_date', '').strip()
    notes = request.POST.get('notes', 'Routine weigh-in').strip()

    if not weight_str:
        return JsonResponse({'success': False, 'error': 'Please enter a valid weight in kg.'}, status=400)

    try:
        weight_val = Decimal(weight_str)
        if weight_val <= 0:
            raise ValueError
    except Exception:
        return JsonResponse({'success': False, 'error': 'Invalid weight value. Must be a positive number.'}, status=400)

    if date_str:
        try:
            recorded_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            recorded_date = timezone.now().date()
    else:
        recorded_date = timezone.now().date()

    # Create weight log
    record = WeightRecord.objects.create(
        pet=pet,
        recorded_date=recorded_date,
        weight_kg=weight_val,
        notes=notes or 'Routine weigh-in'
    )

    # Update pet current weight if recorded date is today or latest
    latest_record = WeightRecord.objects.filter(pet=pet).order_by('-recorded_date', '-id').first()
    if latest_record and latest_record.id == record.id:
        pet.weight = weight_val
        pet.save(update_fields=['weight'])

    range_param = request.POST.get('range', 'all')
    updated_payload = get_pet_weight_payload(pet, range_param)
    updated_payload['message'] = f"Successfully logged {weight_val} kg for {pet.name}!"

    return JsonResponse(updated_payload)
