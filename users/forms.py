from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile, Application, Student, Teacher, Bolim, Hemis, KeroControl, Lms, Faculty, Kafedra, Position, Talimshakli, PositionOne, System, Building





class ArizaForm(forms.Form):
    selected_admin = forms.ChoiceField(choices=[
        ('hemis', 'Hemis'),
        ('moodle', 'Moodle'),
        ('kerocontrol', 'Kerocontrol'),
    ])
    ariza = forms.CharField(widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}))


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']  # Qolgan maydonlar

    def clean_email(self):
        # E-mailni tekshirish uchun o'zgartirishlarni qo'shing (mumkin)
        email = self.cleaned_data['email']
        # E-mail tekshirish va muayyan bir shartni bajarish mumkin
        if "example.com" in email:
            raise forms.ValidationError("Example.com manzilini ishlatmaslik kerak")
        return email


# class ProfileForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=255)
#     last_name = forms.CharField(max_length=255)
#     email = forms.EmailField()

#     class Meta:
#         model = Profile
#         fields = '__all__'
#         exclude = ['user'

def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg


class ApplicationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    class Meta:
        model = Application
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "surname": forms.TextInput(attrs={'class': 'form-control'}),
            "birthday": forms.DateInput(attrs={'class': 'form-control'}),
            "passport_serial":forms.TextInput(attrs={'class': 'form-control'}),
            "passport_image": forms.FileInput(attrs={'class': 'form-control'}),
            "image": forms.FileInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
            "position": forms.Select(attrs={'class': 'form-control', 'id': 'id_position', 'onchange': 'showDiv(this)'}),
            "system": forms.Select(attrs={'class': 'form-control', 'id': 'id_system', 'onchange': 'showDiv1(this)'}),
            "text": forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        # Form kwargs orqali user ni olish
        user = kwargs.pop('user', None)

        # Ota class konstruktorini chaqirish
        super(ApplicationForm, self).__init__(*args, **kwargs)

        # Agar user admin bo'lsa, status maydonini tahrirlashga ruxsat berish
        if user and user.is_staff:
            self.fields['status'] = forms.ChoiceField(choices=Application.STATUS_CHOICES, required=True)
        else:
            # Agar user admin bo'lmasa, status maydonini formadan tashlash
            self.fields.pop('status', None)

        
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            "faculty": forms.Select(attrs={'class': 'form-control'}),
            "kurs": forms.TextInput(attrs={'class': 'form-control'}),
            "group": forms.TextInput(attrs={'class': 'form-control'}),
            "talim_shakli": forms.Select(attrs={'class': 'form-control'}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"
        widgets = {
            "faculty": forms.Select(attrs={'class': 'form-control'}),
            "kafedra": forms.Select(attrs={'class': 'form-control'}),
            "name": forms.TextInput(attrs={'class': 'form-control'}),
        }

class BolimForm(forms.ModelForm):
    class Meta:
        model = Bolim
        fields = "__all__"
        widgets = {
            "positionone": forms.Select(attrs={'class': 'form-control'}),
            "name": forms.TextInput(attrs={'class': 'form-control'}),
        }

class HemisForm(forms.ModelForm):
    class Meta:
        model = Hemis
        fields = "__all__"
        widgets = {
            "hemis_id": forms.TextInput(attrs={'class': 'form-control'}),
        }

class LmsForm(forms.ModelForm):
    class Meta:
        model = Lms
        fields = "__all__"
        widgets = {
            "lms_id": forms.TextInput(attrs={'class': 'form-control'}),
        }

class KerocontrolForm(forms.ModelForm):
    class Meta:
        model = KeroControl
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "building": forms.Select(attrs={'class': 'form-control'}),
        }
