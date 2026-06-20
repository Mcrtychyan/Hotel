from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation, Payment
from rooms.models import Room
from datetime import date, timedelta


class ReservationForm(forms.ModelForm):
    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата заезда'
    )
    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата выезда'
    )

    class Meta:
        model = Reservation
        fields = ['check_in_date', 'departure_date']

    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        super().__init__(*args, **kwargs)

        # Минимальная дата - сегодня
        today = date.today()
        self.fields['check_in_date'].widget.attrs['min'] = today.strftime('%Y-%m-%d')
        self.fields['departure_date'].widget.attrs['min'] = (today + timedelta(days=1)).strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        departure = cleaned_data.get('departure_date')

        if check_in and departure:
            if departure <= check_in:
                raise ValidationError('Дата выезда должна быть позже даты заезда')

            # Проверяем, свободен ли номер на эти даты
            if self.room:
                overlapping = Reservation.objects.filter(
                    room=self.room,
                    reservation_status__in=['pending', 'confirmed', 'checked_in'],
                    check_in_date__lt=departure,
                    departure_date__gt=check_in
                )
                if overlapping.exists():
                    raise ValidationError('Номер уже забронирован на выбранные даты')

        return cleaned_data


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'payment_method': 'Способ оплаты'
        }