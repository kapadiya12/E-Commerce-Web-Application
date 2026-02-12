from django import forms
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from .models import Order, CartItem, Product


class AddToCartForm(forms.Form):
    """Form for adding items to cart with validation"""
    quantity = forms.IntegerField(
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 80px;',
        }),
        error_messages={
            'required': 'Quantity is required.',
            'invalid': 'Please enter a valid number.',
            'min_value': 'Quantity must be at least 1.',
            'max_value': 'Maximum quantity is 100.',
        }
    )
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity and quantity < 1:
            raise forms.ValidationError('Quantity must be at least 1.')
        return quantity


class UpdateCartItemForm(forms.ModelForm):
    """Form to update cart item quantity"""
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'}),
        error_messages={
            'required': 'Quantity is required.',
            'invalid': 'Please enter a valid number.',
            'min_value': 'Quantity must be at least 1.',
        }
    )
    
    class Meta:
        model = CartItem
        fields = ['quantity']
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.instance.product
        
        if quantity > product.stock:
            raise forms.ValidationError(
                f'Only {product.stock} items available in stock.'
            )
        return quantity


class CheckoutForm(forms.ModelForm):
    """Form for checkout with comprehensive validation"""
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Phone number must be valid (9-15 digits).'
    )
    
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        error_messages={'required': 'First name is required.', 'max_length': 'Max 50 characters.'}
    )
    
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        error_messages={'required': 'Last name is required.', 'max_length': 'Max 50 characters.'}
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        error_messages={'required': 'Email is required.', 'invalid': 'Enter a valid email.'}
    )
    
    phone = forms.CharField(
        max_length=20,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        error_messages={'required': 'Phone number is required.'}
    )
    
    address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
        error_messages={'required': 'Address is required.', 'max_length': 'Max 255 characters.'}
    )
    
    city = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        error_messages={'required': 'City is required.', 'max_length': 'Max 50 characters.'}
    )
    
    state = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State/Province'}),
        error_messages={'required': 'State is required.', 'max_length': 'Max 50 characters.'}
    )
    
    postal_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
        error_messages={'required': 'Postal code is required.', 'max_length': 'Max 10 characters.'}
    )
    
    payment_method = forms.ChoiceField(
        choices=[('cod', 'Cash on Delivery')],
        widget=forms.RadioSelect(),
        initial='cod',
        error_messages={'required': 'Payment method is required.'}
    )
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'postal_code', 'payment_method']
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not first_name.replace(' ', '').isalpha():
            raise forms.ValidationError('First name should only contain letters.')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not last_name.replace(' ', '').isalpha():
            raise forms.ValidationError('Last name should only contain letters.')
        return last_name
    
    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if postal_code and not postal_code.isalnum():
            raise forms.ValidationError('Postal code should contain only letters and numbers.')
        return postal_code


# ============================================================================
# AUTHENTICATION FORMS
# ============================================================================
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class RegisterForm(forms.Form):
    """Enterprise-grade user registration form with strong validation"""

    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Username',
            'id': 'register_username',
            'required': 'required'
        }),
        error_messages={
            'required': 'Username is required.',
            'max_length': 'Username must be less than 150 characters.',
        }
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Email Address',
            'id': 'register_email',
            'required': 'required'
        }),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Please enter a valid email address.',
        }
    )

    password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Password (min 8 chars, strong password)',
            'id': 'register_password',
            'required': 'required'
        }),
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 8 characters.',
        }
    )

    confirm_password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm Password',
            'id': 'register_confirm_password',
            'required': 'required'
        }),
        error_messages={
            'required': 'Please confirm your password.',
            'min_length': 'Password must be at least 8 characters.',
        }
    )

    # =========================
    # FIELD VALIDATIONS
    # =========================

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            raise ValidationError("Username is required.")

        if " " in username:
            raise ValidationError("Username cannot contain spaces.")

        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists. Please choose another.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise ValidationError("Email is required.")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered. Please use a different email or login.")

        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        # Run Django's built-in validators (min length, common password, numeric, similarity, etc.)
        validate_password(password)

        # Custom strong password rules
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")

        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter.")

        if not re.search(r"[0-9]", password):
            raise ValidationError("Password must contain at least one number.")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")

        return password

    # =========================
    # FORM LEVEL VALIDATION
    # =========================

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match. Please try again.")

        return cleaned_data


class LoginForm(forms.Form):
    """Custom user login form"""
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Username',
            'id': 'login_username',
            'required': 'required',
            'autofocus': 'autofocus'
        }),
        error_messages={
            'required': 'Username is required.',
        }
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Password',
            'id': 'login_password',
            'required': 'required'
        }),
        error_messages={
            'required': 'Password is required.',
        }
    )
