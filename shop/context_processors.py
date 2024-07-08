from .models import UserRegistration

def session_data(request):
    email = request.session.get('email')
    user_registration = None
    if email:
        user_registration = UserRegistration.objects.filter(email=email).first()
    return {
        'email': email,
        'user_registration': user_registration,
    }