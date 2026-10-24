from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from marketplace.models import CaretakerProfile

User = get_user_model()

class PetOwnerRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter strong password'}),
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'address', 'profile_photo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unique username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 000-0000'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State, Country'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise forms.ValidationError("Email address is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists. Please sign in or use another email.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'PET_OWNER'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CaretakerRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter strong password'}),
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )
    
    # Caretaker specific fields
    experience_years = forms.DecimalField(
        max_digits=4, decimal_places=1, initial=2.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3.5'})
    )
    hourly_rate = forms.DecimalField(
        max_digits=8, decimal_places=2, initial=500.00,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 500.00 (₹/hr)'})
    )
    services_offered = forms.CharField(
        initial='Pet Sitting, Dog Walking, Overnight Boarding',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated services'})
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell pet parents about your experience and love for animals...'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'address', 'profile_photo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unique username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 000-0000'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State, Country'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise forms.ValidationError("Email address is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists. Please sign in or use another email.")
        return email

    def clean_experience_years(self):
        exp = self.cleaned_data.get('experience_years')
        if exp is not None and exp < 0:
            raise forms.ValidationError("Experience years cannot be negative.")
        return exp if exp is not None else 1.0

    def clean_hourly_rate(self):
        rate = self.cleaned_data.get('hourly_rate')
        if rate is not None and rate <= 0:
            raise forms.ValidationError("Hourly rate cannot be zero or negative. Minimum rate is ₹50/hr.")
        if rate is not None and rate < 50:
            raise forms.ValidationError("Hourly rate must be at least ₹50/hr.")
        return rate if rate is not None else 100.00

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'CARETAKER'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            CaretakerProfile.objects.update_or_create(
                user=user,
                defaults={
                    'experience_years': self.cleaned_data.get('experience_years') or 1.0,
                    'hourly_rate': self.cleaned_data.get('hourly_rate') or 25.00,
                    'services_offered': self.cleaned_data.get('services_offered') or 'Pet Sitting, Dog Walking',
                    'bio': self.cleaned_data.get('bio', '')
                }
            )
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'profile_photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CaretakerProfileEditForm(forms.ModelForm):
    class Meta:
        model = CaretakerProfile
        fields = ['experience_years', 'hourly_rate', 'services_offered', 'availability_status', 'bio']
        widgets = {
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '10', 'min': '50'}),
            'services_offered': forms.TextInput(attrs={'class': 'form-control'}),
            'availability_status': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean_hourly_rate(self):
        rate = self.cleaned_data.get('hourly_rate')
        if rate is None:
            raise forms.ValidationError("Hourly rate cannot be empty.")
        if rate <= 0:
            raise forms.ValidationError("Hourly rate cannot be zero or negative. Caretakers must set a valid positive rate (minimum ₹50/hr).")
        if rate < 50:
            raise forms.ValidationError("Hourly rate must be at least ₹50/hr.")
        return rate

    def clean_experience_years(self):
        exp = self.cleaned_data.get('experience_years')
        if exp is None:
            raise forms.ValidationError("Experience years cannot be empty.")
        if exp < 0:
            raise forms.ValidationError("Experience years cannot be negative.")
        return exp
