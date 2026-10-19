import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from .models import LostPetReport, LostPetSighting
from .forms import LostPetReportForm, LostPetSightingForm
from .document_verifier import verify_police_document_ml
from notifications.models import Notification


def perform_ml_document_verification(report):
    """Helper to execute ML police document inspection and update model."""
    if not report.police_document:
        return None

    meta = {
        'pet_name': report.pet_name,
        'species': report.species,
        'breed': report.breed,
        'contact_name': report.contact_name,
        'police_csr_number': report.police_csr_number,
        'police_station_name': report.police_station_name,
        'date_lost': report.date_lost
    }

    res = verify_police_document_ml(report.police_document, meta)
    report.police_verified_by_ai = res['is_valid']
    report.police_verification_confidence = Decimal(str(res['confidence']))
    report.police_verification_details = json.dumps(res['breakdown'])
    report.police_verified_at = timezone.now()

    if res['is_valid']:
        report.police_complaint_status = 'FILED'
    elif report.police_complaint_status == 'NOT_FILED':
        report.police_complaint_status = 'UNDER_REVIEW'

    report.save()
    return res


@login_required
def lost_pet_list(request):
    """Public board of reported lost & found pets with real-time filters and search."""
    queryset = LostPetReport.objects.select_related('reporter').prefetch_related('sightings').all()

    # Search filter
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(pet_name__icontains=q) |
            Q(breed__icontains=q) |
            Q(last_seen_location__icontains=q) |
            Q(description__icontains=q) |
            Q(distinctive_marks__icontains=q) |
            Q(how_lost__icontains=q) |
            Q(police_csr_number__icontains=q) |
            Q(color_pattern__icontains=q)
        )

    # Status filter
    status = request.GET.get('status', 'ALL')
    if status and status != 'ALL':
        queryset = queryset.filter(status=status)

    # Species filter
    species = request.GET.get('species', '')
    if species:
        queryset = queryset.filter(species__iexact=species)

    # Police status filter
    police_status = request.GET.get('police_status', '')
    if police_status:
        if police_status == 'AI_VERIFIED':
            queryset = queryset.filter(police_verified_by_ai=True)
        else:
            queryset = queryset.filter(police_complaint_status=police_status)

    # Reward only filter
    has_reward = request.GET.get('has_reward', '')
    if has_reward == '1':
        queryset = queryset.filter(reward_amount__gt=0)

    all_reports = LostPetReport.objects.all()
    context = {
        'reports': queryset,
        'q': q,
        'status': status,
        'species': species,
        'police_status': police_status,
        'has_reward': has_reward,
        'total_all_count': all_reports.count(),
        'total_lost_count': all_reports.filter(status='LOST').count(),
        'total_reunited_count': all_reports.filter(status='REUNITED').count(),
        'total_found_count': all_reports.filter(status='FOUND').count(),
        'total_police_filed_count': all_reports.filter(police_complaint_status='FILED').count(),
        'total_ai_verified_count': all_reports.filter(police_verified_by_ai=True).count(),
        'total_reward_count': all_reports.filter(reward_amount__gt=0).count(),
    }
    return render(request, 'lostfound/lostfound_list.html', context)


@login_required
def report_lost_pet(request):
    """File a new lost or found pet report with complete birthmarks and police details."""
    if request.method == 'POST':
        form = LostPetReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            if not report.contact_name:
                report.contact_name = request.user.get_full_name() or request.user.username
            if not report.contact_number:
                report.contact_number = getattr(request.user, 'phone', '') or ''
            report.save()

            # Run ML Police Document Inspection if uploaded
            if report.police_document:
                ml_res = perform_ml_document_verification(report)
                if ml_res and ml_res['is_valid']:
                    messages.success(request, f"🛡️ ML Document Inspector: Police CSR Copy verified ({ml_res['confidence']}% confidence)! Official Police CSR badge awarded.")
                elif ml_res:
                    messages.warning(request, f"⚠️ ML Document Inspector: Document uploaded, but confidence was {ml_res['confidence']}%. Status marked as Under Review.")

            messages.success(request, f"Lost Pet Report for '{report.pet_name}' has been successfully published to the community!")
            return redirect('lostfound:detail', pk=report.pk)
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        initial_data = {
            'contact_name': request.user.get_full_name() or request.user.username,
            'contact_number': getattr(request.user, 'phone', '') or '',
            'date_lost': timezone.now().date(),
            'status': 'LOST',
            'police_complaint_status': 'NOT_FILED'
        }
        form = LostPetReportForm(initial=initial_data)

    return render(request, 'lostfound/report_lost.html', {
        'form': form,
        'title': 'Report Lost Pet / Create Alert',
        'is_edit': False
    })


@login_required
def edit_lost_pet(request, pk):
    """Edit an existing lost pet report (update birthmarks, police CSR, reward, status)."""
    report = get_object_or_404(LostPetReport, pk=pk)
    if report.reporter != request.user and not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        old_doc = report.police_document
        form = LostPetReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            saved_report = form.save()

            # Check if document was newly uploaded or changed
            if saved_report.police_document and (not old_doc or saved_report.police_document != old_doc or 'police_document' in request.FILES):
                ml_res = perform_ml_document_verification(saved_report)
                if ml_res and ml_res['is_valid']:
                    messages.success(request, f"🛡️ ML Document Inspector: Police CSR Document verified ({ml_res['confidence']}% confidence)!")
                elif ml_res:
                    messages.warning(request, f"⚠️ ML Document Inspector: Verification score is {ml_res['confidence']}%. Status marked for review.")

            messages.success(request, f"Report for '{saved_report.pet_name}' updated successfully!")
            return redirect('lostfound:detail', pk=saved_report.pk)
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = LostPetReportForm(instance=report)

    return render(request, 'lostfound/report_lost.html', {
        'form': form,
        'title': f'Edit Alert: {report.pet_name}',
        'is_edit': True,
        'report': report
    })


def lost_pet_detail(request, pk):
    """Detailed view of a lost pet report + sightings + ML verification dossier."""
    report = get_object_or_404(LostPetReport.objects.select_related('reporter'), pk=pk)
    sightings = LostPetSighting.objects.filter(lost_pet=report).order_by('-sighting_date', '-created_at')
    sighting_form = LostPetSightingForm(initial={'sighting_date': timezone.now().date()})

    breakdown = {}
    if report.police_verification_details:
        try:
            breakdown = json.loads(report.police_verification_details)
        except Exception:
            breakdown = {}

    context = {
        'report': report,
        'sightings': sightings,
        'sighting_form': sighting_form,
        'verification_breakdown': breakdown,
    }
    return render(request, 'lostfound/lostfound_detail.html', context)


@login_required
@require_POST
def verify_police_document_ajax(request, pk):
    """Real-time AJAX endpoint to test or re-verify uploaded Police Document using ML."""
    report = get_object_or_404(LostPetReport, pk=pk)
    if report.reporter != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    if 'police_document' in request.FILES:
        report.police_document = request.FILES['police_document']
        report.save(update_fields=['police_document'])

    if not report.police_document:
        return JsonResponse({'success': False, 'error': 'No police document uploaded to verify.'}, status=400)

    ml_res = perform_ml_document_verification(report)
    if not ml_res:
        return JsonResponse({'success': False, 'error': 'Could not process document.'}, status=400)

    return JsonResponse({
        'success': True,
        'is_valid': ml_res['is_valid'],
        'confidence': ml_res['confidence'],
        'status': ml_res['status'],
        'summary': ml_res['summary'],
        'breakdown': ml_res['breakdown'],
        'police_csr_number': report.police_csr_number,
        'police_station_name': report.police_station_name,
        'police_status': report.police_complaint_status,
        'document_url': report.police_document.url if report.police_document else None
    })


def submit_sighting(request, pk):
    """Submit a community sighting for a lost pet."""
    report = get_object_or_404(LostPetReport, pk=pk)

    if request.method == 'POST':
        form = LostPetSightingForm(request.POST, request.FILES)
        if form.is_valid():
            sighting = form.save(commit=False)
            sighting.lost_pet = report
            sighting.save()

            # If report was LOST, optionally mark as SIGHTING_REPORTED
            if report.status == 'LOST':
                report.status = 'SIGHTING_REPORTED'
                report.save(update_fields=['status'])

            # Create immediate notification for the owner
            Notification.objects.create(
                user=report.reporter,
                title=f"🚨 New Sighting Reported for {report.pet_name}!",
                message=f"{sighting.reporter_name} reported spotting {report.pet_name} at {sighting.sighting_location} ({sighting.sighting_time or 'Recent'}).",
                notification_type='LOST_FOUND',
                link=f'/lostfound/{report.id}/'
            )

            messages.success(request, f"Thank you! Your sighting report has been sent directly to {report.pet_name}'s owner.")
            return redirect('lostfound:detail', pk=report.pk)
        else:
            messages.error(request, "Please check the sighting details and try again.")

    return redirect('lostfound:detail', pk=report.pk)


@login_required
def mark_reunited(request, pk):
    """Owner marks the pet as reunited with resolution details."""
    report = get_object_or_404(LostPetReport, pk=pk)
    if report.reporter != request.user and not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        reunion_notes = request.POST.get('reunited_details', '').strip()
        reunion_date_str = request.POST.get('reunited_date', '')
        if reunion_date_str:
            try:
                from datetime import datetime
                report.reunited_date = datetime.strptime(reunion_date_str, '%Y-%m-%d').date()
            except ValueError:
                report.reunited_date = timezone.now().date()
        else:
            report.reunited_date = timezone.now().date()

        report.status = 'REUNITED'
        if reunion_notes:
            report.reunited_details = reunion_notes
        report.save()
        messages.success(request, f"Hooray! 🎉 {report.pet_name} has been marked as safely reunited with family!")
    else:
        report.status = 'REUNITED'
        report.reunited_date = timezone.now().date()
        if not report.reunited_details:
            report.reunited_details = f"Safely recovered and reunited with family on {timezone.now().date().strftime('%b %d, %Y')}!"
        report.save()
        messages.success(request, f"Hooray! 🎉 {report.pet_name} has been marked as safely reunited!")

    return redirect('lostfound:detail', pk=report.pk)
