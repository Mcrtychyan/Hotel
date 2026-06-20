from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Reservation, Payment
from .forms import ReservationForm, PaymentForm
from rooms.models import Room
from datetime import date


@login_required
def create_reservation(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)

    # Проверяем, доступен ли номер для бронирования
    if room.status != 'available':
        messages.error(request, 'Этот номер временно недоступен для бронирования')
        return redirect('rooms:detail', slug=room_slug)

    if request.method == 'POST':
        form = ReservationForm(request.POST, room=room)
        if form.is_valid():
            # Создаём бронирование
            reservation = form.save(commit=False)
            reservation.client = request.user
            reservation.room = room
            reservation.reservation_status = 'pending'
            reservation.save()

            messages.success(request, f'Номер {room.room_number} успешно забронирован!')
            return redirect('reservations:payment', reservation_id=reservation.id)
    else:
        form = ReservationForm(room=room)

    # Подсчитываем общую стоимость
    total_days = 0
    total_price = 0
    if request.method == 'GET' and form.is_bound:
        check_in = form.cleaned_data.get('check_in_date')
        departure = form.cleaned_data.get('departure_date')
        if check_in and departure:
            total_days = (departure - check_in).days
            total_price = total_days * room.price_per_day

    context = {
        'room': room,
        'form': form,
        'total_days': total_days,
        'total_price': total_price,
    }
    return render(request, 'reservations/create_reservation.html', context)


@login_required
def payment_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, client=request.user)

    if reservation.reservation_status == 'confirmed':
        messages.warning(request, 'Это бронирование уже оплачено')
        return redirect('clients:profile')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Создаём платёж
            payment = form.save(commit=False)
            payment.reservation = reservation
            payment.amount = (
                                         reservation.departure_date - reservation.check_in_date).days * reservation.room.price_per_day
            payment.payment_status = 'completed'  # В реальном проекте здесь была бы интеграция с платёжной системой
            payment.save()

            # Обновляем статус бронирования
            reservation.reservation_status = 'confirmed'
            reservation.save()

            # Обновляем статус комнаты
            room = reservation.room
            room.status = 'occupied' if reservation.check_in_date <= date.today() <= reservation.departure_date else 'reserved'
            room.save()

            messages.success(request, 'Бронирование успешно оплачено!')
            return redirect('clients:profile')
    else:
        form = PaymentForm()

    total_days = (reservation.departure_date - reservation.check_in_date).days
    total_price = total_days * reservation.room.price_per_day

    context = {
        'reservation': reservation,
        'form': form,
        'total_days': total_days,
        'total_price': total_price,
    }
    return render(request, 'reservations/payment.html', context)


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(
        client=request.user
    ).order_by('-check_in_date')

    return render(request, 'reservations/my_reservations.html', {
        'reservations': reservations
    })


@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, client=request.user)

    if reservation.reservation_status in ['checked_in', 'checked_out']:
        messages.error(request, 'Нельзя отменить уже начатое или завершённое бронирование')
    elif reservation.reservation_status == 'cancelled':
        messages.warning(request, 'Бронирование уже отменено')
    else:
        reservation.reservation_status = 'cancelled'
        reservation.save()

        # Если комната была зарезервирована, возвращаем её в доступные
        if reservation.room.status == 'reserved':
            reservation.room.status = 'available'
            reservation.room.save()

        messages.success(request, 'Бронирование успешно отменено')

    return redirect('reservations:my_reservations')