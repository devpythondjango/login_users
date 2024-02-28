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
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
            "position": forms.Select(attrs={'class': 'form-control form-control-lg border-success', 'id': 'id_position', 'onchange': 'showDiv(this)', 'required': True}),
            "system": forms.Select(attrs={'class': 'form-control form-control-lg border-success', 'id': 'id_system', 'onchange': 'showDiv1(this)'}),
            "faculty": forms.Select(attrs={'class': 'form-control form-control-lg border-success'}),
            "talim_shakli": forms.Select(attrs={'class': 'form-control form-control-lg border-success'}),
            "name": forms.TextInput(attrs={'class': 'form-control form-control-lg border-success'}),
            "kafedra": forms.Select(attrs={'class': 'form-control form-control-lg border-success'}),
            "positionone": forms.Select(attrs={'class': 'form-control form-control-lg border-success'}),
            "tizim": forms.TextInput(attrs={'class': 'form-control form-control-lg border-success'}),
            "building": forms.Select(attrs={'class': 'form-control form-control-lg border-success'}),
            
            "login_create": forms.Select(attrs={'class': 'form-control form-control-lg border-success', 'id': 'id_login_create', 'onchange': 'showDiv2(this)', 'required': True}),
            "group": forms.TextInput(attrs={'class': 'form-control form-control-lg border-success'}),
            "text": forms.TextInput(attrs={'class': 'form-control form-control-lg border-success'}),

            "status":forms.Select(attrs={'class': 'form-control'}),
            "body": forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ApplicationForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
