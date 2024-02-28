from django import forms
from users.models import ApplicationCreate, Application
from .models import AdminProfile, Fayl, Author, FaylTasdiq


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


class FaylInputForm(forms.ModelForm):
    class Meta:
        model = Fayl
        fields = '__all__'
        widgets = {
            "user": forms.Select(attrs={'class': 'form-control'}),
            "faculty": forms.Select(attrs={'class': 'form-control'}),
            "kafedra": forms.Select(attrs={'class': 'form-control'}),
            "authn": forms.SelectMultiple(attrs={'class': 'form-control'}),
            "filetype": forms.Select(attrs={'class': 'form-control'}),
            "fayl": forms.FileInput(attrs={'class': 'form-control', 'id':'fayl', "accept":".pdf"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FaylInputForm, self).__init__(*args, **kwargs)
        if user and self.instance:
            self.fields['user'].initial = user
            self.fields['kafedra'].initial = self.instance.kafedra


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "kafedra": forms.Select(attrs={'class': 'form-control'}),
        }

