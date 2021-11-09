from django.db import models
from users.models import User

# Create your models here.

class Accounts(models.Model):
    id = models.AutoField(primary_key=True)
    tg_id = models.IntegerField(blank=True, null=True)
    tg_username = models.TextField(blank=True, null=True)  
    first_name = models.TextField(blank=True, null=True)  # This field type is a guess.
    patronymic = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)  # This field type is a guess.
    region = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_birthday = models.TextField(blank=True, null=True)
    document_type = models.TextField(blank=True, null=True)
    credit_card = models.IntegerField(blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    type_payment = models.IntegerField(blank=True, null=True)
    status = models.TextField(default=None)

    class Meta:
        managed = False
        db_table = 'accounts'


class Completed(models.Model):
    id = models.AutoField(primary_key=True)
    registrator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    link = models.CharField(max_length=50)
    instruction = models.TextField()

    def get_registrator_username(self):
        return "@"+User.objects.get(id=self.registrator_id.id).username


class Mailing(models.Model):
    id = models.AutoField(primary_key=True)
    tg_id = models.IntegerField()
    tg_username = models.IntegerField()
    tg_chat_id = models.IntegerField()