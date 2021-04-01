"""
Тут функции по отправке и редактированию сообщений
"""

from botStarter import bot
from telebot import types


def send(chatid, new_message, menu=False, markdown=True):
    """
    Отправка нового сообщения

    :param chatid: id пользователя, которому нужно отправить
    :param new_message: текст сообщения
    :param menu: меню сообщения
    :param markdown: включение или отключение разметки
    :return: при успешной отправке True, иначе False
    """
    try:
        if not menu:
            bot.send_message(chatid, new_message, parse_mode='Markdown')
        else:
            if markdown:
                bot.send_message(chatid, new_message, reply_markup=menu, parse_mode='Markdown')
            else:
                bot.send_message(chatid, new_message, reply_markup=menu)
    except Exception as e:
        print(e)
        return False
    else:
        return True


def edit(chatid, messageid, new_message, menu=False, markdown=True):
    """
    Редактирование существующего сообщения

    :param chatid: id пользователя, которому нужно отправить
    :param messageid: id сообщения
    :param new_message: текст нового сообщения
    :param menu: меню нового сообщения
    :param markdown: включение или отключение разметки
    :return: при успешном редактировании True, иначе False
    """
    try:
        if not menu:
            bot.edit_message_text(chat_id=chatid, message_id=messageid, text=new_message, parse_mode='Markdown')
        else:
            if markdown:
                bot.edit_message_text(chat_id=chatid, message_id=messageid, text=new_message, reply_markup=menu,
                                      parse_mode='Markdown')
            else:
                bot.edit_message_text(chat_id=chatid, message_id=messageid, text=new_message, reply_markup=menu)
    except Exception as e:
        print(e)
        return False
    else:
        return True


def senddoc(chatid, name, format):
    """
    Отправка csv файла пользователю

    :param chatid: id пользователя, которому нужно отправить
    :param value: название файла
    :return: при успешной отправке True, иначе False
    """
    try:
        bot.send_document(chatid, open('Объявления//' + name + format, 'rb'))
    except Exception as e:
        print(e)
        return False
    else:
        return True


def mainmenu(chatid, message_id=False):
    """
    Формирование и отправка главного меню.

    :param chatid: id пользователя, которому нужно отправить
    :param message_id: если нужно отредактировать существующее сообщение, то отпредактирует его, иначе отправит новым сообщением
    :return:
    """
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text='🔎Спарсить', callback_data='parse'))
    menu.add(types.InlineKeyboardButton(text='👨🏽‍💻Профиль', callback_data='profile'),
             types.InlineKeyboardButton(text='🗒История', callback_data='history'))
    menu.add(types.InlineKeyboardButton(text='❓Инструкция', callback_data='instruction'),
    types.InlineKeyboardButton(text='👨🏼‍🔧Помощь', callback_data='help'))
    new_message = "_Главное меню_"
    if not message_id:
        send(chatid, new_message, menu)
    else:
        edit(chatid, message_id, new_message, menu, markdown=True)


def welcome(chatid):
    """
    Отправка стартового меню с пользовательским соглашением и т.д

    :param chatid: id пользователя, которому нужно отправить
    :return:
    """
    menu = types.InlineKeyboardMarkup()
    menu.add(types.InlineKeyboardButton(text="🗒Инструкция", url="https://telegra.ph/"))
    menu.add(types.InlineKeyboardButton(text="Пользовательское соглашение", url="https://telegra.ph/"))
    menu.add(types.InlineKeyboardButton(text='Продолжить', callback_data='continue'))
    new_message = "Добро пожаловать в avParser!\n\nПрочитайте инструкцию перед входом.\n\nДля продолжения необходимо " \
                  "принять *Пользовательское соглашение* "
    send(chatid, new_message, menu)
