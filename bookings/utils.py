from datetime import timedelta
from django.utils import timezone
from .models import Booking

MAX_DAILY_PET_CAPACITY = 2


def get_caretaker_daily_pet_count(caretaker, target_date, exclude_booking_id=None):
    """
    Returns the count of distinct pets currently booked with the caretaker on target_date.
    Only considers active/confirmed bookings ('ACCEPTED' and 'PENDING').
    """
    qs = Booking.objects.filter(
        caretaker=caretaker,
        status__in=['ACCEPTED', 'PENDING'],
        start_date__lte=target_date,
        end_date__gte=target_date
    )
    if exclude_booking_id:
        qs = qs.exclude(id=exclude_booking_id)
    return qs.values('pet').distinct().count()


def get_caretaker_fully_booked_dates(caretaker, days_ahead=90, exclude_booking_id=None):
    """
    Returns a list of date strings ['YYYY-MM-DD', ...] within the next `days_ahead` days
    where the caretaker already has MAX_DAILY_PET_CAPACITY (2) pets booked.
    """
    today = timezone.now().date()
    unavailable_dates = []

    end_window = today + timedelta(days=days_ahead)
    active_bookings = Booking.objects.filter(
        caretaker=caretaker,
        status__in=['ACCEPTED', 'PENDING'],
        start_date__lte=end_window,
        end_date__gte=today
    )
    if exclude_booking_id:
        active_bookings = active_bookings.exclude(id=exclude_booking_id)

    bookings_list = list(active_bookings.values('pet_id', 'start_date', 'end_date'))

    current = today
    while current <= end_window:
        pets_on_day = {
            b['pet_id'] for b in bookings_list
            if b['start_date'] <= current <= b['end_date']
        }
        if len(pets_on_day) >= MAX_DAILY_PET_CAPACITY:
            unavailable_dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)

    return unavailable_dates


def get_caretaker_next_available_date(caretaker, start_from=None, days_ahead=90):
    """
    Finds the earliest date on or after `start_from` (default: today) where the caretaker
    has fewer than MAX_DAILY_PET_CAPACITY pets.
    """
    if start_from is None:
        start_from = timezone.now().date()

    end_window = start_from + timedelta(days=days_ahead)
    active_bookings = list(Booking.objects.filter(
        caretaker=caretaker,
        status__in=['ACCEPTED', 'PENDING'],
        start_date__lte=end_window,
        end_date__gte=start_from
    ).values('pet_id', 'start_date', 'end_date'))

    current = start_from
    while current <= end_window:
        pets_on_day = {
            b['pet_id'] for b in active_bookings
            if b['start_date'] <= current <= b['end_date']
        }
        if len(pets_on_day) < MAX_DAILY_PET_CAPACITY:
            return current
        current += timedelta(days=1)
    return current


def validate_caretaker_capacity_for_range(caretaker, start_date, end_date, exclude_booking_id=None):
    """
    Validates that every single day in [start_date, end_date] has strictly < MAX_DAILY_PET_CAPACITY pets.
    Returns: (is_valid: bool, conflicting_date: date or None, next_available_date: date or None)
    """
    active_bookings = list(Booking.objects.filter(
        caretaker=caretaker,
        status__in=['ACCEPTED', 'PENDING'],
        start_date__lte=end_date,
        end_date__gte=start_date
    ).values('pet_id', 'start_date', 'end_date'))

    if exclude_booking_id:
        active_bookings = [b for b in active_bookings if b.get('id') != exclude_booking_id]

    current = start_date
    while current <= end_date:
        pets_on_day = {
            b['pet_id'] for b in active_bookings
            if b['start_date'] <= current <= b['end_date']
        }
        if len(pets_on_day) >= MAX_DAILY_PET_CAPACITY:
            next_avail = get_caretaker_next_available_date(caretaker, start_from=current)
            return False, current, next_avail
        current += timedelta(days=1)

    return True, None, None


def get_caretaker_capacity_summary(caretaker, target_date=None):
    """
    Returns a dictionary summarizing daily capacity for a caretaker for a given target_date (default today).
    """
    if target_date is None:
        target_date = timezone.now().date()
    count = get_caretaker_daily_pet_count(caretaker, target_date)
    is_fully_booked = count >= MAX_DAILY_PET_CAPACITY or caretaker.availability_status == 'UNAVAILABLE'

    if caretaker.availability_status == 'UNAVAILABLE':
        status_text = 'Unavailable'
        badge_class = 'bg-secondary'
    elif count >= MAX_DAILY_PET_CAPACITY:
        status_text = f'Fully Booked Today ({count}/{MAX_DAILY_PET_CAPACITY} Pets)'
        badge_class = 'bg-danger'
    elif count == 1:
        status_text = f'1 Slot Left Today (1/{MAX_DAILY_PET_CAPACITY} Pets)'
        badge_class = 'bg-warning text-dark'
    else:
        status_text = f'Available Today (0/{MAX_DAILY_PET_CAPACITY} Booked)'
        badge_class = 'bg-success'

    next_avail = get_caretaker_next_available_date(caretaker, start_from=target_date)

    return {
        'count': count,
        'max_capacity': MAX_DAILY_PET_CAPACITY,
        'is_fully_booked': is_fully_booked,
        'status_text': status_text,
        'badge_class': badge_class,
        'next_available_date': next_avail,
    }
