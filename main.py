import telebot
from telebot import types
from random import choice, shuffle
import json


# TOKEN = "5289245325:AAEo8pwsc7l5kL6YCqu1C6O6fB-0BtQLJJk" # Токен Ильи
TOKEN = "5798765362:AAFvMnOCIREv9JitthLukfH7pZjPWCY4SFs"  # Токен Вильсона

bot = telebot.TeleBot(TOKEN)

our_id = -1001834028271
attempts = 3

users = json.load(open('users_info.json', 'r', encoding='utf-8'))
data = json.load(open('all_data.json', 'r', encoding='utf-8'))


# вывод клавиатуры с функцией top
def keyboard_welcome():
    mark = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_1 = types.KeyboardButton(text="/tasks")
    btn_2 = types.KeyboardButton(text="/top")
    mark.add(btn_1)
    mark.add(btn_2)
    return mark


def keyboard_restart():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but_1 = types.KeyboardButton(text='Начать подготовку')
    but_2 = types.KeyboardButton(text='Лидеры по этому заданию')
    markup.add(but_1)
    markup.add(but_2)
    return markup


@bot.message_handler(commands=["start"])
def welcome(message):
    uid = message.chat.id
    if str(uid) not in users:
        if message.chat.username:
            name = message.chat.username

        else:
            name = f"{message.from_user.first_name} {message.from_user.second_name}"
        user = json.load(open('Empty_uesrs_template.json', 'r', encoding='utf-8'))
        user["name"] = name
        for j in user["remaining_attempts"]:
            user["remaining_attempts"][j] = attempts
        users[str(uid)] = user
        open("users_info.json", "w").write(json.dumps(users))
    bot.send_message(message.chat.id,
                     f'Добро пожаловать, {message.from_user.first_name}. Бот создан для подготовки к '
                     f'ЕГЭ по русскому.\n'
                     f'Основные команды бота:\n'
                     f'/tasks - выводит список заданий\n'
                     f'/feedback - написать нам\n'
                     f'/progress - посмотреть свои лучшие результаты по задачам\n'
                     f'/top - показывает результаты лучших десяти участников по сумме баллов во всех заданиях\n',
                     reply_markup=keyboard_welcome())


@bot.message_handler(commands=["feedback"])
def feedback_from_user(message):
    mesg = bot.send_message(message.chat.id, text='Введите пожалуйста ваш вопрос одним сообщением',
                            reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(mesg, feedback_to_us)


def feedback_to_us(message):
    bot.send_message(our_id, text=f'К нам поступил feedback от @{message.chat.username}:\n{message.text}',
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=["stats"])
def keys(message):
    bot.send_message(message.chat.id, text=f'Количество участников {len(users.keys())}')


@bot.message_handler(commands=["tasks"])
def welcome(message):
    bot.send_message(message.chat.id, f'На данный момент в этом боте реализованы задания:\n'
                                      f'/task4 - Ударения\n'
                                      f'/task5 - Паронимы\n'
                                      f'/task6 - Лексические нормы\n'
                                      f'/task7 - Морфологические нормы\n'
                                      f'/task8 - Синтаксические нормы\n'
                                      f'/task9 - Правописание корней\n'
                                      f'/task10 - Правописание приставок\n'
                                      f'/task11 - Правописание суффиксов (кроме -Н-/-НН-)\n'
                                      f'/task12 - Правописание окончаний и суффиксов\n'
                                      f'/task13 - Правописание НЕ и НИ\n'
                                      f'/task14 - Слитное, дефисное, раздельное написание слов\n'
                                      f'/task15 - задания на правописание корней\n'
                                      f'/task16 - Пунктуация в сложносочиненном предложении\n'
                                      f'/task17 - Знаки препинания в предложениях с обособленными членами\n'
                                      f'/task18 - Знаки препинания при словах, не связанных с членами предложения\n'
                                      f'/task19 - Знаки препинания в сложноподчиненном предложении\n'
                                      f'/task20 - Знаки препинания в сложных предложениях с разными видами связи\n',
                                      # f'/task21 - Постановка знаков препинания\n',
                     reply_markup=types.ReplyKeyboardRemove())


# функция для отправки сообщений пользователям
@bot.message_handler(commands=["send_users"])
def message(message):
    mesg = bot.send_message(message.chat.id, text='Введите текст сообщения для отправки пользователям:')
    bot.register_next_step_handler(mesg, send_message)


def send_message(mesg):
    for i in users:
        bot.send_message(i, text=mesg.text)


@bot.message_handler(commands=["progress"])
def progress(message):
    l = []
    uid = message.chat.id
    for j in users[str(uid)]['best_score']:
        l.append([users[str(uid)]['best_score'][j], j.replace("#", "")])
    l.sort(key=lambda x: x[0], reverse=True)
    local_out = f"Ваши лучшие результаты:\n"
    for j in range(5):
        local_out += f"{j + 1}) Задание {l[j][1]} с вашим рекордом {l[j][0]}\n"
    bot.send_message(message.chat.id, text=local_out, reply_markup=types.ReplyKeyboardRemove())


def task_initiation(message):
    uid = message.chat.id
    task_number = message.text.replace('/task', '')
    attempt_local = users[str(uid)]["remaining_attempts"]["#" + task_number]
    if attempt_local == 3:
        bot.send_message(message.from_user.id, f'У вас есть {users[str(uid)]["remaining_attempts"]["#" + task_number]} попытки',
                     reply_markup=keyboard_restart())
    else:
        bot.send_message(message.from_user.id,
                         f'У вас осталось {users[str(uid)]["remaining_attempts"]["#" + task_number]} попытки',
                         reply_markup=keyboard_restart())
    users[str(uid)]['actual_task'] = f'#{task_number}'
    users[str(uid)]['actual_question'] = 0


# функция выводит первое сообщение приветсвия
@bot.message_handler(commands=["task4", "task5", "task6", "task7", "task8",
                               "task9", "task10", "task11", "task12", "task13",
                               "task14", "task15", "task16", "task17", "task18",
                               "task19", "task20", "task21"])
def welcome_task5(message):
    task_number = message.text.replace('/task', '')
    if task_number in ["4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
                       "21"]:
        task_initiation(message)


# функця для подсчета общего рекорда каждого пользователя
@bot.message_handler(commands=["top"])
def top_all(message):
    l = []
    for i in users:
        local_score = 0
        for j in users[i]['best_score']:
            local_score += max(users[i]['best_score'][j], users[i]['score'][j])
        l.append([local_score, users[i]["name"]])
    l.sort(key=lambda x: x[0], reverse=True)
    local_out = f"🏆 Лидеры по суммарным результатам:\n"
    for j in range(len(l)):
        if j == 9:
            break
        else:
            local_out += f"{j + 1})@{l[j][1]} с результатом {l[j][0]}\n"
    bot.send_message(message.chat.id, text=local_out, reply_markup=types.ReplyKeyboardRemove())


def top(message, text):
    l = []
    for i in users:
        local_score = users[i]['best_score']["#" + text]
        l.append([local_score, users[i]["name"]])
    l.sort(key=lambda x: x[0], reverse=True)
    local_out = f"🏆 Лидеры по результатам:\n"
    for j in range(len(l)):
        if j == 9:
            break
        else:
            local_out += f"{j + 1})@{l[j][1]} с результатом {l[j][0]}\n"
    bot.send_message(message.chat.id, text=local_out, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def user_answer(message):
    uid = message.chat.id
    actual_task = users[str(uid)]['actual_task']
    if not users[str(uid)]['actual_question']:
        if message.text == 'Начать подготовку':
            markup = question_update(str(uid))
            if not data[actual_task]['questions'][users[str(uid)]['actual_question']]['all']:
                markup = types.ReplyKeyboardRemove()

            bot.send_message(uid, f'{data[actual_task]["hello_text"]}', reply_markup=markup)
            if data[actual_task]['questions'][users[str(uid)]['actual_question']]['text']:
                bot.send_message(uid, data[actual_task]['questions'][users[str(uid)]['actual_question']]['text'])

        if message.text == 'Продолжить подготовку':
            markup = question_update(str(uid))
            bot.send_message(uid, data[actual_task]["hello_text"], reply_markup=markup)
            if data[actual_task]['questions'][users[str(uid)]['actual_question']]['text']:
                bot.send_message(uid, data[actual_task]['questions'][users[str(uid)]['actual_question']]['text'])

        if message.text == 'Лидеры по этому заданию':
            x = actual_task
            top(message, x.replace("#", ""))

    else:
        if actual_task == "#8" and message.text == "Список вариантов ошибок":
            bot.send_message(message.chat.id, text=f'0) В предложении нет ошибки\n'
                                                   f'1) Нарушение в построении предложения с причастным оборотом\n'
                                                   f'2) Нарушение связи между подлежащим и сказуемым\n'
                                                   f'3) Ошибка в построении предложения с деепричастным оборотом\n'
                                                   f'4) Нарушение в построении предложения с несогласованным приложением\n'
                                                   f'5) Неправильное употребление падежной формы существительного с предлогом\n'
                                                   f'6) Ошибка в построении предложения с однородными членами\n'
                                                   f'7) Нарушение в построении предложения с несогласованным приложением\n'
                                                   f'8) Ошибка в построении предложения с косвенной речью\n'
                                                   f'9) Нарушение в построении предложения с несогласованным приложением\n'
                                                   f'10) Нарушение видовременной соотнесённости глагольных форм\n'
                                                   f'11) Ошибка в построении сложного предложения'
                                                   f'12) Ошибка в употреблении имени числительного')
        else:
            actual_question = users[str(uid)]['actual_question']
            if len(data[actual_task]['questions'][actual_question]['all']) > 1 and \
                    message.text not in data[actual_task]['questions'][actual_question]['all']:
                bot.send_message(uid, 'Ответ введен в неверном формате')

            else:
                if (message.text.lower() == data[actual_task]['questions'][actual_question]['right'].lower() and actual_task != "#4") or (message.text == data[actual_task]['questions'][actual_question]['right'] and actual_task == "#4"):
                    markup = question_update(str(uid))
                    if not data[actual_task]['questions'][users[str(uid)]['actual_question']]['all']:
                        markup = types.ReplyKeyboardRemove()

                    bot.send_message(uid, '✅ Вы ответили правильно!', reply_markup=markup)
                    if data[actual_task]['questions'][users[str(uid)]['actual_question']]['text']:
                        bot.send_message(uid, data[actual_task]['questions'][users[str(uid)]['actual_question']]['text'])

                    users[str(uid)]['score'][actual_task] += 1

                else:
                    if users[str(uid)]["remaining_attempts"][actual_task] == 1:
                        users[str(uid)]["remaining_attempts"][actual_task] = attempts
                        if data[actual_task]["type_out"] == "NO":
                            if users[str(uid)]['score'][actual_task] <= users[str(uid)]['best_score'][actual_task]:
                                bot.send_message(uid, f'❌ К сожалению, вы ошиблись:(.\n'
                                                      f'Ваши попытки закончились(\n'
                                                      f'Вы набрали {users[str(uid)]["score"][actual_task]} очков.\n',
                                                 reply_markup=keyboard_restart())
                            else:
                                users[str(uid)]['best_score'][actual_task] = users[str(uid)]['score'][actual_task]
                                bot.send_message(uid,
                                                 f'❌ К сожалению, вы ошиблись:(.\n'
                                                 f'Ваши попытки закончились(\n'
                                                 f'Однако вы побили свой рекорд, набрав {users[str(uid)]["score"][actual_task]} очков.\n',
                                                 reply_markup=keyboard_restart())

                        elif data[actual_task]["type_out"] == "YES":
                            if users[str(uid)]['score'][actual_task] <= users[str(uid)]['best_score'][actual_task]:
                                bot.send_message(uid,
                                                 f'❌ К сожалению, вы ошиблись:(.\n'
                                                 f'Верный ответ:\n{data[actual_task]["questions"][actual_question]["out_data"]}\n'
                                                 f'Ваши попытки закончились(\n'
                                                 f'Вы набрали {users[str(uid)]["score"][actual_task]} очков.\n',
                                                 reply_markup=keyboard_restart())
                            else:
                                users[str(uid)]['best_score'][actual_task] = users[str(uid)]['score'][actual_task]
                                bot.send_message(uid,
                                                 f'❌ К сожалению, вы ошиблись:(.\n'
                                                 f'Верный ответ:\n{data[actual_task]["questions"][actual_question]["out_data"]}\n'
                                                 f'Ваши попытки закончились(\n'
                                                 f'Однако вы побили свой рекорд, набрав {users[str(uid)]["score"][actual_task]} очков.\n',
                                                 reply_markup=keyboard_restart())

                        elif data[actual_task]["type_out"] == "NO_YES":
                            if data[actual_task]["questions"][actual_question]["right"] == "Неслитно" or \
                                    data[actual_task]["questions"][actual_question]["right"] == "Нет" or \
                                    data[actual_task]["questions"][actual_question]["right"] == "Неверно":
                                if users[str(uid)]['score'][actual_task] <= users[str(uid)]['best_score'][actual_task]:
                                    bot.send_message(uid,
                                                     f'❌ К сожалению, вы ошиблись:(.\n'
                                                     f'Верный ответ:\n{data[actual_task]["questions"][actual_question]["out_data"]}\n'
                                                     f'Ваши попытки закончились(\n'
                                                     f'Вы набрали {users[str(uid)]["score"][actual_task]} очков.\n',
                                                     reply_markup=keyboard_restart())
                                else:
                                    users[str(uid)]['best_score'][actual_task] = users[str(uid)]['score'][actual_task]
                                    bot.send_message(uid,
                                                     f'❌ К сожалению, вы ошиблись:(. '
                                                     f'Верный ответ:\n{data[actual_task]["questions"][actual_question]["out_data"]}\n'
                                                     f'Ваши попытки закончились(\n'
                                                     f'Однако вы побили свой рекорд, набрав {users[str(uid)]["score"][actual_task]} очков.\n',
                                                     reply_markup=keyboard_restart())

                            else:
                                if users[str(uid)]['score'][actual_task] <= users[str(uid)]['best_score'][actual_task]:
                                    bot.send_message(uid,
                                                     f'❌ К сожалению, вы ошиблись:(.\nВы набрали {users[str(uid)]["score"][actual_task]} очков.\n'
                                                     f'Ваши попытки закончились(\n',
                                                     reply_markup=keyboard_restart())
                                else:
                                    users[str(uid)]['best_score'][actual_task] = users[str(uid)]['score'][actual_task]
                                    bot.send_message(uid,
                                                     f'❌ К сожалению, вы ошиблись:(.\n'
                                                     f'Ваши попытки закончились(\n'
                                                     f'Однако вы побили свой рекорд, набрав {users[str(uid)]["score"][actual_task]} очков.\n',
                                                     reply_markup=keyboard_restart())

                        users[str(uid)]['score'][actual_task] = 0
                        users[str(uid)]['actual_question'] = None
                    else:
                        users[str(uid)]["remaining_attempts"][actual_task] -= 1
                        markup = question_update(str(uid))
                        if not data[actual_task]['questions'][users[str(uid)]['actual_question']]['all']:
                            markup = types.ReplyKeyboardRemove()

                        if data[actual_task]["type_out"] == "NO":
                            bot.send_message(uid, f'❌ К сожалению, вы ошиблись:(.\n'
                                                  f'У вас осталось {users[str(uid)]["remaining_attempts"][actual_task]} попыток\n',
                                             reply_markup=markup)

                        elif data[actual_task]["type_out"] == "YES":
                            bot.send_message(uid,
                                             f'❌ К сожалению, вы ошиблись:(.\n'
                                             f'Верный ответ:\n{data[actual_task]["questions"][actual_question]["out_data"]}\n'
                                             f'У вас осталось {users[str(uid)]["remaining_attempts"][actual_task]} попыток\n',
                                             reply_markup=markup)

                        elif data[actual_task]["type_out"] == "NO_YES":
                            if data[actual_task]["questions"][actual_question]["right"] == "Неслитно" or \
                                    data[actual_task]["questions"][actual_question]["right"] == "Нет" or \
                                    data[actual_task]["questions"][actual_question]["right"] == "Неверно":
                                bot.send_message(uid,
                                                 f'❌ К сожалению, вы ошиблись:(.\n'
                                                 f'Верный ответ:\n{data[actual_task]["questions"][actual_question]["out_data"]}\n'
                                                 f'У вас осталось {users[str(uid)]["remaining_attempts"][actual_task]} попыток\n',
                                                 reply_markup=markup)

                            else:
                                bot.send_message(uid,
                                                 f'❌ К сожалению, вы ошиблись:(.\nВы набрали {users[str(uid)]["score"][actual_task]} очков.\n'
                                                 f'У вас осталось {users[str(uid)]["remaining_attempts"][actual_task]} попыток\n',
                                                 reply_markup=markup)

                        if data[actual_task]['questions'][users[str(uid)]['actual_question']]['text']:
                            bot.send_message(uid, data[actual_task]['questions'][users[str(uid)]['actual_question']]['text'])
            open("users_info.json", "w").write(json.dumps(users, indent=4))


def question_update(user_id):
    new_actual_question = choice(list(data[users[user_id]['actual_task']]['questions']))
    users[user_id]['actual_question'] = new_actual_question

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if data[users[user_id]['actual_task']]['questions'][new_actual_question]['all']:
        shuffled_buttons = list(data[users[user_id]['actual_task']]['questions'][new_actual_question]['all'])
        shuffle(shuffled_buttons)
        if len(shuffled_buttons) == 2:
            btn_1 = types.KeyboardButton(shuffled_buttons[0])
            btn_2 = types.KeyboardButton(shuffled_buttons[1])
            markup.add(btn_1, btn_2)
        else:
            for ready_answer in shuffled_buttons:
                markup.add(types.KeyboardButton(text=ready_answer))

    return markup


if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling()
        except IndexError:
            pass
