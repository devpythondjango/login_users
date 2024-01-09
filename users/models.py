from django.db import models
from .validators import validate_passport_serial
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.templatetags.static import static
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils import timezone
import os


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/avatar/<filename>
    return f'user_{instance.user.id}/avatar/{filename}'


class Profile(models.Model): 
    is_users = models.BooleanField(default=True, null=True, blank=True)
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, gettext("Erkak")),
        (GENDER_FEMALE, gettext("Ayol")),
    ]
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="user/profiles/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    passport_serial = models.CharField(max_length=9, validators=[validate_passport_serial], null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        verbose_name = gettext('Profile')
        verbose_name_plural = gettext('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('img/team/default-profile-picture.png')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Check if this instance has a file already
        try:
            this = Profile.objects.get(id=self.id)
            # If the file exists and is not the same as the new file, delete the old file
            if this.avatar and this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except Profile.DoesNotExist:
            pass

        super(Profile, self).save(*args, **kwargs)


@receiver(post_delete, sender=Profile)
def user_profile_post_delete_handler(sender, **kwargs):
    user_profile = kwargs['instance']
    # Delete the old file when the associated UserProfile object is deleted
    if user_profile.avatar:
        user_profile.avatar.delete(False)


class Faculty(models.Model):  # 1-model
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Kafedra(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Position(models.Model):  # 2-model
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class System(models.Model):  # 4-model
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Talimshakli(models.Model):
    name = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name


class PositionOne(models.Model):
    name = models.CharField(max_length=70, null=True, blank=True)

    def __str__(self):
        return self.name


class Building(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    passport_serial = models.CharField(max_length=9, validators=[validate_passport_serial], null=True, blank=True)
    passport_image = models.ImageField(upload_to='user_passport/', null=True, blank=True)
    image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    system = models.ForeignKey(System, on_delete=models.SET_NULL, null=True, blank=True)

    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    kurs = models.CharField(max_length=10, null=True, blank=True)
    group = models.CharField(max_length=50, null=True, blank=True)
    talim_shakli = models.ForeignKey(Talimshakli, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=50, null=True, blank=True)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.SET_NULL, null=True, blank=True)
    positionone = models.ForeignKey(PositionOne, on_delete=models.SET_NULL, null=True, blank=True)

    tizim = models.CharField(max_length=50, null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True, blank=True)

    text = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    @property
    def get_passport(self):
        return self.passport_image.url if self.passport_image else static('')

    @property
    def get_image(self):
        return self.image.url if self.image else static('')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ApplicationCreate(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    application = models.OneToOneField(Application,  related_name='app_create', on_delete=models.SET_NULL, null=True, blank=True) 
    update = models.DateTimeField(auto_now=True)
    createdate = models.DateTimeField(auto_now_add=True)

    body = models.TextField(null=True, blank=True, default='Yo\'q')
    STATUS_CHOICES = (
        ('yangi', 'Yangi'),
        ('tekshirilmoqda', 'Tekshirilmoqda'),
        ('rad etildi', 'Rad etildi'),
        ('tekshirildi', 'Tekshirildi'),
    )
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='yangi', null=True)

    class Meta:
        ordering = ['-update', '-createdate']

    def __str__(self):
        return self.user.username if self.user else 'Foydalanuvchi yuq'
