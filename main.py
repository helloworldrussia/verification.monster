import telebot, config

from models import Account, Referal, Mailing
from datetime import datetime
from telebot import util

bot = telebot.TeleBot(config.token, parse_mode="Markdown")
bot.worker_pool = util.ThreadPool(num_threads=8)

AccountModel = None
ReferalModel = None

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
        menu_markup.add(balance, referal)

        bot.send_message(message.chat.id, f"Привет _{message.from_user.first_name} {message.from_user.last_name}_!", reply_markup=menu_markup)

    else:
        AccountModel = Account(tg_id = message.chat.id,
                                tg_username =  message.chat.username
        )

        try:
            global ReferalModel
            ReferalModel = Referal(from_id = message.text.split()[1])
        except:
            print("~dont referal~")

        chat_id = message.chat.id
        start_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        yes = telebot.types.InlineKeyboardButton("Да", callback_data='yeah_get_money')
        no = telebot.types.InlineKeyboardButton("Нет", callback_data="2")
        start_markup.add(yes, no)

        show_start_inline = bot.send_message(message.chat.id, "Привет! Ты хочешь заработать немного денег?! (300 грн)", reply_markup=start_markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if(call.data == "yeah_get_money"):
        age_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        yes = telebot.types.InlineKeyboardButton("Да", callback_data="yeah_18")
        no = telebot.types.InlineKeyboardButton("Нет", callback_data="no_18")
        age_markup.add(yes, no)

        bot.send_message(call.message.chat.id, "Для регистрации подходят люди старше 18 лет, у которых есть при себе документ, удостоверяющий личность. (Тебе есть 18 лет?)", 
            reply_markup=age_markup
        )




    elif(call.data == "yeah_18"):
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
        finish_proccess(call.message)

    elif(call.data == "select_payment_300"):
        AccountModel.type_payment = 300
        AccountModel.save()
        finish_proccess(call.message)


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

        bot.send_message(call.message.chat.id, "create order to withdraw", reply_markup=hide_keyboard)

    elif(call.data == "no_valid_credit_card"):
        hide_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
        label_new_credit_card = bot.send_message(call.message.chat.id, "Введите новый номер карты:", reply_markup=hide_keyboard)
        bot.register_next_step_handler(label_new_credit_card, input_new_credit_card)


def input_credit_card(message):
    label_credit = bot.send_message(message.chat.id, "*Введите свою банковскую карту для выплаты вам денег.*")
    bot.register_next_step_handler(label_credit, set_credit_card)


def set_credit_card(message):
    AccountModel.credit_card = message.text
    bot.send_message(message.chat.id, "Перепишите ваши данные как в документе, который вы выбрали выше.")
    label_first_name = bot.send_message(message.chat.id, "*Имя:*")
    bot.register_next_step_handler(label_first_name, input_first_name)

def input_first_name(message):
    AccountModel.first_name = message.text
    if AccountModel.document_type != "Загранпаспорт":
        label_patronymic = bot.send_message(message.chat.id, "*Отчество:*")
        bot.register_next_step_handler(label_patronymic, input_patronymic)
    else:
        AccountModel.patronymic = "не указано"
        label_last_name = bot.send_message(message.chat.id, "*Фамилия:*")
        bot.register_next_step_handler(label_last_name, input_last_name)


def input_patronymic(message):
    AccountModel.patronymic = message.text
    label_last_name = bot.send_message(message.chat.id, "*Фамилия:*")
    bot.register_next_step_handler(label_last_name, input_last_name)

def input_last_name(message):
    AccountModel.last_name = message.text

    select_country_markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    ukraine = telebot.types.KeyboardButton("Украина")
    russia = telebot.types.KeyboardButton("Россия")
    kaz = telebot.types.KeyboardButton("Казахстан")
    select_country_markup.add(ukraine, russia, kaz)


    label_country = bot.send_message(message.chat.id, "*Страна:*", reply_markup=select_country_markup)
    bot.register_next_step_handler(label_country, input_country)

def input_country(message):
    AccountModel.country = message.text

    hide_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
    label_region = bot.send_message(message.chat.id, "*Область:*", reply_markup=hide_keyboard)
    bot.register_next_step_handler(label_region, input_region)


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


        type_payment_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        first_type = telebot.types.InlineKeyboardButton("100грн.", callback_data="select_payment_100")
        second_type = telebot.types.InlineKeyboardButton("300грн.", callback_data="select_payment_300")
        type_payment_markup.add(first_type, second_type)

        bot.send_message(message.chat.id, "Есть 2 варианта оплаты:\n *Сразу после регистрации _100 грн._* \n *В течении 3-4 дней _300грн._* \n \n _Сделай выбор:_",
            reply_markup=type_payment_markup
         )

   
    except ValueError:
        label_error = bot.send_message(message.chat.id, "*Неверный формат даты!* Повторите ещё раз.")
        bot.register_next_step_handler(label_error, input_datebirthday)


def finish_proccess(message):
    if not ReferalModel is None:
        ReferalModel.to_id = AccountModel.tg_id
        ReferalModel.save()
        Account().paid_account(ReferalModel.from_id, 100)

    mailing = Mailing(tg_id = AccountModel.tg_id, tg_username=AccountModel.tg_username,
            tg_chat_id = message.chat.id
        )
    mailing.save()

    bot.send_message(message.chat.id, f"Всё, готово! \nТеперь ожидайте когда вашу заявку примет наш сотрудник с инструкцией. *Перейти в меню*: /start")

@bot.message_handler(content_types=['text'])
def menu_options(message):
    if(message.text ==  "Мой баланс"):
        hide_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, f"Ваш баланс: *{AccountModel.balance}* грн.", reply_markup=hide_keyboard)

        balance_options = telebot.types.ReplyKeyboardMarkup(row_width=1)
        withdraw = telebot.types.KeyboardButton("Заказать выплату")
        balance_options.add(withdraw)

        balance_label_select = bot.send_message(message.chat.id, "Действия", reply_markup=balance_options)
        bot.register_next_step_handler(balance_label_select, select_balance_option)

    elif(message.text == "Мои рефералы"):
        referals = Referal().select_where(AccountModel.tg_id)
        print(referals)
        for referal in referals:
            account_referal = Account().select_where('tg_id', referal['to_id'])[0]
            bot.send_message(message.chat.id, f"_{account_referal['first_name']}_\nНик: {account_referal['tg_username']}\nОплата: {account_referal['type_payment']}")


        generate_referal_link = config.blank_referals+str(AccountModel.tg_id)
        bot.send_message(message.chat.id, f"Ваша реферальная ссылка:\n[{generate_referal_link}]({generate_referal_link})")

    
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


    AccountModel.credit_card = message.text
    AccountModel.update()
    bot.send_message(message.chat.id, "_Ваши реквизиты успешно обновлены!_ \nЗаказать выплату на новые данные?" ,reply_markup=go_withdraw_markup)    


def API_send_message(message="Test"):
    bot.send_message(447774527, message)

bot.polling()