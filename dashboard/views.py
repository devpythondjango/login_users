from django.shortcuts import render, redirect
from authn.forms import form_validation_error
from django.contrib import messages
from users.models import Profile, Application, ApplicationCreate
from authn.views import login_decorator
from .forms import ApplicationCreateForm, AdminProfileForm
from .models import AdminProfile
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone


@login_decorator
def admin_profile_view(request):
    if request.user.admin_profile.is_admin:
        holat = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2)

        holat_kero = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3)

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

            'holat_hemis_count': holat_hemis_count,
            'holat_lms_count': holat_lms_count,
            'holat_kero_count': holat_kero_count,

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/profile.html', context)

    else:
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


@login_decorator
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

        holat = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2)

        holat_kero = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3)

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

        hemis_foiz_formatted = "{:.2f}%".format(hemis_foiz)
        kero_foiz_formatted = "{:.2f}%".format(kero_foiz)
        lms_foiz_formatted = "{:.2f}%".format(lms_foiz)
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
        }
        return render(request, 'admins/index.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


@login_decorator
def hemis_arizalar(request):
    if request.user.admin_profile.is_admin:  # user.admin_profile.is_admin
        holat = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2)

        holat_kero = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3)

        q = request.GET.get('q') if request.GET.get('q') != None else ''
        profiles = Profile.objects.all()
        hemis = Application.objects.filter(
            Q(first_name__contains=q) |
            Q(last_name__contains=q) |
            Q(phone__contains=q) |
            Q(passport_serial__icontains=q)
        ).filter(system=1)
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

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/hemis_arizalar.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


@login_decorator
def kero_arizalar(request):
    if request.user.admin_profile.is_admin:  # user.admin_profile.is_admin
        holat = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2)

        holat_kero = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3)

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
            'segment': 'kero_arizalar',
            'holat_hemis_count': holat_hemis_count,
            'holat_lms_count': holat_lms_count,
            'holat_kero_count': holat_kero_count,

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/kero_arizalar.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


@login_decorator
def lms_arizalar(request):
    if request.user.admin_profile.is_admin:  # user.admin_profile.is_admin
        holat = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2)

        holat_kero = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3)

        q = request.GET.get('q') if request.GET.get('q') != None else ''
        profiles = Profile.objects.all()
        lms = Application.objects.filter(
            Q(first_name__contains=q) |
            Q(last_name__contains=q) |
            Q(phone__contains=q) |
            Q(passport_serial__icontains=q)
        ).filter(system=2)
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

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/lms_arizalar.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))


@login_decorator
def Ariza_edit(request, pk):
    if request.user.admin_profile.is_admin:  # user.admin_profile.is_admin
        holat = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi')
        holat_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi').count()

        holat_hemis_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1).count()

        holat_lms_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2).count()

        holat_kero_count = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3).count()

        holat_hemis = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=1)

        holat_lms = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=2)

        holat_kero = Application.objects.select_related('position', 'system', 'app_create').filter(
            app_create__status='yangi', system=3)

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

            'holat': holat,
            'holat_count': holat_count,
        }
        return render(request, 'admins/ariza_edit.html', ctx)

    else:
        # Agar foydalanuvchi admin emas bo'lsa, xabarnoma chiqariladi va bosh sahifaga yo'naltiriladi
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect(reverse('home'))
