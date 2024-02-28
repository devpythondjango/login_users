from django.db import models
from users.validators import validate_passport_serial
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.templatetags.static import static
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils import timezone
import os
from users.models import Faculty, Kafedra
from django.db.models.signals import post_save


def admin_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/avatar/<filename>
    return f'user_{instance.user.id}/avatar/{filename}'


class AdminProfile(models.Model): 
    is_hemis_admin = models.BooleanField(default=False, null=True, blank=True)
    is_lms_admin = models.BooleanField(default=False, null=True, blank=True)
    is_kerocontrol_admin = models.BooleanField(default=False, null=True, blank=True )
    is_kerocontrol2_admin = models.BooleanField(default=False, null=True, blank=True )
    is_kerocontrol3_admin = models.BooleanField(default=False, null=True, blank=True )
    is_self_visible = models.BooleanField(default=False, null=True, blank=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    is_admin_kafedra = models.BooleanField(default=False, null=True, blank=True)
    is_admin_talim = models.BooleanField(default=False, null=True, blank=True)
    is_admin_oquv = models.BooleanField(default=False, null=True, blank=True)
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


class Author(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class FileType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Fayl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    filetype = models.ForeignKey(FileType, related_name='fayl_type', on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey(Faculty, related_name='faculty', on_delete=models.SET_NULL, null=True)
    kafedra = models.ForeignKey(Kafedra, related_name='kafedra', on_delete=models.SET_NULL, null=True)
    authn = models.ManyToManyField(Author, related_name='author', blank=True)
    fayl = models.FileField(upload_to='fayllar/')
    tasdiq_soni = models.IntegerField(null=True, blank=True, default=0)
    tasdiqlangan = models.BooleanField(default=False)
    createdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
 

class FaylTasdiq(models.Model): 
    fayl = models.ForeignKey(Fayl, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    tasdiq_vaqt = models.DateTimeField(auto_now_add=True)
    tasdiq_holati = models.BooleanField(default=False, null=True)
    admin_tekshirish_vaqt = models.DateTimeField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=FaylTasdiq)
def avtomatik_tekshirish_vaqt(sender, instance, created, **kwargs):
    if created and not instance.tasdiq_holati:
        instance.tasdiq_holati = True
        instance.admin_tekshirish_vaqt = timezone.now()
        instance.save()