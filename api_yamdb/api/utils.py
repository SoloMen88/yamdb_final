from django.core.mail import send_mail


def send_confirmation_email(confirmation_code, email):
    """Функция отправляющая код подтверждения пользователю"""
    send_mail(
        subject='Ваш код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='webmaster@localhost',
        recipient_list=[email],
        fail_silently=False
    )
