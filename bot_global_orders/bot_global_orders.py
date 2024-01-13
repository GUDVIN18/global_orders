from datetime import datetime
import schedule
import telebot
from pycbrf import ExchangeRates
import random
import time
#import config
import requests
from telebot import types
from bs4 import BeautifulSoup
import re
from flask import Flask
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from telegram import ReplyKeyboardMarkup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


import os, sys
activate_this = '/home/w0461585/python/bin/activate_this.py'
with open(activate_this) as f:
     exec(f.read(), {'__file__': activate_this})


bot = telebot.TeleBot('6890983450:AAFESskiGVms7kW_ykM0TNndQ0dsewnrhXM')




def button_switch():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn2 = telebot.types.KeyboardButton('📈 Курс')
    item3 = telebot.types.KeyboardButton("💴 Расчитать стоимость")
    item5 = telebot.types.KeyboardButton("📦 Отследить заказ")
    item6 = telebot.types.KeyboardButton("📞 Обратная связь")
    item7 = telebot.types.KeyboardButton("ℹ️ FAQ")
    markup.add(itembtn2,item5, item3, item6, item7)
    return markup


def parcer_cny():
    start_time = time.time()
    url = 'https://www.tinkoff.ru/invest/currencies/CNYRUB/'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            price_cny = soup.find('span', class_="Money-module__money_p_VHJ").text
            price_cny = re.sub(r'[^\d.,]', '', price_cny)
            price_cny = round(float(price_cny.replace(',', '.')), 2)
            price_cny = round(price_cny + float(0.6 + 0.3), 3)
        except AttributeError:
             price_cny = 'Ошибка при получении курса!'
        print('CNY Tinkoff биржа ', price_cny)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f'Время выполнения : {execution_time} сек')   

        return price_cny





def category_orders():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Одежда", callback_data="button1"))
    markup.add(types.InlineKeyboardButton("Обувь", callback_data="button2"))
    markup.add(types.InlineKeyboardButton("Акссесуары", callback_data="button3"))
    markup.add(types.InlineKeyboardButton("Закрыть", callback_data="button4"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "button1":
        new_message = '<b>Отпарвьте стоимость товара в ¥</b>'
        possition = '<b>Одежда</b>'
        # Создайте пустую встроенную клавиатуру
        empty_keyboard = types.InlineKeyboardMarkup()
        bot.edit_message_text(text=possition, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=empty_keyboard, parse_mode='html')
        video_file = open('/home/w0461585/domains/my.matrium.ru/tgbot/bot_global_orders/video.mp4', 'rb')
        bot.send_video(chat_id=call.message.chat.id, video=video_file, width=100, height=100)

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        item13 = telebot.types.KeyboardButton('Назад')
        markup.add(item13)
        button1 = bot.send_message(chat_id=call.message.chat.id, text=new_message, parse_mode='html', reply_markup=markup)

        bot.register_next_step_handler(button1, clothing_calculation)
        # if button1 == 'Назад':



    elif call.data == "button2":
        bot.answer_callback_query(call.id, "Вы нажали на Кнопку 2")
    elif call.data == "button3":
        bot.answer_callback_query(call.id, "Вы нажали на Кнопку 3")
    elif call.data == "button4":
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=False)




@bot.message_handler(commands=['start'])
def start(message):
    chat_member = bot.get_chat_member('@GlobalOrders_chanal', message.chat.id)
    is_subscribed = chat_member.status in ['member', 'administrator', 'creator']
    if is_subscribed:
        markupes = button_switch()
        bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЗаинтересовались покупкой в нашем магазине? Бот поможет рассчитать стоимость товара по актуальному курсу!".format(message.from_user, bot.get_me()),
            parse_mode='html', reply_markup=markupes)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        item3 = types.InlineKeyboardButton("Подписаться", url='https://t.me/GlobalOrders_chanal')

        markup.add(item3)
        bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nДля пользования ботом вам необходимо быть подписчиком нашего канала!".format(message.from_user, bot.get_me()),
            parse_mode='html', reply_markup=markup)

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtn2 = telebot.types.KeyboardButton('Готово!')
        markup.add(itembtn2)
        time.sleep(2)
        bot.send_message(message.chat.id, "Нажмите на Готово, как все сделаете".format(message.from_user, bot.get_me()),
            parse_mode='html', reply_markup=markup)






@bot.message_handler(content_types=['text'])
def message(message):
    if message.chat.type == 'private':
        if message.text == 'Готово!':
            is_subscribed = bot.get_chat_member('@GlobalOrders_chanal', message.chat.id).status in ['member', 'administrator', 'creator']
            if is_subscribed is True:
                    markup = button_switch()
                    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЗаинтересовались покупкой в нашем магазине? Бот поможет рассчитать стоимость товара по актуальному курсу!".format(message.from_user, bot.get_me()),
                        parse_mode='html', reply_markup=markup)


            else:
                markup = types.InlineKeyboardMarkup(row_width=2)
                item3 = types.InlineKeyboardButton("Подписаться", url='https://t.me/GlobalOrders_chanal')
                markup.add(item3)
                # bot.send_message(message.chat.id, "ХЕР!".format(message.from_user, bot.get_me()),
                #     parse_mode='html', reply_markup=markup)


        is_subscribed = bot.get_chat_member('@GlobalOrders_chanal', message.chat.id).status in ['member', 'administrator', 'creator']
        if is_subscribed is True:
            if message.text == '💴 Расчитать стоимость':
                price = parcer_cny()
                print(round((price), 2), 'Расчет.', 'Команда от: {0.first_name} {0.last_name}. id: {0.username} '.format(message.from_user, bot.get_me()))

                markup = category_orders()
                # Отправьте текст и клавиатуру
                bot.send_message(message.chat.id, '<b>🛍️ Выберите категорию товара: </b>', parse_mode='html' , reply_markup=markup)

            elif message.text == '📈 Курс':
                    
                    price = parcer_cny()

                    print(price, 'Курс.', 'Команда от: {0.first_name} {0.last_name}. id: {0.username} '.format(message.from_user, bot.get_me()))
                    bot.send_message(message.chat.id, f'Курс юаня на сегодня: {round((price), 2)}')

            elif message.text == '📦 Отследить заказ':
                    numbers_order = bot.send_message(message.chat.id, 'Введите <b>номер</b> вашего заказа.', parse_mode='html')
                    print('Отследить заказ.', 'Команда от: {0.first_name} {0.last_name}. id: {0.username} '.format(message.from_user, bot.get_me()))
                    bot.register_next_step_handler(numbers_order, numbers_order_tracking)




            elif message.text == '📞 Обратная связь':
                    feedback = bot.send_message(message.chat.id, 'Остались вопросы? Напиши нам!')
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    back_button = types.KeyboardButton('Назад')
                    markup.add(back_button)
                    bot.send_message(chat_id=message.chat.id, text="Нажмите кнопку 'Назад', если хотите вернуться.", reply_markup=markup)
                    bot.register_next_step_handler(feedback, feedback_send)
                    print('Обратная связь.', 'Команда от: {0.first_name} {0.last_name}. id: {0.username} '.format(message.from_user, bot.get_me()))



            elif message.text == 'Назад':
                markup = button_switch()
                bot.send_message(message.chat.id, "Возвращаю...".format(message.from_user, bot.get_me()),
                    parse_mode='html', reply_markup=markup)

                print('Назад', 'Команда от: {0.first_name} {0.last_name}. id: {0.username} '.format(message.from_user, bot.get_me()))


            elif message.text == 'ℹ️ FAQ':
                text_html = '''
❗️<b>Ответы на часто задаваемые вопросы</b>❗️

- <b><a href="http://example.com">Всё о доставке.</a></b>
- <b><a href="http://example.com">В чем различия синий и черной кнопки на Poizon?</a></b>
- <b><a href="http://example.com">Что делать, если мне пришёл неоригинальный товар?</a></b>

- ✨<b><a href="https://t.me/+LQ8zOoZSnLpkMmFi">Отзывы</a></b>✨
            '''
                bot.send_message(chat_id=message.chat.id, text=text_html, parse_mode='html')

            elif message.text == 'Готово!':
                print('fake_error', 'Команда от: {0.first_name} {0.last_name}. id: {0.username} '.format(message.from_user, bot.get_me()))


            else:
                    bot.send_message(message.chat.id, '''Я не знаю что ответить 😢
Нажмите <b>/start</b>''', parse_mode='html')
        else:
            markup = types.InlineKeyboardMarkup(row_width=2)
            item3 = types.InlineKeyboardButton("Подписаться", url='t.me/GlobalOrders_chanal')

            markup.add(item3)
            bot.send_message(message.chat.id, "Для пользования ботом вам необходимо быть подписчиком нашего канала!".format(message.from_user, bot.get_me()),
                parse_mode='html', reply_markup=markup)

            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            itembtn2 = telebot.types.KeyboardButton('Готово!')
            markup.add(itembtn2)
            time.sleep(2)
            bot.send_message(message.chat.id, "Нажмите на Готово, как все сделаете".format(message.from_user, bot.get_me()),
                parse_mode='html', reply_markup=markup)




@bot.message_handler(commands=['return'])
def clothing_calculation(message):
    input_sum = message.text
    if input_sum == 'Назад':
        markup_oll = button_switch()
        bot.send_message(message.chat.id, text='Возвращаю...', reply_markup=markup_oll)
    else:
        if message.text.isdigit():
            input_sum = int(message.text)
            curce = parcer_cny()

            if input_sum  >= 100000000 or input_sum <= 10:
                print("Слишком много")
                bot.send_message(message.chat.id, f'Не допустимое значение!')
            else:
                if input_sum <= 3399:
                        m = round((input_sum *(curce)+1500))
                        bot.send_message(message.chat.id, f'''✈️ <b>Итоговая стоимость без доставки {m} руб.</b>
- ({curce} * {input_sum}) + 500 + 1000
- (Курс * цена в юанях) + доставка до склада в Китае + комиссия сервиса                             
''', parse_mode='html')
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        item3 = types.InlineKeyboardButton("Связаться", url='https://t.me/GlobalOrders_chanal')
                        markup.add(item3)
                        bot.send_message(message.chat.id, f'Для расчета стоимости доставки и оформления заказа, свяжитесь с менеджером.', reply_markup=markup)

                        print(message.text)

                elif input_sum >= 3400:
                        m = (input_sum * (curce) + 500)
                        last_price = round((m + (m/100*7)))
                        bot.send_message(message.chat.id, f'''
✈️ <b>Итоговая стоимость без доставки {last_price} руб.</b>
- ({curce} * {input_sum}) + 500 + 7%
- (Курс * цена в юанях) + доставка до склада в Китае + комиссия сервиса                             
''', parse_mode='html')
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        item3 = types.InlineKeyboardButton("Связаться", url='https://t.me/GlobalOrders_chanal')
                        markup.add(item3)
                        bot.send_message(message.chat.id, f'Для расчета стоимости доставки и оформления заказа, свяжитесь с менеджером.', reply_markup=markup)

                        print(message.text)

        else:
            bot.reply_to(message, f'Введите только число!')


def feedback_send(message):
    if message.text == 'Назад':
        markup = button_switch()
        bot.send_message(message.chat.id, "Возвращаю...".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)
    else:
        feedback_sms = str(message.text)
        print(f'Пользователь оставил сообщение: {feedback_sms}')
        user_id = message.from_user.id
        username = message.from_user.username # Получаем id отправителя сообщения
        bot.send_message(message.chat.id, '''Ваше обращение успешно получено! Ожидайте, в скором времени менеджер с вами свяжется.''')
        chat_id = '-1002114420582'  # Здесь нужно указать ID пользователя, которому будут пересылаться сообщения
        bot.send_message(chat_id, f'Сообщение от пользователя @{username} (ID: {user_id}): {feedback_sms}')  # Пересылаем текст сообщения





def numbers_order_tracking(message):
    start_time = time.time()
    txt = message.text
    # Подключение к Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/w0461585/domains/my.matrium.ru/tgbot/bot_global_orders/globalorders-a5541fea450a.json', scope)
    gc = gspread.authorize(credentials)

    # Откройте вашу таблицу по имени
    spreadsheet = gc.open('Orders Global Orders')

    # Выберите лист по имени или индексу
    worksheet = spreadsheet.get_worksheet(0)
    print(worksheet)

    # Чтение всех значений из 1 столбца
    column_values_1 = worksheet.col_values(1)
    column_values_2 = worksheet.col_values(2)
    print('номера', column_values_1,
          'статусы', column_values_2)


    if txt in column_values_1:
        index = column_values_1.index(txt) + 1  # индекс + 1 равен номеру строки
        status = worksheet.cell(index, 2).value  # 2 - номер столбца для Tracking
        bot.send_message(message.chat.id, f'''{txt} : <b>{status}</b>''', parse_mode='html')
    else:
        bot.send_message(message.chat.id, f"Заказ {txt} не найден. ")
    end_time = time.time()
    total_time = end_time - start_time 
    print(total_time)


# bot.polling(none_stop=True)
# Функция для запуска опроса каждые 900 секунд
def run_polling():
    while True:
        schedule.run_pending()
        time.sleep(900)

schedule.every(900).seconds.do(start)

# Запуск опроса и проверки подписок в отдельном потоке
import threading
polling_thread = threading.Thread(target=run_polling)
polling_thread.daemon = True  # Установите daemon в True, чтобы поток работал в фоновом режиме
polling_thread.start()

# Отсюда начинается основной поток, в котором обрабатываются сообщения
bot.infinity_polling()









            # elif message.text == 'Участвовать':
            #     def is_user_in_file(user_id):
            #         with open('participants.txt', 'r') as file:
            #             global users
            #             users = file.readlines()
            #             global num_lines
            #             num_lines = len(users)

            #             for user in users:
            #                 if str(user_id) == user.strip():
            #                     return True
            #         return False
            #     user_id = message.chat.username
            #     if is_user_in_file(user_id):

            #         markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            #         item5 = telebot.types.KeyboardButton("Назад")
            #         markup.add(item5)

            #         bot.reply_to(message, f"Вы уже участвуете!", reply_markup=markup)

            #     else:

            #         with open('participants.txt', 'a') as file:
            #             file.write(str(user_id) + '\n')

            #         markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            #         item5 = telebot.types.KeyboardButton("Назад")
            #         markup.add(item5)
            #         bot.reply_to(message, f"Спасибо за участие!", reply_markup=markup)

            #         print('Розыгрыш.', 'Команда от: {0.first_name} {0.last_name}. id: {0.username} '.format(message.from_user, bot.get_me()))


            # elif message.text == 'Количество участников':
            #     with open('participants.txt', 'r') as file:
            #         users = file.readlines()
            #         members_len = len(users)
            #         bot.reply_to(message, f"Количество участников: {members_len}")
            #         print('Кол-во участников', 'Команда от: {0.first_name} {0.last_name}. id: {0.username} '.format(message.from_user, bot.get_me()))