from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from Participant.models import User


class LoginForm(AuthenticationForm):
    captcha = CaptchaField(
        error_messages={
            'invalid': 'Invalid CAPTCHA. Please try again.',
            'required': 'Please complete the CAPTCHA.'
        }
    )


class RegisterForm(UserCreationForm):
    captcha = CaptchaField(
        error_messages={
            'invalid': 'Invalid CAPTCHA. Please try again.',
            'required': 'Please complete the CAPTCHA.'
        }
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
