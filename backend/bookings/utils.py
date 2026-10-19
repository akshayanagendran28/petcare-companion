from datetime import timedelta
from django.utils import timezone
from .models import Booking

# Caretakers accept strictly 1 booking per day
MAX_DAILY_PET_CAPACITY = 1
MAX_DAILY_BOOKING_CAPACITY = 1


def get_caretaker_daily_pet_count(caretaker, target_date, exclude_booking_id=None):
    """
    Returns the count of active bookings currently with the caretaker on target_date.
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
    return qs.count()


def get_caretaker_fully_booked_dates(caretaker, days_ahead=90, exclude_booking_id=None):
    """
    Returns a list of date strings ['YYYY-MM-DD', ...] within the next `days_ahead` days
    where the caretaker is already booked by another person (strictly 1 booking per day).
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

    bookings_list = list(active_bookings.values('id', 'start_date', 'end_date'))

    current = today
    while current <= end_window:
        is_booked = any(b['start_date'] <= current <= b['end_date'] for b in bookings_list)
        if is_booked:
            unavailable_dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)

    return unavailable_dates


def get_caretaker_next_available_date(caretaker, start_from=None, days_ahead=90):
    """
    Finds the earliest date on or after `start_from` (default: today) where the caretaker
    has no bookings.
    """
    if start_from is None:
        start_from = timezone.now().date()

    end_window = start_from + timedelta(days=days_ahead)
    active_bookings = list(Booking.objects.filter(
        caretaker=caretaker,
        status__in=['ACCEPTED', 'PENDING'],
        start_date__lte=end_window,
        end_date__gte=start_from
    ).values('id', 'start_date', 'end_date'))

    current = start_from
    while current <= end_window:
        is_booked = any(b['start_date'] <= current <= b['end_date'] for b in active_bookings)
        if not is_booked:
            return current
        current += timedelta(days=1)
    return current


def validate_caretaker_capacity_for_range(caretaker, start_date, end_date, exclude_booking_id=None):
    """
    Validates that every single day in [start_date, end_date] has strictly 0 existing bookings.
    Caretakers can take a maximum of 1 booking per day.
    Returns: (is_valid: bool, conflicting_date: date or None, next_available_date: date or None)
    """
    active_bookings = list(Booking.objects.filter(
        caretaker=caretaker,
        status__in=['ACCEPTED', 'PENDING'],
        start_date__lte=end_date,
        end_date__gte=start_date
    ).values('id', 'start_date', 'end_date'))

    if exclude_booking_id:
        active_bookings = [b for b in active_bookings if b.get('id') != exclude_booking_id]

    current = start_date
    while current <= end_date:
        is_booked = any(b['start_date'] <= current <= b['end_date'] for b in active_bookings)
        if is_booked:
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
    is_fully_booked = count >= MAX_DAILY_BOOKING_CAPACITY or caretaker.availability_status == 'UNAVAILABLE'

    if caretaker.availability_status == 'UNAVAILABLE':
        status_text = 'Unavailable'
        badge_class = 'bg-secondary'
    elif count >= MAX_DAILY_BOOKING_CAPACITY:
        status_text = 'Booked Today (1/1 Booking Limit Reached)'
        badge_class = 'bg-danger'
    else:
        status_text = 'Available Today (0/1 Booked)'
        badge_class = 'bg-success'

    next_avail = get_caretaker_next_available_date(caretaker, start_from=target_date)

    return {
        'count': count,
        'max_capacity': MAX_DAILY_BOOKING_CAPACITY,
        'is_fully_booked': is_fully_booked,
        'status_text': status_text,
        'badge_class': badge_class,
        'next_available_date': next_avail,
    }


def get_caretaker_calendar_grid(caretaker, days_ahead=35, exclude_booking_id=None):
    """
    Generates a list of day dictionaries for visual calendar display.
    Dates booked by other persons are marked is_booked=True (RED).
    """
    today = timezone.now().date()
    end_window = today + timedelta(days=days_ahead)

    active_bookings = Booking.objects.filter(
        caretaker=caretaker,
        status__in=['ACCEPTED', 'PENDING'],
        start_date__lte=end_window,
        end_date__gte=today
    )
    if exclude_booking_id:
        active_bookings = active_bookings.exclude(id=exclude_booking_id)

    bookings_list = list(active_bookings.values('id', 'start_date', 'end_date', 'owner__username'))

    calendar_days = []
    current = today
    standard_min_date = today + timedelta(days=2)

    while current <= end_window:
        matching = [
            b for b in bookings_list
            if b['start_date'] <= current <= b['end_date']
        ]
        is_booked = len(matching) > 0
        is_emergency_window = (current < standard_min_date)

        calendar_days.append({
            'date': current,
            'date_str': current.strftime('%Y-%m-%d'),
            'day': current.day,
            'weekday': current.strftime('%a'),
            'month': current.strftime('%b'),
            'is_booked': is_booked,
            'is_emergency_window': is_emergency_window,
            'is_today': current == today,
        })
        current += timedelta(days=1)

    return calendar_days
