from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from django.core.files.storage import FileSystemStorage

from accounts.models import Accounts, PassportFile, Mailing, DropAccount

class CreateView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    redirect_field_name = None
    template_name = "users/cabinet/drop/create.tpl"

    def post(self, request):
        if request.user.get_group() == "Администратор" or request.user.get_group() == "Дроповод":
            new_account = Accounts.objects.create(
                tg_id = None,
                tg_username = request.POST['tg_username'],
                first_name = request.POST['first_name'],
                patronymic = request.POST['patronymic'],
                last_name = request.POST['last_name'],
                country = request.POST['country'],
                region = request.POST['region'],
                city = request.POST['city'],
                address = request.POST['address'],
                date_birthday = request.POST['birthday'],
                document_type = request.POST['document_type'],
                credit_card = request.POST['credit_card'],
                balance = 0,
                type_payment = request.POST['type_payment'],
                status = "drop"
            )

            upload_photo = request.FILES['passport_photo']
            fss = FileSystemStorage()
            file = fss.save("static/tg_documents/"+str(new_account.id)+".jpg", upload_photo)
            file_url = fss.url(file)

            set_passport_file = PassportFile.objects.create(tg_id=new_account.id, path="static/tg_documents/"+str(new_account.id)+".jpg")
            set_mailing = Mailing.objects.create(tg_id=new_account.id, tg_username = request.POST['tg_username'], tg_chat_id=-1)
            set_dropaccount = DropAccount.objects.create(account_id=new_account.id, drop_user=request.user)
            return redirect("/user")

        else:
            return redirect("/user")
