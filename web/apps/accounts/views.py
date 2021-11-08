from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.models import Accounts, Completed
from referals.models import Referals


@login_required
def all_view(request, show_type):
    if show_type == "all":
        if request.user.get_group() == "Администратор":
            get_all_objects = Accounts.objects.all()
            return render(request, "users/cabinet/accounts/show.tpl", {"accounts": get_all_objects})
        
        else: 
            return redirect("/accounts/my")

    elif show_type == "my":
        get_my_completed = Completed.objects.filter(registrator_id = request.user.id)
        return render(request, "users/cabinet/accounts/show.tpl", {"accounts": get_my_completed})

    elif show_type == "new":
        get_new_accounts = Accounts.objects.filter(status=None)
        return render(request, "users/cabinet/accounts/show.tpl", {"accounts": get_new_accounts})


@login_required
def detail_view(request, account_id):
    if request.user.get_group() == "Администратор":
        try:
            referal_username = None
            account_detail = Accounts.objects.get(id=account_id) 
            try:
                referal_object = Referals.objects.get(to_id=account_detail.tg_id)
                referal_tg_id = referal_object.from_id
                referal_account = Accounts.objects.get(tg_id=referal_tg_id)
                referal_username = referal_account.tg_username
            except:
                referal_username = "нет"
            
            get_status = Completed.objects.filter(account_id=account_id)

            return render(request, "users/cabinet/accounts/detail.tpl", {"user":request.user, "account": account_detail, "referal_username": referal_username, "status": get_status})
        except:
            return HttpResponse("Заявки не найдено!")
    
    elif request.user.get_group() == "Регистратор":
        try:
            get_account_detail = Accounts.objects.get(id=account_id, status=None)
            try:
                referal_object = Referals.objects.get(to_id=account_detail.tg_id)
                referal_tg_id = referal_object.from_id
                referal_account = Accounts.objects.get(tg_id=referal_tg_id)
                referal_username = "@"+referal_account.tg_username
            except:
                referal_username = "нет"
        except:
            return HttpResponse("Заявки не найдено")
        get_status = Completed.objects.filter(account_id=account_id)
        return render(request, "users/cabinet/accounts/detail.tpl", {"user":request.user, "account": get_account_detail, "referal_username": referal_username, "status": get_status})




@login_required
def delete_view(request, account_id):
    if request.user.get_group() == "Администратор":
        try:
            account_object = Accounts.objects.get(id=account_id).delete()
        except:
            return HttpResponse("Произошла ошибка!")
        
        get_all_objects = Accounts.objects.all()
        return redirect("/accounts/all")


@login_required
def take_view(request, account_id):
    return render(request, "users/cabinet/accounts/take.tpl")
