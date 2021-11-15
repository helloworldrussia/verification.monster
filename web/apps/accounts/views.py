from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.models import Accounts, Completed, Mailing, PassportFile
from referals.models import Referals
from telegram_api.app import send_message


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
        my_accounts = list()
        for completed_account in get_my_completed:
            my_accounts.append(completed_account.account_id)
        return render(request, "users/cabinet/accounts/show.tpl", {"accounts": my_accounts})

    elif show_type == "new":
        get_new_accounts = Accounts.objects.filter(status=None)
        return render(request, "users/cabinet/accounts/show.tpl", {"accounts": get_new_accounts})

    elif show_type == "completed":
        get_completed_accounts = Accounts.objects.filter(status=1)
        return render(request, "users/cabinet/accounts/show.tpl", {"accounts": get_completed_accounts})


@login_required
def detail_view(request, account_id):
    if request.method == "POST":
        select_account = Accounts.objects.get(id=account_id)
        select_account.status = 1
        select_account.save()

        new_completed = Completed.objects.create(
            registrator_id = request.user,
            account_id = select_account,
            status = "Принят",
            link = request.POST['link'],
            instruction = request.POST['instruction']
        )

        content_message_invite = f"Вашу заявку принял @{request.user.username}. \n Вы можете обращяться к нему если возникнут вопросы."
        send_message(account_id = select_account.id, text=content_message_invite)

        content_message_instructions = f"*Перейдите по ссылке:* [перейти...]({request.POST['link']}) \n*Инструкция*: \n{request.POST['instruction']}"
        send_message(account_id = select_account.id, text = content_message_instructions)

        return redirect("/accounts/view/"+str(select_account.id))


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
            try:
                get_passport_file = PassportFile.objects.get(tg_id=account_detail.tg_id)
            except:
                get_passport_file = None
            return render(request, "users/cabinet/accounts/detail.tpl", {"user":request.user, "account": account_detail, "referal_username": referal_username, "status": get_status, "passportfile": get_passport_file})
        except Exception as e:
            print(e)
            return HttpResponse("Заявки не найдено!")
    
    elif request.user.get_group() == "Регистратор":
        try:
            check_completed = Completed.objects.get(account_id = account_id)

            if check_completed.registrator_id.id == request.user.id:
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
                    try:
                        get_passport_file = PassportFile.objects.get(tg_id=account_detail.tg_id)
                    except:
                        get_passport_file = None
                    return render(request, "users/cabinet/accounts/detail.tpl", {"user":request.user, "account": account_detail, "referal_username": referal_username, "status": get_status, "passportfile": get_passport_file})
                except Exception as e:
                    print(e)
                    return HttpResponse("Заявки не найдено!")
            else:
                return redirect("/accounts/new/")
        except:
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
                try:
                    get_passport_file = PassportFile.objects.get(tg_id=account_detail.tg_id)
                except:
                    get_passport_file = None
                return render(request, "users/cabinet/accounts/detail.tpl", {"user":request.user, "account": account_detail, "referal_username": referal_username, "status": get_status, "passportfile": get_passport_file})
            except Exception as e:
                print(e)
                return HttpResponse("Заявки не найдено!")
    
    



@login_required
def delete_view(request, account_id):
    if request.user.get_group() == "Администратор":
        try:
            account_object = Accounts.objects.get(id=account_id)
            try:
                passportfile_object = PassportFile.objects.get(tg_id=account_object.tg_id).delete()
            except:
                pass
            try:
                referal_object = Referals.objects.get(to_id=account_object.tg_id).delete()
            except:
                pass
            if account_object.status == "1":
                completed_object = Completed.objects.get(account_id=account_object.id).delete()
            
            account_object.delete()
            mailing_object = Mailing.objects.get(tg_id=account_object.tg_id).delete()


        except Exception as e:
            print(e)
            return HttpResponse("Произошла ошибка!")
        
        get_all_objects = Accounts.objects.all()
        return redirect("/accounts/all")


@login_required
def take_view(request, account_id):
    return render(request, "users/cabinet/accounts/take.tpl")

@login_required
def setbalance_view(request, account_id):
    if request.method == "POST":
        account = Accounts.objects.get(id=account_id)
        account.balance = request.POST['balance']
        account.save()
        return redirect("/accounts/view/"+str(account_id))

    get_account = Accounts.objects.get(id=account_id)
    balance_account = get_account.balance
    return render(request, "users/cabinet/accounts/setbalance.tpl", {"balance_account": balance_account})