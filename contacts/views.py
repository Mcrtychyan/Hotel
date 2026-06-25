from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def contacts_view(request):
    return render(request, 'components/contacts.html')


def send_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        subject_choices = {
            'booking': 'Бронирование',
            'question': 'Вопрос',
            'suggestion': 'Предложение',
            'other': 'Другое'
        }
        subject_text = subject_choices.get(subject, 'Другое')

        full_message = f"""
        От: {name} ({email})
        Тема: {subject_text}

        Сообщение:
        {message}
        """

        try:
            send_mail(
                f'Сообщение с сайта Grand Hotel - {subject_text}',
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                ['partygamestop007@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
        except Exception as e:
            messages.error(request, 'Произошла ошибка при отправке. Попробуйте позже.')

        return redirect('contacts:contacts')

    return redirect('contacts:contacts')