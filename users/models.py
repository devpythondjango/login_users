from django.db import models
from .validators import validate_passport_serial
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.templatetags.static import static


class Profile(models.Model):
    is_hemis_admin = models.BooleanField(default=False, null=True, blank=True)
    is_moodle_admin = models.BooleanField(default=False, null=True, blank=True)
    is_kerocontrol_admin = models.BooleanField(default=False, null=True, blank=True)
    is_self_visible = models.BooleanField(default=False, null=True, blank=True)
    selected_admin = models.CharField(max_length=20, choices=[
        ('hemis', 'Hemis'),
        ('lms', 'LMS'),
        ('kerocontrol', 'Kerocontrol'),
    ], null=True, blank=True)
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, gettext("Erkak")),
        (GENDER_FEMALE, gettext("Ayol")),
    ]
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    is_self_visible = models.BooleanField(default=False, null=True, blank=True)
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


class Faculty(models.Model):  # 1-model
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Kafedra(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


#####  Lavozimlar #####

class Position(models.Model):  # 2-model
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Talimshakli(models.Model):
    name = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):  # 3-model
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    kurs = models.CharField(max_length=10, null=True, blank=True)
    group = models.CharField(max_length=50, null=True, blank=True)
    talim_shakli = models.ForeignKey(Talimshakli, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.group:
            return self.group
        return f"Student id: {self.id}"


class Teacher(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.name:
            return self.name
        return f"O'qituvchi id: {self.id}"


class PositionOne(models.Model):
    name = models.CharField(max_length=70, null=True, blank=True)

    def __str__(self):
        return self.name


class Bolim(models.Model):
    positionone = models.ForeignKey(PositionOne, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if self.name:  # Eslatma: nomi maydonining nomi o'zgaruvchisi
            return self.name
        return f"Bolim id: {self.id}"


########


#####  Tizimlar  ######

class System(models.Model):  # 4-model
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Hemis(models.Model):  # 5-model
    hemis_id = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        if self.hemis_id:
            return self.hemis_id
        return f"Hemis id: {self.id}"


class Lms(models.Model):
    lms_id = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        if self.lms_id:
            return self.lms_id
        return f"Lms id: {self.id}"


class Building(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class KeroControl(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.name:
            return self.name
        return f"Kero id: {self.id}"


########


class Application(models.Model):  # 6-model
    STATUS_CHOICES = (
        ('tekshirilmoqda', 'Tekshirilmoqda'),
        ('rad etildi', 'Rad etildi'),
        ('tekshirildi', 'Tekshirildi'),
    )
    user = models.OneToOneField(User, related_name="forms", on_delete=models.CASCADE, null=True, blank=True)
    surname = models.CharField(max_length=20, null=True, blank=True, default='Sharf')
    birthday = models.DateField(null=True, blank=True)
    passport_serial = models.CharField(max_length=9, validators=[validate_passport_serial], null=True, blank=True)
    passport_image = models.ImageField(upload_to='user_passport/', null=True, blank=True)
    image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    system = models.ForeignKey(System, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=14,
                              choices=STATUS_CHOICES,
                              default='tekshirilmoqda')

    def save(self, *args, **kwargs):
        # Fayllarni saqlash va boshqa kerakli operatsiyalarni bajaring
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name if self.user else "No User"


class ApplicationCreate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    createdate = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        if self.body:
            return self.body[0:50]
        return f"Arizachi : {self.user}"

    class Meta:
        ordering = ['-update', '-createdate']

    def save(self, *args, **kwargs):
        # Foydalanuvchiga xabar yozish
        if self.user and self.body:
            message_body = f"Sizning arizangizni qabul qildik: {self.body}"
            # admin_message = AdminMessage.objects.create(user=self.user, body=message_body)

        # Faqat admin yozishi uchun
        if self.user and self.body:
            super().save(*args, **kwargs)
