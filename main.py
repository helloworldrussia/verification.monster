"""""
v. 1
"""""

# Callback Handlers - 64 line
#


import telebot,re, urllib
import config

from models import Account, Referal, Mailing, PassportFile
from datetime import datetime

bot = telebot.TeleBot(config.token, parse_mode="Markdown")

AccountModel = None
ReferalModel = None
AuthStatus = False

"""
    Function: send_start
    Exec: cmd = /start
    NextStep: {
        not loggined = callback_handlers

    }
"""
@bot.message_handler(commands=['start'])
def send_start(message):
    
    get_account = Account().select_where('tg_id', message.from_user.id)
    if len(get_account) == 1:

        global AccountModel
        AccountModel = Account()
        AccountModel.get_object(message.from_user.id)
        
        menu_markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
        balance = telebot.types.KeyboardButton("Мой баланс")
        referal = telebot.types.KeyboardButton("Мои рефералы")
        set_passportfile = telebot.types.KeyboardButton("Загрузить фото паспорта")
        menu_markup.add(balance, referal)

        passportfile_object = PassportFile().select_where(tg_id=AccountModel.tg_id)
        if len(passportfile_object) == 0:
            menu_markup.add(set_passportfile)

        bot.send_message(message.chat.id, f"Привет _{message.from_user.first_name} {message.from_user.last_name}_!", reply_markup=menu_markup)

    else:
        AccountModel = Account(tg_id = message.chat.id,
                                tg_username =  message.chat.username
        )

        try:
            if int(message.text.split()[1]) != AccountModel.tg_id:
                global ReferalModel
                ReferalModel = Referal(from_id = message.text.split()[1])
            else:
                print("~is your tg id~")
                raise ValueError("~is your tg id~")
        except:
            print("~dont referal~")

        select_refer_register_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        referal = telebot.types.InlineKeyboardButton("Привлечь людей", callback_data="go_to_referal")
        register = telebot.types.InlineKeyboardButton("Пройти регистрацию", callback_data="yeah_get_money")
        select_refer_register_markup.add(referal, register)

        show_start_inline = bot.send_message(message.chat.id, "*Привет! Ты хочешь заработать немного денег?!* \nХочешь привлечь друзей или зарегистрироваться за деньги? ", reply_markup=select_refer_register_markup)

#   -----------------Callback Handlers-----------------

#                     After /start
#   ___________________________________________________
@bot.callback_query_handler(func=lambda call: call.data in ["yeah_get_money", "go_to_referal"])
def select_register_referal_handler(call):
    if(call.data == "yeah_get_money"):
        age_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        yes = telebot.types.InlineKeyboardButton("Да", callback_data="yeah_18")
        no = telebot.types.InlineKeyboardButton("Нет", callback_data="no_18")
        age_markup.add(yes, no)

        bot.send_message(call.message.chat.id, "Для регистрации подходят люди старше 18 лет, у которых есть при себе документ, удостоверяющий личность. (Тебе есть 18 лет?)", 
            reply_markup=age_markup
        )
#   ___________________________________________________

#                  Callback select country
#   ___________________________________________________
@bot.callback_query_handler(func=lambda call: call.data in ["Украина", "Россия", "Казахстан"])
def select_country(call):
    AccountModel.country = call.data
    label_region = bot.send_message(call.message.chat.id, "*Область:*")
    bot.register_next_step_handler(label_region, input_region)
#   ___________________________________________________

#                   Callback select where will
#                        verification
#   ___________________________________________________
@bot.callback_query_handler(func=lambda call: call.data in ["now_verification", "later_verification"])
def select_time_verification(call):
    if call.data == "now_verification":
        blank_photo = open('telegram_assets/blank.jpg', 'rb')
        bot.send_photo(call.message.chat.id, blank_photo)
        label_verification_photo = bot.send_message(call.message.chat.id, "Для подтверждения своих данных ,которые Вы предоставили  нужно приложить Фото документа на фоне переписки с ботом (где видно последнее сообщение)  как на примере выше.")
        bot.register_next_step_handler(label_verification_photo, download_verification_photo)

    else:
        bot.send_message(call.message.chat.id, "*Хорошо, ваша заявка будет создана.*\nПозже вы сможете загрузить документы в личном кабинете.")
        global AuthStatus
        AuthStatus = True
        finish_proccess(call.message)


@bot.callback_query_handler(func=lambda call: True)
def callback_handerl(call):
    if(call.data == "yeah_18"):
        select_document_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        id_passport = telebot.types.InlineKeyboardButton("ID паспорт", callback_data="have_id_pass")
        licenses = telebot.types.InlineKeyboardButton("Права пластиковые", callback_data="have_licenses")
        custom_pass = telebot.types.InlineKeyboardButton("Загранпаспорт", callback_data="have_custom_pass")
        select_document_markup.add(id_passport, licenses, custom_pass)

        bot.send_message(call.message.chat.id, "Для граждан Украины подходят ID паспорт, права пластиковые, загранпаспорт. (что у тебя есть? )", 
            reply_markup=select_document_markup
        )

    elif(call.data == "have_id_pass"):
        AccountModel.document_type = "ID карточка"
        input_credit_card(call.message)

    elif(call.data == "have_licenses"):
        AccountModel.document_type = "Права пластиковые"
        input_credit_card(call.message)

    
    elif(call.data == "have_custom_pass"):
        AccountModel.document_type = "Загранпаспорт"
        input_credit_card(call.message)


    elif(call.data == "select_payment_100"):
        AccountModel.type_payment = 100
        AccountModel.save()

        time_verification_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        now = telebot.types.InlineKeyboardButton("Сейчас", callback_data="now_verification")
        later = telebot.types.InlineKeyboardButton("Позже", callback_data="later_verification")
        time_verification_markup.add(now, later)

        bot.send_message(call.message.chat.id, "Готов сейчас пройти верефикацию с документами?\n*Ссылка на регистрицию действует 15 минут...*",
            reply_markup = time_verification_markup
        )

                

    elif(call.data == "select_payment_300"):
        AccountModel.type_payment = 300
        AccountModel.save()

        time_verification_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        now = telebot.types.InlineKeyboardButton("Сейчас", callback_data="now_verification")
        later = telebot.types.InlineKeyboardButton("Позже", callback_data="later_verification")
        time_verification_markup.add(now, later)

        bot.send_message(call.message.chat.id, "Готов сейчас пройти верефикацию с документами?\n*Ссылка на регистрицию действует 15 минут...*",
            reply_markup = time_verification_markup
        )

    elif(call.data == "back_to_main_menu"):
        menu_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        balance = telebot.types.InlineKeyboardButton("Мой баланс", callback_data="account_balance")
        referal = telebot.types.InlineKeyboardButton("Мои рефералы", callback_data="account_referals")
        menu_markup.add(balance, referal)
        
        bot.send_message(call.message.chat.id, f"Привет _{call.message.chat.first_name} {call.message.chat.last_name}_ !", reply_markup=menu_markup)

    elif(call.data == "go_to_withdraw"):
        withdraw_module(call.message)



    elif(call.data == "yeah_valid_credit_card"):
        hide_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)

        bot.send_message(call.message.chat.id, "create order to withdraw")

    elif(call.data == "no_valid_credit_card"):
        label_new_credit_card = bot.send_message(call.message.chat.id, "Введите новый номер карты:")
        bot.register_next_step_handler(label_new_credit_card, input_new_credit_card)


def download_verification_photo(message):
    if message.content_type == "document":
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        path_file = "static/tg_documents/"+str(message.chat.id)+".jpg"
        data = urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{config.token}/{file_info.file_path}', path_file)
        
        PassportFile(tg_id=message.chat.id, path=path_file).save()
        

        finish_proccess(message) 

    elif message.content_type == "photo":
        photo_id = message.photo[-1].file_id
        photo_info = bot.get_file(photo_id)
        data = urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{config.token}/{photo_info.file_path}', "documents/"+str(message.chat.id)+".jpg")
        finish_proccess(message)

def input_credit_card(message):
    label_credit = bot.send_message(message.chat.id, "*Введите свою банковскую карту для выплаты вам денег:*")
    bot.register_next_step_handler(label_credit, set_credit_card)


def set_credit_card(message):
    check_validate = re.match(config.pattern_credit_card, message.text)
    if check_validate:    
        AccountModel.credit_card = message.text
        bot.send_message(message.chat.id, "Перепишите ваши данные как в документе, который вы выбрали выше.")
        label_first_name = bot.send_message(message.chat.id, "*Имя* как в документе:")
        bot.register_next_step_handler(label_first_name, input_first_name)
    else:
        label_error = bot.send_message(message.chat.id, "_Номер карты не корректный!_\nПовторите ещё раз:")
        bot.register_next_step_handler(label_error, set_credit_card)

def input_first_name(message):
    AccountModel.first_name = message.text
    if AccountModel.document_type != "Загранпаспорт":
        label_patronymic = bot.send_message(message.chat.id, "*Отчество* как в документе:")
        bot.register_next_step_handler(label_patronymic, input_patronymic)
    else:
        AccountModel.patronymic = "не указано"
        label_last_name = bot.send_message(message.chat.id, "*Фамилия* как в документе:")
        bot.register_next_step_handler(label_last_name, input_last_name)


def input_patronymic(message):
    AccountModel.patronymic = message.text
    label_last_name = bot.send_message(message.chat.id, "*Фамилия* как в документе:")
    bot.register_next_step_handler(label_last_name, input_last_name)

def input_last_name(message):
    AccountModel.last_name = message.text

    select_country_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    ukraine = telebot.types.InlineKeyboardButton("Украина", callback_data="Украина")
    russia = telebot.types.InlineKeyboardButton("Россия", callback_data="Россия")
    kaz = telebot.types.InlineKeyboardButton("Казахстан", callback_data="Казахстан")
    select_country_markup.add(ukraine, russia, kaz)

    label_country = bot.send_message(message.chat.id, "*Страна:*", reply_markup=select_country_markup)
    bot.register_next_step_handler(label_country, input_country)

def input_country(message):
    AccountModel.country = message.text

    hide_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
   


def input_region(message):
    AccountModel.region = message.text
    label_city = bot.send_message(message.chat.id, "*Город:*")
    bot.register_next_step_handler(label_city, input_city)

def input_city(message):
    AccountModel.city = message.text
    label_address = bot.send_message(message.chat.id, "*Адресс:*")
    bot.register_next_step_handler(label_address, input_address)

def input_address(message):
    AccountModel.address = message.text
    label_datebirthday = bot.send_message(message.chat.id, "*Дата рождения.* Формат: _день-месяц-год_")
    bot.register_next_step_handler(label_datebirthday, input_datebirthday)


def input_datebirthday(message):
    try:
        datetime.strptime(message.text, "%d-%m-%Y")
        AccountModel.date_birthday = message.text

        select_payment_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        payment_100 = telebot.types.InlineKeyboardButton("100грн.", callback_data="select_payment_100")
        payment_300 = telebot.types.InlineKeyboardButton("300грн.", callback_data="select_payment_300")
        select_payment_markup.add(payment_100, payment_300)


        bot.send_message(message.chat.id, "Есть 2 варианта оплаты:\n*Сразу после регистрации - 100 грн.* \n *До 7 дней - 300грн.*",
            reply_markup=select_payment_markup
        )
        
          
    except ValueError:
        label_error = bot.send_message(message.chat.id, "*Неверный формат даты!* Повторите ещё раз.")
        bot.register_next_step_handler(label_error, input_datebirthday)


def finish_proccess(message):
    if not ReferalModel is None:
        ReferalModel.to_id = AccountModel.tg_id
        ReferalModel.save()
        Account().paid_account(ReferalModel.from_id, 100)

    check_mailing = len(Mailing().select_where(AccountModel.tg_id))
    if check_mailing == 0:
        mailing = Mailing(tg_id = AccountModel.tg_id, tg_username=AccountModel.tg_username,
                tg_chat_id = message.chat.id
            )
        mailing.save()

    bot.send_message(message.chat.id, f"Всё, готово! \nТеперь ожидайте когда вашу заявку примет наш сотрудник с инструкцией. *Перейти в меню*: /start")



@bot.message_handler(content_types=['text'])
def menu_options(message):
    if(message.text ==  "Мой баланс"):
        balance_method_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        withdraw = telebot.types.InlineKeyboardButton("Вывести", callback_data="withdraw_balance")
        change_number_card = telebot.types.InlineKeyboardButton("Изменить реквизиты", callback_data="no_valid_credit_card")
        balance_method_markup.add(withdraw, change_number_card)
        
        bot.send_message(message.chat.id, f"Ваш баланс: *{AccountModel.balance}* грн.", reply_markup=balance_method_markup)

    elif(message.text == "Мои рефералы"):
        referals = Referal().select_where(AccountModel.tg_id)

        one_hundred_payment_list = list()
        three_hundred_payment_list = list()
        for referal in referals:
            account_referal = Account().select_where('tg_id', referal['to_id'])[0]
            
            if account_referal['type_payment'] == 100:
                one_hundred_payment_list.append(account_referal)
            elif account_referal['type_payment'] == 300:
                three_hundred_payment_list.append(account_referal)
            
        
        one_hundred_payment_count = len(one_hundred_payment_list)
        three_hundred_payment_count = len(three_hundred_payment_list)
        bot.send_message(message.chat.id, f"*Ваши рефералы:*\n_Оплата 100грн.: {one_hundred_payment_count}_\n_Оплата 300грн.: {three_hundred_payment_count}_\n_Всего: {one_hundred_payment_count+three_hundred_payment_count}_")
        
        generate_referal_link = config.blank_referals+str(AccountModel.tg_id)
        bot.send_message(message.chat.id, f"Ваша реферальная ссылка:\n[{generate_referal_link}]({generate_referal_link})")

    elif(message.text == "Загрузить фото паспорта"):
        blank_photo = open('telegram_assets/blank.jpg', 'rb')
        bot.send_photo(message.chat.id, blank_photo)
        label_verification_photo = bot.send_message(message.chat.id, "Для подтверждения своих данных ,которые Вы предоставили  нужно приложить Фото документа на фоне переписки с ботом (где видно последнее сообщение)  как на примере выше.")
        bot.register_next_step_handler(label_verification_photo, download_verification_photo)
    
def select_balance_option(message):
    if(message.text == "Заказать выплату"):
        withdraw_module(message)

def withdraw_module(message):
    change_credit_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    yes = telebot.types.InlineKeyboardButton("Да", callback_data="yeah_valid_credit_card")
    no = telebot.types.InlineKeyboardButton("Нет", callback_data="no_valid_credit_card")
    change_credit_markup.add(yes, no)

    bot.send_message(message.chat.id, f"Ваши реквизиты: *{AccountModel.credit_card}* \nВерно?", reply_markup=change_credit_markup)


def input_new_credit_card(message):
    go_withdraw_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    yes = telebot.types.InlineKeyboardButton("Да", callback_data="go_to_withdraw")
    no = telebot.types.InlineKeyboardButton("Нет", callback_data="back_to_main_menu")
    go_withdraw_markup.add(yes, no)

    check_validate = re.match(config.pattern_credit_card, message.text)
    if check_validate:
        AccountModel.credit_card = message.text
        AccountModel.update()
        bot.send_message(message.chat.id, "_Ваши реквизиты успешно обновлены!_ \nЗаказать выплату на новые данные?" ,reply_markup=go_withdraw_markup)    
    else:
        label_error = bot.send_message(message.chat.id, "_Номер карты не корректный.\nПоробуйте ещё раз_")
        bot.register_next_step_handler(label_error, input_new_credit_card)

bot.polling()