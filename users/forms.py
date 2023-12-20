from django import forms
from users.models import Application, Profile



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

    def clean_email(self):
        email = self.cleaned_data['email']
        if "example.com" in email:
            raise forms.ValidationError("Example.com manzilini ishlatmaslik kerak")
        return email


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "user": forms.Select(attrs={'class': 'form-control'}),
            "birthday": forms.DateInput(attrs={'class': 'form-control'}),
            "passport_serial": forms.TextInput(attrs={'class': 'form-control'}),
            "passport_image": forms.FileInput(attrs={'class': 'form-control'}),
            "image": forms.FileInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
            "position": forms.Select(attrs={'class': 'form-control', 'id': 'id_position', 'onchange': 'showDiv(this)', 'required': True}),
            "system": forms.Select(attrs={'class': 'form-control', 'id': 'id_system', 'onchange': 'showDiv1(this)', 'required': True}),
            "faculty": forms.Select(attrs={'class': 'form-control'}),
            "kurs": forms.TextInput(attrs={'class': 'form-control'}),
            "group": forms.TextInput(attrs={'class': 'form-control'}),
            "talim_shakli": forms.Select(attrs={'class': 'form-control'}),
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "kafedra": forms.Select(attrs={'class': 'form-control'}),
            "positionone": forms.Select(attrs={'class': 'form-control'}),
            "tizim": forms.TextInput(attrs={'class': 'form-control'}),
            "building": forms.Select(attrs={'class': 'form-control'}),
            
            "text": forms.TextInput(attrs={'class': 'form-control'}),

            "status":forms.Select(attrs={'class': 'form-control'}),
            "body": forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ApplicationForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
