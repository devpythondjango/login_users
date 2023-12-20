from django.db import models
from users.validators import validate_passport_serial
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.templatetags.static import static


class AdminProfile(models.Model): 
    is_hemis_admin = models.BooleanField(default=False, null=True, blank=True)
    is_lms_admin = models.BooleanField(default=False, null=True, blank=True)
    is_kerocontrol_admin = models.BooleanField(default=False, null=True, blank=True )
    is_self_visible = models.BooleanField(default=False, null=True, blank=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, gettext("Erkak")),
        (GENDER_FEMALE, gettext("Ayol")),
    ]
    user = models.OneToOneField(User, related_name="admin_profile", on_delete=models.CASCADE)
    admin_avatar = models.ImageField(upload_to="admin/profiles/", null=True, blank=True)
    back_admin_avatar = models.ImageField(upload_to="admin/back/", null=True, blank=True)
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
    def get_admin_avatar(self):
        return self.admin_avatar.url if self.admin_avatar else static('img/team/default-profile-picture.png')

    @property
    def get_back_admin_avatar(self):
        return self.back_admin_avatar.url if self.back_admin_avatar else static('')

    def __str__(self):
        return self.user.username