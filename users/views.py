from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, ProfileForm, form_validation_error
from django.contrib import messages
from django.views import View
from .models import Profile
from .services import get_profile


def login_decorator(func):
    return login_required(func, login_url='login')


def home(request):
    return render(request, 'index.html')


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


def login_user(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            messages.success(request, f'Tizimga muvafaqiyatli kirdingiz!')
            return redirect("profile")

    return render(request, 'users/login.html')


@login_decorator
def logout_user(request):
    logout(request)
    return redirect("login")


@login_decorator
def profile(request):
    return render(request, 'admins/index.html')


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