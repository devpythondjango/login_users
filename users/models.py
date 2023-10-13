from django.db import models
from .validators import validate_passport_serial
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.templatetags.static import static


class Profile(models.Model):
    is_hemis_admin = models.BooleanField(default=False)
    is_moodle_admin = models.BooleanField(default=False)
    is_kerocontrol_admin = models.BooleanField(default=False)
    is_self_visible = models.BooleanField(default=False)
    selected_admin = models.CharField(max_length=20, choices=[
        ('hemis', 'Hemis'),
        ('moodle', 'Moodle'),
        ('kerocontrol', 'Kerocontrol'),
    ], null=True, blank=True)
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, gettext("Erkak")),
        (GENDER_FEMALE, gettext("Ayol")),
    ]

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_self_visible = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="profiles/avatars/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    passport_serial = models.CharField(max_length=9, validators=[validate_passport_serial], null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = gettext('Profile')
        verbose_name_plural = gettext('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('img/team/default-profile-picture.png')


class Faculty(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Kafedra(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


#####  Lavozimlar #####

class Position(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Talishakli(models.Model):
    name = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    kurs = models.CharField(max_length=10, null=True, blank=True)
    group = models.CharField(max_length=50, null=True, blank=True)
    talim_shakli = models.ForeignKey(Talishakli, on_delete=models.SET_NULL, null=True, blank=True)


class Teacher(models.Model):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.SET_NULL, null=True, blank=True)


class Bolim(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


########


#####  Tizimlar  ######

class System(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Hemis(models.Model):
    hemis_id = models.CharField(max_length=25, null=True, blank=True)
    system = models.ForeignKey(System, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.hemis_id


class Lms(models.Model):
    lms_id = models.CharField(max_length=25, null=True, blank=True)
    system = models.ForeignKey(System, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.lms_id


class KeroControl(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    system = models.ForeignKey(System, on_delete=models.SET_NULL, null=True, blank=True)


class Building(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    kerocontrol = models.ForeignKey(KeroControl, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


########


class Application(models.Model):
    first_name = models.CharField(max_length=15, null=True, blank=True, default='Ism')
    lest_name = models.CharField(max_length=20, null=True, blank=True, default='Familiya')
    surname = models.CharField(max_length=20, null=True, blank=True, default='Sharf')
    birthday = models.DateField(null=True, blank=True)
    passport_serial = models.CharField(max_length=9, validators=[validate_passport_serial], null=True, blank=True)
    passport_image = models.ImageField(upload_to=f'user/{first_name}/passport', null=True, blank=True)
    image = models.ImageField(upload_to=f'user/{first_name}/image', null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    system = models.ForeignKey(System, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.lest_name}"


class ApplicationCreate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    createdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-createdate']
