from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import View
from users.models import Profile
from django.http import HttpResponse
from django.template.loader import render_to_string
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore


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
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)

        if user is not None:
            login(request, user)
            messages.success(request, f'Tizimga muvafaqiyatli kirdingiz!')
            return redirect('index')
        else:
            messages.warning(request, f'Username yoki parol xato')

    return render(request, 'registration/login.html')


def login_user(request):
    unsuccessful_attempts = request.session.get('unsuccessful_attempts', 0)

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            if unsuccessful_attempts >= 2:
                form.fields['captcha'].required = True
                if not form.cleaned_data.get('captcha', False):
                    form.add_error('captcha', 'Noto‘g‘ri captcha. Iltimos, qaytadan urinib ko‘ring.')
                    request.session['unsuccessful_attempts'] = unsuccessful_attempts + 1
                    return render(request, 'login_template.html', {'form': form})

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, password=password, username=username)
            if user is not None:
                login(request, user)
                messages.success(request, f'Tizimga muvafaqiyatli kirdingiz!')

                return redirect('application_list')
            else:
                messages.warning(request, f'Username yoki parol xato')

            request.session['unsuccessful_attempts'] = 0

            return redirect('application_list')
        else:
            request.session['unsuccessful_attempts'] = unsuccessful_attempts + 1
    else:
        form = LoginForm()

    return render(request,  'users/login.html', {'form': form})


def captcha_image(request):
    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        new_captcha_key = CaptchaStore.generate_key()
        to_json_response = {
            'key': new_captcha_key,
            'image_url': captcha_image_url(new_captcha_key),
        }
        return HttpResponse(render_to_string('users/captcha_image_ajax.html', to_json_response))
    else:
        return HttpResponse(status=400)


# def login_user(request):
#     if request.POST:
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, password=password, username=username)
#
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f'Tizimga muvafaqiyatli kirdingiz!')
#
#                 return redirect('application_list')
#             else:
#                 messages.warning(request, f'Username yoki parol xato')
#         else:
#             messages.warning(request, f'Forma noto\'g\'ri to\'ldirilgan')
#         print(form.errors)
#     else:
#         form = LoginForm()
#
#     return render(request, 'users/login.html', {'form':form})
#

@login_decorator
def logout_user(request):
    logout(request)
    return redirect("login")
