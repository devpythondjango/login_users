from django.shortcuts import render, redirect, get_object_or_404
from authn.forms import form_validation_error
from django.contrib import messages
from users.models import Profile, Application, ApplicationCreate, Kafedra
from authn.views import login_decorator
from .forms import ApplicationCreateForm, AdminProfileForm, FaylInputForm, AuthorForm
from .models import AdminProfile, Fayl, FaylTasdiq, Author, FileType
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.http import HttpResponseRedirect


@login_required
@login_decorator
@csrf_protect
@ensure_csrf_cookie
def admin_profile_view(request):
    if request.user.admin_profile.is_admin:

        last_login_time = request.user.last_login
        # Agar o'zingizning so'nggi kirish vaqtingizdan 1 soat o'tib ketgan bo'lsa
        if timezone.now() - last_login_time > timedelta(hours=1):
        # Bu yerdan foydalanuvchi uchun kerakli amallarni bajarishingiz mumkin
        # Masalan, yangi login qilish logikasi yoki xabar yuborish, qo'shimcha ma'lumotlar, va hokazo.

        # Misol uchun yangi kirish vaqti saqlang
            request.user.last_login_check = timezone.now()
            request.user.save()

        holat = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_count3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_newlogin_count1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1).count()
        
        holat_kero_newlogin_count3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3)

        holat_kero = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=1)
        
        holat_kero3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3)
        
        holat_kero_newlogin_3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1)
        
        holat_kero_newlogin_1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1)

        holat_vaucher_count = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2).count()

        holat_vaucher = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2)
        

        admin_profile, __ = AdminProfile.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            form = AdminProfileForm(request.POST, request.FILES, instance=admin_profile)
            if form.is_valid():
                admin_profile = form.save()
                admin_profile.user.first_name = form.cleaned_data.get('first_name')
                admin_profile.user.last_name = form.cleaned_data.get('last_name')
                admin_profile.user.email = form.cleaned_data.get('email')
                admin_profile.user.save()

                messages.success(request, 'Profil muvaffaqiyatli saqlandi')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                messages.error(request, form_validation_error(form))
            print(form.errors)
            return redirect('admin_profile')


        context = {
            'admin_profile': admin_profile,
            'segment': 'admin_profile', 
            'holat_hemis': holat_hemis,
            'holat_lms': holat_lms,
            'holat_kero': holat_kero,
            # news
            'holat_kero3': holat_kero3,
            'holat_kero_newlogin_1':holat_kero_newlogin_1,
            'holat_kero_newlogin_3':holat_kero_newlogin_3,
            'holat_vaucher':holat_vaucher,
            
            'holat_hemis_count': holat_hemis_count,
            'holat_lms_count': holat_lms_count,
            'holat_kero_count': holat_kero_count,
            # news
            'holat_kero_count3': holat_kero_count3,
            'holat_kero_newlogin_count1':holat_kero_newlogin_count1,
            'holat_kero_newlogin_count3':holat_kero_newlogin_count3,
            'holat_vaucher_count':holat_vaucher_count,

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/admin/profile.html', context)

    else:
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


@login_decorator
@csrf_protect
@ensure_csrf_cookie
def index(request):
    today = timezone.now()
    if request.user.admin_profile.is_admin:  # user.admin_profile.is_admin

        oy_1_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=1,
            app_create__createdate__year=today.year,
            system=1).count()
        oy_2_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=2,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=1).count()
        oy_3_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=3,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=1).count()
        oy_4_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=4,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=1).count()
        oy_5_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=5,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=1).count()
        oy_6_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=6,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=1).count()
        oy_7_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=7,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=1).count()
        oy_8_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=8,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=1).count()
        oy_9_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=9,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=1).count()
        oy_10_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=10,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=1).count()
        oy_11_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=11,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=1).count()
        oy_12_1 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=12,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=1).count()

        oy_1_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=1,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()
        oy_2_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=2,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()
        oy_3_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=3,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()
        oy_4_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=4,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()
        oy_5_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=5,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()
        oy_6_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=6,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()
        oy_7_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=7,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()
        oy_8_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=8,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()
        oy_9_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=9,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()
        oy_10_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=10,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()
        oy_11_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=11,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()
        oy_12_2 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=12,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=2).count()

        oy_1_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=1,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()
        oy_2_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=2,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()
        oy_3_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=3,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()
        oy_4_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=4,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()
        oy_5_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=5,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()
        oy_6_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=6,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()
        oy_7_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=7,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()
        oy_8_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=8,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()
        oy_9_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=9,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()
        oy_10_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=10,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()
        oy_11_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=11,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()
        oy_12_3 = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__createdate__month=12,  # January
            app_create__createdate__year=today.year,  # Filter by the current year
            system=3).count()

        holat = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_count3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_newlogin_count1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1).count()
        
        holat_kero_newlogin_count3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3)

        holat_kero = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=1)
        
        holat_kero3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3)
        
        holat_kero_newlogin_3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1)
        
        holat_kero_newlogin_1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1)

        holat_vaucher_count = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2).count()

        holat_vaucher = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2)

        foiz = Application.objects.count()
        hemis = Application.objects.filter(system=1).count()
        kero = Application.objects.filter(system=3).count()
        lms = Application.objects.filter(system=2).count()
        if foiz > 0:
            hemis_foiz = hemis * 100 / foiz
            kero_foiz = kero * 100 / foiz
            lms_foiz = lms * 100 / foiz
        else:
            hemis_foiz, kero_foiz, lms_foiz = 0, 0, 0

        hemis_foiz_formatted = "{:.1f}%".format(hemis_foiz)
        kero_foiz_formatted = "{:.1f}%".format(kero_foiz)
        lms_foiz_formatted = "{:.1f}%".format(lms_foiz)

        fayl_type = FileType.objects.all()
        kafedra = Kafedra.objects.all()

        fayl_tasdiq_son1 = []
        for i in fayl_type:
            fayl_tasdiq_son1.append(Fayl.objects.prefetch_related('filetype', 'kafedra').filter(filetype__name=f"{str(i)}", kafedra__name="Axborat xavfsizligi", tasdiq_soni=2).count())
        fayl_tasdiq_son2 = []
        for i in fayl_type:
            fayl_tasdiq_son2.append(Fayl.objects.prefetch_related('filetype', 'kafedra').filter(filetype__name=f"{str(i)}", kafedra__name="Axborot texnologiyalari", tasdiq_soni=2).count())
        fayl_tasdiq_son3 = []
        for i in fayl_type:
            fayl_tasdiq_son3.append(Fayl.objects.prefetch_related('filetype', 'kafedra').filter(filetype__name=f"{str(i)}", kafedra__name="Dasturiy injiniring", tasdiq_soni=2).count())
        fayl_tasdiq_son4 = []
        for i in fayl_type:
            fayl_tasdiq_son4.append(Fayl.objects.prefetch_related('filetype', 'kafedra').filter(filetype__name=f"{str(i)}", kafedra__name="Kompyuter tizimlari kafedrasi", tasdiq_soni=2).count())
        fayl_tasdiq_son5 = []
        for i in fayl_type:
            fayl_tasdiq_son5.append(Fayl.objects.prefetch_related('filetype', 'kafedra').filter(filetype__name=f"{str(i)}", kafedra__name="Axborot ta’lim texnologiyalari", tasdiq_soni=2).count())
        fayl_tasdiq_son6 = []
        for i in fayl_type:
            fayl_tasdiq_son6.append(Fayl.objects.prefetch_related('filetype', 'kafedra').filter(filetype__name=f"{str(i)}", kafedra__name="Gumanitar va ijtimoiy fanlar", tasdiq_soni=2).count())
        fayl_tasdiq_son7 = []
        for i in fayl_type:
            fayl_tasdiq_son7.append(Fayl.objects.prefetch_related('filetype', 'kafedra').filter(filetype__name=f"{str(i)}", kafedra__name="Tabiiy fanlar", tasdiq_soni=2).count())
        fayl_tasdiq_son8 = []
        for i in fayl_type:
            fayl_tasdiq_son8.append(Fayl.objects.prefetch_related('filetype', 'kafedra').filter(filetype__name=f"{str(i)}", kafedra__name="Telekommunikatsiya injiniringi", tasdiq_soni=2).count())
        fayl_tasdiq_son9 = []
        for i in fayl_type:
            fayl_tasdiq_son9.append(Fayl.objects.prefetch_related('filetype', 'kafedra').filter(filetype__name=f"{str(i)}", kafedra__name="Tillar kafedrasi", tasdiq_soni=2).count())

        fayl_tasdiq_fakultet_son1 = []
        for i in fayl_type:
            fayl_tasdiq_fakultet_son1.append(Fayl.objects.prefetch_related('filetype', 'faculty').filter(filetype__name=f"{str(i)}", faculty__name="Telekommunikatsiya texnologiyalari va kasb ta'limi", tasdiq_soni=2).count())
        
        fayl_tasdiq_fakultet_son2 = []
        for i in fayl_type:
            fayl_tasdiq_fakultet_son2.append(Fayl.objects.prefetch_related('filetype', 'faculty').filter(filetype__name=f"{str(i)}", faculty__name="Kompyuter injiniringi fakulteti", tasdiq_soni=2).count())

        ctx = {
            'hemis': hemis, 'lms': lms, 'kero': kero,
            'hemis_foiz': hemis_foiz_formatted,
            'kero_foiz': kero_foiz_formatted,
            'lms_foiz': lms_foiz_formatted,
            'segment': 'index',

            'holat_hemis': holat_hemis,
            'holat_lms': holat_lms,
            'holat_kero': holat_kero,

            'holat_hemis_count': holat_hemis_count,
            'holat_lms_count': holat_lms_count,
            'holat_kero_count': holat_kero_count,

            # news
            'holat_kero3': holat_kero3,
            'holat_kero_newlogin_1':holat_kero_newlogin_1,
            'holat_kero_newlogin_3':holat_kero_newlogin_3,
            'holat_vaucher':holat_vaucher,
            'holat_kero_count3': holat_kero_count3,
            'holat_kero_newlogin_count1':holat_kero_newlogin_count1,
            'holat_kero_newlogin_count3':holat_kero_newlogin_count3,
            'holat_vaucher_count':holat_vaucher_count,

            'holat': holat,
            'holat_count': holat_count,
            'oy_1_1': oy_1_1, 'oy_2_1': oy_2_1, 'oy_3_1': oy_3_1, 'oy_4_1': oy_4_1,
            'oy_5_1': oy_5_1, 'oy_6_1': oy_6_1, 'oy_7_1': oy_7_1, 'oy_8_1': oy_8_1,
            'oy_9_1': oy_9_1, 'oy_10_1': oy_10_1, 'oy_11_1': oy_11_1, 'oy_12_1': oy_12_1,

            'oy_1_2': oy_1_2, 'oy_2_2': oy_2_2, 'oy_3_2': oy_3_2, 'oy_4_2': oy_4_2,
            'oy_5_2': oy_5_2, 'oy_6_2': oy_6_2, 'oy_7_2': oy_7_2, 'oy_8_2': oy_8_2,
            'oy_9_2': oy_9_2, 'oy_10_2': oy_10_2, 'oy_11_2': oy_11_2, 'oy_12_2': oy_12_2,

            'oy_1_3': oy_1_3, 'oy_2_3': oy_2_3, 'oy_3_3': oy_3_3, 'oy_4_3': oy_4_3,
            'oy_5_3': oy_5_3, 'oy_6_3': oy_6_3, 'oy_7_3': oy_7_3, 'oy_8_3': oy_8_3,
            'oy_9_3': oy_9_3, 'oy_10_3': oy_10_3, 'oy_11_3': oy_11_3, 'oy_12_3': oy_12_3,

            'fayl_type':fayl_type,
            'kafedra':kafedra,
            'fayl_tasdiq_son1':fayl_tasdiq_son1,
            'fayl_tasdiq_son2':fayl_tasdiq_son2,
            'fayl_tasdiq_son3':fayl_tasdiq_son3,
            'fayl_tasdiq_son4':fayl_tasdiq_son4,
            'fayl_tasdiq_son5':fayl_tasdiq_son5,
            'fayl_tasdiq_son6':fayl_tasdiq_son6,
            'fayl_tasdiq_son7':fayl_tasdiq_son7,
            'fayl_tasdiq_son8':fayl_tasdiq_son8,
            'fayl_tasdiq_son9':fayl_tasdiq_son9,
            'fayl_tasdiq_fakultet_son1':fayl_tasdiq_fakultet_son1,
            'fayl_tasdiq_fakultet_son2':fayl_tasdiq_fakultet_son2,
        }
        # return render(request, 'admins/index.html', ctx)
        return render(request, 'admins/admin/dashboard.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


@login_decorator
@csrf_protect
@ensure_csrf_cookie
def hemis_arizalar(request):
    if request.user.admin_profile.is_admin:  # user.admin_profile.is_admin
        holat = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_count3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_newlogin_count1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1).count()
        
        holat_kero_newlogin_count3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3)

        holat_kero = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=1)
        
        holat_kero3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3)
        
        holat_kero_newlogin_3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1)
        
        holat_kero_newlogin_1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1)

        holat_vaucher_count = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2).count()

        holat_vaucher = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2)

        q = request.GET.get('q') if request.GET.get('q') != None else ''
        profiles = Profile.objects.all()
        hemis = Application.objects.filter(
            Q(first_name__contains=q) |
            Q(last_name__contains=q) |
            Q(phone__contains=q) |
            Q(passport_serial__icontains=q)
        ).filter(system=1, login_create=3)
        application_create = ApplicationCreate.objects.all()
        ctx = {
            'hemis': hemis, 
            'profiles': profiles,
            'application_create': application_create,
            'holat_hemis': holat_hemis,
            'holat_lms': holat_lms,
            'holat_kero': holat_kero,
            'segment': 'hemis_arizalar',
            'holat_hemis_count': holat_hemis_count,
            'holat_lms_count': holat_lms_count,
            'holat_kero_count': holat_kero_count,

            # news
            'holat_kero3': holat_kero3,
            'holat_kero_newlogin_1':holat_kero_newlogin_1,
            'holat_kero_newlogin_3':holat_kero_newlogin_3,
            'holat_vaucher':holat_vaucher,
            'holat_kero_count3': holat_kero_count3,
            'holat_kero_newlogin_count1':holat_kero_newlogin_count1,
            'holat_kero_newlogin_count3':holat_kero_newlogin_count3,
            'holat_vaucher_count':holat_vaucher_count,

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/admin/hemis_ariza.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


@login_decorator
@csrf_protect
@ensure_csrf_cookie
def kero_a_arizalar(request):
    if request.user.admin_profile.is_admin:  # user.admin_profile.is_admin
        holat = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_count3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_newlogin_count1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1).count()
        
        holat_kero_newlogin_count3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3)

        holat_kero = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=1)
        
        holat_kero3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3)
        
        holat_kero_newlogin_3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1)
        
        holat_kero_newlogin_1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1)

        holat_vaucher_count = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2).count()

        holat_vaucher = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2)

        q = request.GET.get('q') if request.GET.get('q') != None else ''
        profiles = Profile.objects.all()
        kero = Application.objects.filter(
            Q(first_name__contains=q) |
            Q(last_name__contains=q) |
            Q(phone__contains=q) |
            Q(passport_serial__icontains=q)
        ).filter(system=3)
        application_create = ApplicationCreate.objects.all()
        ctx = {
            'kero': kero,
            'profiles': profiles,
            'application_create': application_create,
            'holat_hemis': holat_hemis,
            'holat_lms': holat_lms,
            'holat_kero': holat_kero,
            'segment': 'kero_a_arizalar',
            'holat_hemis_count': holat_hemis_count,
            'holat_lms_count': holat_lms_count,
            'holat_kero_count': holat_kero_count,

            # news
            'holat_kero3': holat_kero3,
            'holat_kero_newlogin_1':holat_kero_newlogin_1,
            'holat_kero_newlogin_3':holat_kero_newlogin_3,
            'holat_vaucher':holat_vaucher,
            'holat_kero_count3': holat_kero_count3,
            'holat_kero_newlogin_count1':holat_kero_newlogin_count1,
            'holat_kero_newlogin_count3':holat_kero_newlogin_count3,
            'holat_vaucher_count':holat_vaucher_count,

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/admin/kerio_ariza.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))

@login_decorator
@csrf_protect
@ensure_csrf_cookie
def kero_c_arizalar(request):
    if request.user.admin_profile.is_admin:  # user.admin_profile.is_admin
        holat = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_count3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_newlogin_count1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1).count()
        
        holat_kero_newlogin_count3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3)

        holat_kero = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=1)
        
        holat_kero3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3)
        
        holat_kero_newlogin_3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1)
        
        holat_kero_newlogin_1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1)

        holat_vaucher_count = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2).count()

        holat_vaucher = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2)

        q = request.GET.get('q') if request.GET.get('q') != None else ''
        profiles = Profile.objects.all()
        kero2 = Application.objects.filter(
            Q(first_name__contains=q) |
            Q(last_name__contains=q) |
            Q(phone__contains=q) |
            Q(passport_serial__icontains=q)
        ).filter(system=3, login_create=1, building=3)
        application_create = ApplicationCreate.objects.all()
        ctx = {
            'kero2': kero2,
            'profiles': profiles,
            'application_create': application_create,
            'holat_hemis': holat_hemis,
            'holat_lms': holat_lms,
            'holat_kero': holat_kero,
            'segment': 'kero_c_arizalar',
            'holat_hemis_count': holat_hemis_count,
            'holat_lms_count': holat_lms_count,
            'holat_kero_count': holat_kero_count,

            # news
            'holat_kero3': holat_kero3,
            'holat_kero_newlogin_1':holat_kero_newlogin_1,
            'holat_kero_newlogin_3':holat_kero_newlogin_3,
            'holat_vaucher':holat_vaucher,
            'holat_kero_count3': holat_kero_count3,
            'holat_kero_newlogin_count1':holat_kero_newlogin_count1,
            'holat_kero_newlogin_count3':holat_kero_newlogin_count3,
            'holat_vaucher_count':holat_vaucher_count,

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/admin/kerio2_ariza.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))

@login_decorator 
@csrf_protect
@ensure_csrf_cookie 
def vaucher_arizalar(request):
    if request.user.admin_profile.is_admin:  # user.admin_profile.is_admin
        holat = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_count3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_newlogin_count1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1).count()
        
        holat_kero_newlogin_count3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3)

        holat_kero = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=1)
        
        holat_kero3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3)
        
        holat_kero_newlogin_3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1)
        
        holat_kero_newlogin_1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1)

        holat_vaucher_count = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2).count()

        holat_vaucher = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2)

        q = request.GET.get('q') if request.GET.get('q') != None else ''
        profiles = Profile.objects.all()
        vaucher = Application.objects.filter(
            Q(first_name__contains=q) |
            Q(last_name__contains=q) |
            Q(phone__contains=q) |
            Q(passport_serial__icontains=q)
        ).filter(login_create=2)
        application_create = ApplicationCreate.objects.all()
        ctx = {
            'vaucher': vaucher,
            'profiles': profiles,
            'application_create': application_create,
            'holat_hemis': holat_hemis,
            'holat_lms': holat_lms,
            'holat_kero': holat_kero,
            'segment': 'vaucher_arizalar',
            'holat_hemis_count': holat_hemis_count,
            'holat_lms_count': holat_lms_count,
            'holat_kero_count': holat_kero_count,

            # news
            'holat_kero3': holat_kero3,
            'holat_kero_newlogin_1':holat_kero_newlogin_1,
            'holat_kero_newlogin_3':holat_kero_newlogin_3,
            'holat_vaucher':holat_vaucher,
            'holat_kero_count3': holat_kero_count3,
            'holat_kero_newlogin_count1':holat_kero_newlogin_count1,
            'holat_kero_newlogin_count3':holat_kero_newlogin_count3,
            'holat_vaucher_count':holat_vaucher_count,

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/admin/vaucher_ariza.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))



@login_decorator
@csrf_protect
@ensure_csrf_cookie
def lms_arizalar(request):
    if request.user.admin_profile.is_admin:  # user.admin_profile.is_admin
        holat = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_count3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_newlogin_count1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1).count()
        
        holat_kero_newlogin_count3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3)

        holat_kero = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=1)
        
        holat_kero3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3)
        
        holat_kero_newlogin_3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1)
        
        holat_kero_newlogin_1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1)

        holat_vaucher_count = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2).count()

        holat_vaucher = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2)

        holat_kero = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3)

        q = request.GET.get('q') if request.GET.get('q') != None else ''
        profiles = Profile.objects.all()
        lms = Application.objects.filter(
            Q(first_name__contains=q) |
            Q(last_name__contains=q) |
            Q(phone__contains=q) |
            Q(passport_serial__icontains=q)
        ).filter(system=2, login_create=3)
        application_create = ApplicationCreate.objects.all()
        ctx = {
            'lms': lms,
            'profiles': profiles,
            'application_create': application_create,
            'holat_hemis': holat_hemis,
            'holat_lms': holat_lms,
            'holat_kero': holat_kero,
            'segment': 'lms_arizalar',
            'holat_hemis_count': holat_hemis_count,
            'holat_lms_count': holat_lms_count,
            'holat_kero_count': holat_kero_count,

            # news
            'holat_kero3': holat_kero3,
            'holat_kero_newlogin_1':holat_kero_newlogin_1,
            'holat_kero_newlogin_3':holat_kero_newlogin_3,
            'holat_vaucher':holat_vaucher,
            'holat_kero_count3': holat_kero_count3,
            'holat_kero_newlogin_count1':holat_kero_newlogin_count1,
            'holat_kero_newlogin_count3':holat_kero_newlogin_count3,
            'holat_vaucher_count':holat_vaucher_count,

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/admin/lms_ariza.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


@login_decorator
@csrf_protect
@ensure_csrf_cookie 
def Ariza_edit(request, pk):
    if request.user.admin_profile.is_admin:  # user.admin_profile.is_admin
        holat = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_count3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3).count()

        holat_kero_newlogin_count1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1).count()
        
        holat_kero_newlogin_count3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=1, login_create=3)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=2, login_create=3)

        holat_kero = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=1)
        
        holat_kero3 = Application.objects.select_related('position', 'system', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', system=3, login_create=3, building=3)
        
        holat_kero_newlogin_3 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=3, login_create=1)
        
        holat_kero_newlogin_1 = Application.objects.select_related('position', 'building', 'app_create', 'login_create').filter(
            app_create__status='yangi', building=1, login_create=1)

        holat_vaucher_count = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2).count()

        holat_vaucher = Application.objects.select_related('position', 'app_create', 'login_create').filter(app_create__status='yangi', login_create=2)

        # Application obyektini olish
        application = Application.objects.get(pk=pk)
        # ApplicationCreate obyektini olish
        application_create = ApplicationCreate.objects.get(application=application)

        # ApplicationCreateForm bilan birlashish
        form = ApplicationCreateForm(request.POST or None, instance=application_create)

        # POST so'rovi kelgan bo'lsa va forma to'g'ri kiritilgan bo'lsa
        if request.method == 'POST' and form.is_valid():
            # ApplicationCreate obyektini saqlash
            form.save()

            messages.success(request, 'Holat foydalanuvchiga yuborildi')
            return redirect('index')

        else:
            messages.error(request, form_validation_error(form))

        ctx = {
            "application": application,
            "form": form,
            'holat_hemis': holat_hemis,
            'holat_lms': holat_lms,
            'holat_kero': holat_kero,

            'holat_hemis_count': holat_hemis_count,
            'holat_lms_count': holat_lms_count,
            'holat_kero_count': holat_kero_count,

            # news
            'holat_kero3': holat_kero3,
            'holat_kero_newlogin_1':holat_kero_newlogin_1,
            'holat_kero_newlogin_3':holat_kero_newlogin_3,
            'holat_vaucher':holat_vaucher,
            'holat_kero_count3': holat_kero_count3,
            'holat_kero_newlogin_count1':holat_kero_newlogin_count1,
            'holat_kero_newlogin_count3':holat_kero_newlogin_count3,
            'holat_vaucher_count':holat_vaucher_count,

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/admin/ariza_edit.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


@login_decorator
@csrf_protect
@ensure_csrf_cookie
def fayl_tasdiq(request):
    if request.user.admin_profile.is_admin:
        fayl = Fayl.objects.all()
        return render(request, 'admins/fayl/fayl_tasdiq.html', {'fayl':fayl})



@login_decorator
@csrf_protect
@ensure_csrf_cookie
def tasdiqlash(request, fayl_id):
    fayl = get_object_or_404(Fayl, pk=fayl_id)
    tasdiqlar = FaylTasdiq.objects.filter(fayl=fayl, admin=request.user)

    if tasdiqlar.exists():
        # Foydalanuvchi faylni allaqachon tasdiqlagan
        return render(request, 'admins/fayl/fayl_already_approved.html', {'fayl': fayl})

    if request.method == 'POST':
        tasdiq_holati = request.POST.get('tasdiq_holati')
        admin = request.user

        # Fayl uchun tasdiq jadvalini yaratish
        fayl_tasdiq = FaylTasdiq.objects.create(
            fayl=fayl,
            admin=admin,
            tasdiq_holati=tasdiq_holati
        )

        # Faylga tasdiqlangan soni va holatni yangilash
        fayl.tasdiq_soni += 1
        fayl.tasdiqlangan = tasdiq_holati
        fayl.save()

        return HttpResponseRedirect(reverse('fayl_detail', args=[fayl.id]))

    return render(request, 'admins/fayl/tasdiq.html', {'fayl': fayl})


@login_decorator
@csrf_protect
@ensure_csrf_cookie
def fayl_detail(request, fayl_id):
    fayl = get_object_or_404(Fayl, pk=fayl_id)
    tasdiqlar = FaylTasdiq.objects.filter(fayl=fayl)

    return render(request, 'admins/fayl/detail.html', {'fayl': fayl, 'tasdiqlar': tasdiqlar})


@login_decorator
@csrf_protect
@ensure_csrf_cookie
def fayllar(request):
    if request.user.admin_profile.is_admin:
        fayl = Fayl.objects.all()
        return render(request, 'admins/fayl/fayllar.html', {'fayl':fayl})


@login_decorator
@csrf_protect
@ensure_csrf_cookie
def yuklash_sahifasi(request):
    if request.user.admin_profile.is_admin:
        if request.method == 'POST':
            form = FaylInputForm(request.POST, request.FILES, user=request.user)
            print(form)
            if form.is_valid():
                form.save()
                messages.success(request, 'Fayl saqlandi')
            else:
                messages.warning(request, 'Xatolik yuz berdi')
            print(form.errors)
            return redirect('files')
        else:
            form = FaylInputForm(user=request.user)
        context = {'form': form}
        return render(request, 'admins/fayl/fayl_input.html', context)

    else:
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


@login_decorator
@csrf_protect
@ensure_csrf_cookie
def edit_input(request, pk):
    if request.user.admin_profile.is_admin:
        model = Fayl.objects.get(pk=pk)

        if request.method == 'POST':
            form = FaylInputForm(request.POST, request.FILES, user=request.user, instance=model)
            if form.is_valid():
                form.save()
                messages.success(request, 'O\'zgartirish saqlandi')
            else:
                messages.warning(request, 'Xatolik yuz berdi')
            return redirect('files')
        else:
            form = FaylInputForm(user=request.user, instance=model)
        context = {
            "model": model,
            'form': form
        }
        return render(request, 'admins/fayl/fayl_input.html', context)

    else:
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


def get_authors(request):
    kafedra_id = request.GET.get('kafedra_id')
    authors = Author.objects.filter(kafedra_id=kafedra_id).values('id', 'name')
    return JsonResponse({'authors': list(authors), 'selected_authors': []})


@login_decorator
@csrf_protect
@ensure_csrf_cookie
def teacher(request):
    if request.user.admin_profile.is_admin:
        if request.method == 'POST':
            teachers = AuthorForm(request.POST, request.FILES)
            if teachers.is_valid():
                teachers.save()
                messages.success(request, 'O\'qituvchi saqlandi')
            else:
                messages.warning(request, 'Xatolik yuz berdi')
            return redirect('yuklash_sahifasi')
        else:
            teachers = AuthorForm()
        context = {'teachers': teachers}
        return render(request, 'admins/fayl/oqituvchi.html', context)

    else:
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))