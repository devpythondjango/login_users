from django.db import models
from users.validators import validate_passport_serial
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.templatetags.static import static
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils import timezone
import os


def admin_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/avatar/<filename>
    return f'user_{instance.user.id}/avatar/{filename}'


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

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Check if this instance has a file already
        try:
            this = AdminProfile.objects.get(id=self.id)
            # If the file exists and is not the same as the new file, delete the old file
            if this.admin_avatar and this.admin_avatar != self.admin_avatar:
                this.admin_avatar.delete(save=False)
        except AdminProfile.DoesNotExist:
            pass

        super(AdminProfile, self).save(*args, **kwargs)


@receiver(post_delete, sender=AdminProfile)
def admin_profile_post_delete_handler(sender, **kwargs):
    admin_profile = kwargs['en']
    # Delete the old file when the associated UserProfile object is deleted
    if admin_profile.admin_avatar:
        admin_profile.admin_avatar.delete(False)
