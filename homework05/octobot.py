import json
from datetime import datetime, timedelta

import gspread
import numpy as np
import pandas
import pandas as pd
import requests
import telebot

bot = telebot.TeleBot("6102785506:AAF84IPauLelZATSr2aKOv-Qj76xNpt5878")
subject_n = 0
connected = False
df = pd.DataFrame
sheet = ""
dedline_n = 0


def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    try:
        parsed_date = datetime.strptime(date, f"%d{divider}%m{divider}%y").date()
    except ValueError:
        return False

    today_date = datetime.now().date()
    if parsed_date < today_date:
        return False
    if parsed_date > today_date + timedelta(days=365):
        return False

    return True


def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    try:
        # Добавляем схему, если ее нет
        if not url.startswith("http"):
            url = "https://" + url
        # Отправляем GET-запрос по указанной ссылке
        response = requests.get(url)
        # Проверяем, что статус-код ответа не является ошибкой (от 400 и выше)
        response.raise_for_status()
    except:
        return False

    return True


def convert_date(date: str = "01/01/00"):
    """Конвертируем дату из строки в datetime"""
    date_format = "%d/%m/%y"
    date_obj = datetime.strptime(date, date_format)
    return date_obj


def connect_table(message):
    """Подключаемся к Google-таблице"""
    global connected, df, sheet

    url = message.text
    if is_valid_url(url):
        sheet_id = url.split("/")[5]
        # sheet_id = '1bCTerqTeHyCtrLB3uiHfZyDdA-RYKS8PlYBUlxVf7EI'
        try:
            with open("tables.json") as json_file:
                tables = json.load(json_file)
            title = len(tables) + 1
            tables[title] = {"url": url, "id": sheet_id}
        except FileNotFoundError:
            tables = {0: {"url": url, "id": sheet_id}}
        with open("tables.json", "w") as json_file:
            json.dump(tables, json_file)
        bot.send_message(message.chat.id, "Таблица подключена!")
        connected = True
        sheet, _, df = access_current_sheet()
    else:
        bot.send_message(message.chat.id, "Неправильный url")
    start(message)


def access_current_sheet():
    """Обращаемся к Google-таблице"""
    with open("tables.json") as json_file:
        tables = json.load(json_file)

    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    df = pd.DataFrame(worksheet.get_all_records())
    if df.empty:
        df = pd.DataFrame({"subject": [], "link": []})
    df = df.replace("", np.NaN)
    return worksheet, tables[max(tables)]["url"], df


def get_subjects():  # функция которая выдаёт все предметы
    global df

    if df.empty:
        return []
    else:
        return df["subject"].tolist()


def get_all_deadlines_of_subject(subject_n):
    global df

    return df.iloc[subject_n].dropna().tolist()[2:]


def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        bot.send_message(chat_id=message.chat.id, text="Введите ссылку на Google-таблицу:")
        bot.register_next_step_handler(message, connect_table)
    elif message.text == "Редактировать предметы":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Посмотреть список предметов")
        start_markup.row("Добавить новый предмет")
        start_markup.row("Обновить информацию о предмете")
        start_markup.row("Удалить предмет")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject_action)
    elif message.text == "Посмотреть дедлайны на этой неделе":
        message_to_send = ""
        subjects = get_subjects()
        for i in range(len(subjects)):
            time_now = datetime.now()
            dedlines = []
            for j in get_all_deadlines_of_subject(i):
                if (convert_date(j) - time_now).days < 7:
                    dedlines.append(j)
            dedlines = ", ".join(dedlines)
            if not dedlines:
                dedlines = "Для данного предмета нет дедлайнов"
            message_to_send += f"{subjects[i]} - {dedlines}\n"
        bot.send_message(message.chat.id, message_to_send)
        start(message)
    elif message.text == "Редактировать дедлайн":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Посмотреть все дедлайны")
        start_markup.row("Обновить дедлайн")
        start_markup.row("Добавить новый дедлайн")
        start_markup.row("Удалить дедлайн")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_deadline_action)
    else:
        bot.send_message(chat_id=message.chat.id, text="Я не понимаю, что вы хотите сделать.")
        start(message)


def auto_markup(iter) -> telebot.types.ReplyKeyboardMarkup:
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for i in iter:
        markup.add(i)
    return markup


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    if message.text == "Посмотреть список предметов":
        subjects = get_subjects()
        if subjects:
            bot.send_message(message.chat.id, "Список предметов:\n" + "\n".join(subjects))
        else:
            bot.send_message(message.chat.id, "Список предметов пуст.")
        bot.register_next_step_handler(message, choose_subject_action)
    elif message.text == "Добавить новый предмет":
        bot.send_message(message.chat.id, "Введите название нового предмета:")
        bot.register_next_step_handler(message, add_new_subject)
    elif message.text == "Обновить информацию о предмете":
        subjects = get_subjects()
        if subjects:
            bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=auto_markup(subjects))
            bot.register_next_step_handler(message, update_subject)
        else:
            bot.send_message(message.chat.id, "Список предметов пуст.")
            bot.register_next_step_handler(message, choose_subject_action)
    elif message.text == "Удалить предмет":
        bot.send_message(message.chat.id, "Выберите предмет, который хотите удалить:")
        subjects = get_subjects()
        if subjects:
            bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=auto_markup(subjects))
            bot.register_next_step_handler(message, delete_subject)
        else:
            bot.send_message(message.chat.id, "Список предметов пуст.")
            bot.register_next_step_handler(message, choose_subject_action)
    else:
        bot.send_message(message.chat.id, "Выберите один из вариантов в меню.")
        bot.register_next_step_handler(message, choose_subject_action)


def choose_deadline_action(message):
    """Выбираем действие в разделе Редактировать дедлайн"""
    if message.text == "Посмотреть все дедлайны":
        message_to_send = ""
        subjects = get_subjects()
        for i in range(len(subjects)):
            dedlines = ", ".join(get_all_deadlines_of_subject(i))
            if not dedlines:
                dedlines = "Для данного предмета нет дедлайнов"
            message_to_send += f"{subjects[i]} - {dedlines}\n"
        bot.send_message(message.chat.id, message_to_send)
        start(message)
    elif message.text == "Обновить дедлайн":
        subjects = get_subjects()
        if subjects:
            bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=auto_markup(subjects))
            bot.register_next_step_handler(message, choose_deadline_to_update)
        else:
            bot.send_message(message.chat.id, "Список предметов пуст.")
    elif message.text == "Добавить новый дедлайн":
        subjects = get_subjects()
        if subjects:
            bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=auto_markup(subjects))
            bot.register_next_step_handler(message, enter_deadline_to_add)
        else:
            bot.send_message(message.chat.id, "Список предметов пуст.")
    elif message.text == "Удалить дедлайн":
        subjects = get_subjects()
        if subjects:
            bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=auto_markup(subjects))
            bot.register_next_step_handler(message, choose_deadline_to_delete)
        else:
            bot.send_message(message.chat.id, "Список предметов пуст.")

    else:
        bot.send_message(message.chat.id, "Выберите один из вариантов в меню.")
        bot.register_next_step_handler(message, choose_deadline_action)


# def choose_removal_option(message):
#     """Уточняем, точно ли надо удалить все"""
#     if message.text.lower() == "да":
#         for item in items:
#             item_id = item["id"]
#             remove_item(item_id)
#         bot.send_message(message.chat.id, "Все элементы удалены.")
#     elif message.text.lower() == "нет":
#         bot.send_message(message.chat.id, "Ок, ничего не будем удалять.")
#     else:
#         bot.send_message(message.chat.id, "Пожалуйста, ответьте 'Да' или 'Нет'.")
#         bot.register_next_step_handler(message, choose_removal_option)


def choose_subject_to_update(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    pass


def choose_deadline_to_delete(message):
    """ "Выбираем предмет, у которого надо удалить дедлайн"""

    global subject_n

    subject_n = get_subjects().index(message.text)
    dedlines = get_all_deadlines_of_subject(subject_n)
    if dedlines:
        bot.send_message(
            message.chat.id, "выберите деделайн, который нужно удалить", reply_markup=auto_markup(dedlines)
        )
        bot.register_next_step_handler(message, delete_subject_deadline)
    else:
        bot.send_message(message.chat.id, "для этого предмета нет дедлайнов")
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Посмотреть все дедлайны")
        start_markup.row("Обновить дедлайн")
        start_markup.row("Добавить новый дедлайн")
        start_markup.row("Удалить дедлайн")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_deadline_action)


def delete_subject_deadline(message):
    global df, subject_n

    dedline_n = get_all_deadlines_of_subject(subject_n).index(message.text) + 1

    df.loc[subject_n, str(dedline_n)] = np.NaN
    start(message)


def enter_deadline_to_add(message):
    """Выбираем предмет, у которого надо добавить дедлайн"""

    global subject_n

    subject_n = get_subjects().index(message.text)

    bot.send_message(message.chat.id, "Введите дедлайн, пример: 05/05/23")
    bot.register_next_step_handler(message, add_subject_deadline)


def add_subject_deadline(message):
    global df, subject_n
    if is_valid_date(message.text):
        df.loc[subject_n, str(df.count(axis=1)[subject_n] - 1)] = message.text
        start(message)
    else:
        bot.send_message(message.chat.id, "Введите нормальный дедлайн, пример: 05/05/23")
        bot.register_next_step_handler(message, add_subject_deadline)


def choose_deadline_to_update(message):
    """Обновляем дедлайн"""
    global subject_n

    subject_n = get_subjects().index(message.text)
    dedlines = get_all_deadlines_of_subject(subject_n)
    if dedlines:
        bot.send_message(
            message.chat.id, "выберите деделайн, который нужно изменить", reply_markup=auto_markup(dedlines)
        )
        bot.register_next_step_handler(message, get_new_deadline)
    else:
        bot.send_message(message.chat.id, "для этого предмета нет дедлайнов")
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Посмотреть все дедлайны")
        start_markup.row("Обновить дедлайн")
        start_markup.row("Добавить новый дедлайн")
        start_markup.row("Удалить дедлайн")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_deadline_action)


def get_new_deadline(message):
    global dedline_n, subject_n

    dedline_n = get_all_deadlines_of_subject(subject_n).index(message.text) + 1

    bot.send_message(message.chat.id, "Введите новую дату дедлайна")
    bot.register_next_step_handler(message, update_subject_deadline)


def update_subject_deadline(message):
    """Обновляем дедлайн"""
    global dedline_n
    print("aaaaaaaaaaaa")

    df.loc[subject_n, str(dedline_n)] = message.text
    start(message)


def add_new_subject(message):
    """Вносим новое название предмета в Google-таблицу"""
    global df

    df.loc[len(get_subjects())] = message.text
    bot.send_message(message.chat.id, "Введите ссылку на прдемет")
    bot.register_next_step_handler(message, add_new_subject_url)


def add_new_subject_url(message):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    df.loc[len(get_subjects()) - 1, "link"] = message.text
    start(message)


def update_subject(message):
    """Обновляем информацию о предмете в Google-таблице"""
    global subject_n

    subject_n = get_subjects().index(message.text)
    bot.send_message(message.chat.id, "Введите новое название предмета")
    bot.register_next_step_handler(message, update_subject_name)


def update_subject_name(message):
    """Обновляем информацию о предмете в Google-таблице"""
    global df, subject_n

    df.loc[subject_n, "subject"] = message.text
    bot.send_message(message.chat.id, "Введите новый url для предмета")
    bot.register_next_step_handler(message, update_subject_url)


def update_subject_url(message):
    """Обновляем информацию о предмете в Google-таблице"""
    global df, subject_n

    df.loc[subject_n, "link"] = message.text
    start(message)


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    global df

    df = df[df.subject != message.text]
    df.reset_index(drop=True, inplace=True)
    start(message)


def process_subject_deletion(message):
    """Обрабатываем выбор предмета для удаления"""


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    if message.text.lower() == "да":
        worksheet, _, df = access_current_sheet()
        worksheet.delete_rows(2, len(df) + 1)
        bot.send_message(message.chat.id, "Всё удалено")
    else:
        bot.send_message(message.chat.id, "Эх...")


def update():
    global df, sheet

    sheet.clear()
    df_copy = df.replace(np.NaN, "")
    sheet.update([df_copy.columns.values.tolist()] + df_copy.values.tolist())


@bot.message_handler(commands=["start"])
def start(message):
    print(df)
    print("---------------")
    if connected:
        update()
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if not connected:
        start_markup.row("Подключить Google-таблицу")
    start_markup.row("Посмотреть дедлайны на этой неделе")
    start_markup.row("Редактировать дедлайн")
    start_markup.row("Редактировать предметы")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


try:
    sheet, _, df = access_current_sheet()
except:
    print("Aaaaaaaaaaaaaaaaaaaaaaaaaa")
print(df)
bot.infinity_polling()
