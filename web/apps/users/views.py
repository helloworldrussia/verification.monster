from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from django.shortcuts import render, redirect

from users.models import User
from accounts.models import Accounts

#from main import API_send_message

class LoginView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/user")
        else:
            return render(request, "users/login.tpl")


class CabinetView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    redirect_field_name = None
    
    def get(self, request):
        if request.user.get_group() == "Администратор":
            all_accounts_count = len(Accounts.objects.all())
            completed_accounts_count = len(Accounts.objects.filter(status="1"))
            all_users_count = len(User.objects.all())

            return render(request, "users/cabinet/index.tpl", {"user": request.user, 
                "all_accounts_count":all_accounts_count, 
                "completed_accounts_count": completed_accounts_count,
                "all_users_count": all_users_count
                 })
        else:
            
            return render(request, "users/cabinet/index.tpl")


class ListView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    redirect_field_name = None
    template_name = "users/cabinet/show_all.tpl"

    def get(self, request):
        if request.user.get_group() == "Администратор":
            get_all_users = User.objects.all()
            return render(request, self.template_name, {"users": get_all_users})


class AddView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    redirect_field_name = None
    template_name = "users/cabinet/add_user.tpl"

    def get(self, request):
        if request.user.get_group() == "Администратор":
            return render(request, self.template_name)