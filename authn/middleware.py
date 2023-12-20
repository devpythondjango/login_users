from django.shortcuts import redirect
from django.urls import resolve


class DashboardMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        path = request.path

        if user.is_authenticated and user.profile.is_admin and path == 'http://127.0.0.1:8000/dashboard/':
            return self.get_response(request)  # Foydalanuvchi admin va "/dashboard" ga kirgan bo'lsa, davom etamiz

        if user.is_authenticated and not user.profile.is_admin and path == 'http://127.0.0.1:8000/dashboard/':
            return redirect('login')  # Foydalanuvchi admin emas va "/dashboard" ga kirgan bo'lsa, login sahifasiga yo'naltiramiz

        if not user.is_authenticated and path == 'http://127.0.0.1:8000/dashboard/':
            return redirect('login')  # Foydalanuvchi autentifikatsiyadan o'tmagan bo'lsa, login sahifasiga yo'naltiramiz


        # if user.is_authenticated and hasattr(user, 'profile') and getattr(user.profile, 'is_admin', False) and path == '/dashboard':
        #     return self.get_response(request)  # Foydalanuvchi admin va "/dashboard" ga kirgan bo'lsa, davom etamiz

        # if user.is_authenticated and hasattr(user, 'profile') and not getattr(user.profile, 'is_admin', False) and path == '/dashboard':
        #     return redirect('login')  # Foydalanuvchi admin emas va "/dashboard" ga kirgan bo'lsa, login sahifasiga yo'naltiramiz

        # if not user.is_authenticated and hasattr(user, 'profile') and path == '/dashboard':
        #     return redirect('login')  # Foydalanuvchi autentifikatsiyadan o'tmagan bo'lsa, login sahifasiga yo'naltiramiz


        response = self.get_response(request)
        return response


# class DashboardMiddleware:
    # def __init__(self, get_response):
    #     self.get_response = get_response

    # def __call__(self, request):
    #     user = request.user
    #     path = request.path

    #     # Foydalanuvchi admin emas va "/dashboard" ga kirgan bo'lsa
    #     if not user.profile.is_admin and path == '/dashboard':
    #         return redirect('login_admin')  # Avvalgi sahifaga yo'naltirish

    #     response = self.get_response(request)
    #     return response