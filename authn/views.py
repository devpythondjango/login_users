from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import View
from users.models import Profile
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.template import loader
from django.http import HttpResponse
from django import template


def login_decorator(func):
    return login_required(func, login_url='login')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()

            profile, _ = Profile.objects.get_or_create(user=user)

            profile.avatar = form.cleaned_data.get('avatar')
            profile.back_avatar = form.cleaned_data.get('back_avatar')
            profile.birthday = form.cleaned_data.get('birthday')
            profile.passport_serial = form.cleaned_data.get('passport_serial')
            profile.phone = form.cleaned_data.get('phone')
            profile.gender = form.cleaned_data.get('gender')
            profile.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} foydalanuvchi yaratildi')

            return redirect(to='login')

        return render(request, 'users/register.html', {'form': form})


def login_admin(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            captcha = form.cleaned_data.get('captcha', None)
            user = authenticate(request, password=password, username=username, captcha=captcha)

            if user.admin_profile.is_admin:
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Tizimga muvafaqiyatli kirdingiz!')
                    return redirect('index')
                else:
                    messages.warning(request, f'Username yoki parol xato')
        else:
            messages.warning(request, f'Forma noto\'g\'ri to\'ldirilgan')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def login_user(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            captcha = form.cleaned_data.get('captcha', None)
            user = authenticate(request, password=password, username=username, captcha=captcha)
            if user.user_profile.is_users:
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Tizimga muvafaqiyatli kirdingiz!')

                    return redirect('application_list')
                else:
                    messages.warning(request, f'Username yoki parol xato')

        else:
            messages.warning(request, f'Forma noto\'g\'ri to\'ldirilgan')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_decorator
def logout_user(request):
    logout(request)
    return redirect("login")


class YourCustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/your_custom_password_reset_email_template.html'

