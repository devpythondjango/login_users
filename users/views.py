from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, ProfileForm, form_validation_error, ApplicationForm, StudentForm, TeacherForm, \
    BolimForm, HemisForm, KerocontrolForm, LmsForm
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from .models import Profile, Application, Position, System, Student, Teacher, Bolim, ApplicationCreate
from django.http import HttpResponse


def login_decorator(func):
    return login_required(func, login_url='login')


def home(request):
    return render(request, 'layouts/index.html')


@login_decorator
def dashboard(request):
    return render(request, 'users/dashboard.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} foydalanuvchi yaratildi')

            return redirect(to='login')

        return render(request, 'users/register.html', {'form': form})


def login_admin(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            if user.profile.is_admin:
                return redirect('admins')

    return render(request, 'users/login.html')


def login_user(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            messages.success(request, f'Tizimga muvafaqiyatli kirdingiz!')

            return redirect('dashboard')

    return render(request, 'users/login.html')


@login_decorator
def logout_user(request):
    logout(request)
    return redirect("login")


@login_decorator
def admins(request):
    form = Profile.objects.all()
    messages.success(request, f'Tizimga muvafaqiyatli kirdingiz!')

    return render(request, 'admins/index.html', {'form': form})


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile_user'}
        return render(request, 'users/profile.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.user.save()
            profile.save()

            messages.success(request, 'Profil muvaffaqiyatli saqlandi')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('profile_user')


@login_decorator
def application_create(request):
    students = StudentForm(request.POST)
    teachers = TeacherForm(request.POST)
    bolims = BolimForm(request.POST)
    hemis = HemisForm(request.POST)
    kerocontrol = KerocontrolForm(request.POST)
    lms = LmsForm(request.POST)

    appli, __ = Application.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        forms = ApplicationForm(request.POST, request.FILES, instance=appli)
        print(forms.errors)
        if forms.is_valid() or students.is_valid() or teachers.is_valid() or bolims.is_valid() or hemis.is_valid() or kerocontrol.is_valid() or lms.is_valid():
            user_data = forms.cleaned_data.get('user')
            if user_data is not None:
                appli, created = Application.objects.get_or_create(user=user_data)
                appli = forms.save(commit=False)
                appli.user.first_name = user_data.first_name
                appli.user.last_name = user_data.last_name
                appli.user.email = user_data.email
                appli.user.save()
                appli.save()
            forms.save()
            application_create = ApplicationCreate.objects.create(
                user=request.user,
                application=forms.save(commit=False),
            )
            students.save()
            teachers.save()
            bolims.save()
            hemis.save()
            kerocontrol.save()
            lms.save()

            application_create.application = appli  # O'zgaruvchini yangilaymiz
            application_create.save()

            messages.success(request, 'Arizangiz muvofiqiyatli adminga yuborildi')
        else:
            messages.error(request, form_validation_error(forms))

        return redirect('application_create')
    else:
        forms = ApplicationForm()
        students = StudentForm()
        teachers = TeacherForm()
        bolims = BolimForm()
    context = {'appli': appli, 'segment': 'application_create', 'forms': forms, 'students': students,
               'teachers': teachers, 'bolims': bolims, 'hemis': hemis, 'kero': kerocontrol, 'lms': lms}
    return render(request, 'users/form.html', context=context)


@login_decorator
def application_list(request):
    profiles = Profile.objects.all()
    applications = Application.objects.all()
    application_create = ApplicationCreate.objects.all()
    context = {'applications': applications, 'application_create': application_create, 'profiles': profiles}
    return render(request, 'users/list.html', context=context)

# @login_required
# def profilepage(request):
#     profile = request.user.profile
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profil ma\'lumotlaringiz saqlandi.')
#             return redirect('profile')
#
#     else:
#         form = ProfileForm(instance=profile)
#
#     return render(request, 'admins/profile.html', {'form': form, 'profile': profile})
