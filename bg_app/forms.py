# bg_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Role, Student, Staff

class UserForm(UserCreationForm):
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        required=False,
        empty_label="Select Role"
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'role', 'profile_picture', 'phone_number', 'address',
            'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class UserUpdateForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        required=False,
        empty_label="Select Role"
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'role', 'profile_picture', 'phone_number', 'address',
            'status'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['enrollment_number', 'qualification', 'training', 'total_fees','fees_paid', 'training_end_date']
        widgets = {
            'enrollment_number': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'training': forms.TextInput(attrs={'class': 'form-control'}),
            'total_fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'fees_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'training_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['employee_id', 'department', 'position', 'salary','paid_salary', 'join_date']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'paid_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'join_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description', 'permissions']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'permissions': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }