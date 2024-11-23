from django import forms
from .models import Task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError

# TaskForm to handle task creation/editing
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']


class UserInviteForm(forms.Form):
    email = forms.EmailField(label='Invitee Email', required=True)

    def send_invitation(self):
        # Get the email from the cleaned data
        email = self.cleaned_data['email']

        # Define the subject and message for the invitation email
        subject = 'Invitation to Join Our Platform'
        registration_link = 'http://127.0.0.1:8000/accounts/signup/?invite_token=xyz'  # Replace 'xyz' with a dynamic token if needed
        message = f'Hello,\n\nYou have been invited to join our platform! Click the link below to register:\n\n{registration_link}\n\nBest regards,\nYour Team'

        # Use Django's send_mail function to send the email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,

        )



class CustomSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Passwords do not match.')



