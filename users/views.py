from django.shortcuts import render, redirect
from authn.forms import form_validation_error
from authn.views import login_decorator
from .forms import ApplicationForm, ProfileForm
from django.contrib import messages
from .models import Application, ApplicationCreate, Profile


def home(request):
    return render(request, 'layouts/index.html')


@login_decorator
def profile_view(request):
    if request.user.user_profile.is_users:  # user.user_profile.is_users
        user_profile, __ = Profile.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                user_profile = form.save()
                user_profile.user.first_name = form.cleaned_data.get('first_name')
                user_profile.user.last_name = form.cleaned_data.get('last_name')
                user_profile.user.email = form.cleaned_data.get('email')
                user_profile.user.save()

                messages.success(request, 'Profil muvaffaqiyatli saqlandi')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                messages.error(request, form_validation_error(form))
            print(form.errors)
            return redirect('user_profile')

        context = {'user_profile': user_profile, 'segment': 'user_profile'}
        return render(request, 'users/profile.html', context)
    else:
        messages.warning(request, 'Sizda user ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect('login')


@login_decorator
def application_create(request):
    if request.user.user_profile.is_users:  # user.user_profile.is_users
        if request.method == 'POST':
            forms = ApplicationForm(request.POST, request.FILES, user=request.user)
            if forms.is_valid():
                application_instance = forms.save()
                application_create_instance = ApplicationCreate.objects.create(
                    user=request.user,
                    application=application_instance,
                )

                messages.success(request, 'Arizangiz muvofiqiyatli adminga yuborildi')
                print(forms.errors)
            else:
                print(forms.errors)
                messages.error(request, form_validation_error(forms))
            print(forms.errors)
            return redirect('application_list')
        else:
            forms = ApplicationForm(user=request.user)
        context = {'forms': forms, 'segment': 'application_create'}

        return render(request, 'users/form.html', context=context)

    else:
        messages.warning(request, 'Sizda user ruxsati yo\'q.')
        return redirect('login')


@login_decorator
def application_list(request):
    if request.user.user_profile.is_users:  # user.user_profile.is_users
        applications = Application.objects.all()
        applications_create = ApplicationCreate.objects.all()
        context = {'applications': applications, 'applications_create': applications_create,
                   'segment': 'application_list'}
        return render(request, 'users/list.html', context=context)

    else:
        messages.warning(request, 'Sizda user ruxsati yo\'q.')
        return redirect('login')


@login_decorator
def application_views(request, pk):
    if request.user.user_profile.is_users:  # user.user_profile.is_users
        application = Application.objects.get(pk=pk)
        create = ApplicationCreate.objects.get(pk=pk)
        ctx = {'application': application, 'create': create}
        return render(request, 'users/view.html', ctx)

    else:
        messages.warning(request, 'Sizda user ruxsati yo\'q.')
        return redirect('login')
