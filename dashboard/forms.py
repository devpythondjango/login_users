from django import forms
from users.models import ApplicationCreate, Application
from .models import AdminProfile


class ApplicationCreateForm(forms.ModelForm):
    class Meta: 
        model = ApplicationCreate
        fields = "__all__"
        widgets = {
            "status": forms.Select(attrs={'class': 'form-control'}),
            "user": forms.Select(attrs={'class': 'form-control', 'readonly': True}),
            "application": forms.Select(attrs={'class': 'form-control', 'readonly': True}),
         }


class AdminProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = AdminProfile
        fields = '__all__'
        exclude = ['user']

    def clean_email(self):
        email = self.cleaned_data['email']
        if "example.com" in email:
            raise forms.ValidationError("Example.com manzilini ishlatmaslik kerak")
        return email
