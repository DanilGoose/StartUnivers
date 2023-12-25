from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)

# reply
main_kb = [
    [
        KeyboardButton(text='Мой аккаунт'),
        KeyboardButton(text='Задания')
    ],
    [
        KeyboardButton(text='Правила'),
        KeyboardButton(text='Помощь')
    ]
]

admin_kb = [
    [
        KeyboardButton(text='Задания'),
        KeyboardButton(text='Правила')
    ],
    [
        KeyboardButton(text='Пользователи'),
        KeyboardButton(text='Проверенные задания'),
        KeyboardButton(text='Не проверенные задания')
    ],
    [
        KeyboardButton(text='Таблица'),
        KeyboardButton(text='Сделать рассылку')
    ]
]

create_main_kb = ReplyKeyboardMarkup(
    keyboard=main_kb,
    resize_keyboard=True,
    input_field_placeholder='Нажмите на кнопку ниже...'
)


create_admin_kb = ReplyKeyboardMarkup(
    keyboard=admin_kb,
    resize_keyboard=True,
    input_field_placeholder='Нажмите на кнопку ниже...'
)


def contact_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='📱 Отправить', request_contact=True)
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder='Нажмите на кнопку ниже...'
    )
    return markup


# inline
def fname(items, page=1):
    items_per_page = 5
    start_index = (page - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(items))

    keyboard = []
    for i in range(start_index, end_index):
        keyboard.append([InlineKeyboardButton(
            text=f'{items[i][3]}', callback_data=f'choose_{items[i][0]}')])

    navigation_buttons = []

    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='◀️ Назад', callback_data=f'prev_page_{page-1}')
        )
    if end_index < len(items):
        navigation_buttons.append(
            InlineKeyboardButton(
                text='Вперед ▶️', callback_data=f'next_page_{page+1}')
        )

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_tasks_kb(arr):
    tasks_kb = []
    last = arr[-1]
    for task in arr:
        if task != last:
            tasks_kb.append(
                [
                    InlineKeyboardButton(
                        text=f'{task.name}',
                        callback_data=f'task_{task.id}'
                    )
                ],
            )
        else:
            tasks_kb.append(
                [
                    InlineKeyboardButton(
                        text=f'{task.name}',
                        callback_data=f'task_{task.id}'
                    )
                ]
            )
    tasks = InlineKeyboardMarkup(inline_keyboard=tasks_kb)
    return tasks


def create_pass_kb(task_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Сдать задание',
                callback_data=f'pass_{task_id}'
            )
        ]
    ])
    return kb


def create_open_dialog_kb(telegram_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Написать сообщение пользователю',
                callback_data=f'dialog_{telegram_id}'
            )
        ]
    ])
    return kb


def create_scrollable_user_keyboard(items, page=1):
    items_per_page = 5
    start_index = (page - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(items))

    keyboard = []
    print(items)    
    for i in range(start_index, end_index):
        print(items[i].full_name)
        keyboard.append([InlineKeyboardButton(
            text=f'{items[i].full_name}', callback_data=f'choose_{items[i].id}')])

    navigation_buttons = [] 

    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='◀️ Назад', callback_data=f'next_page_user_{page-1}')
        )
    if end_index < len(items):
        navigation_buttons.append(
            InlineKeyboardButton(
                text='Вперед ▶️', callback_data=f'prev_page_user_{page+1}')
        )

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_scrollable_keyboard_ver(items, page=1):
    items_per_page = 5
    start_index = (page - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(items))

    keyboard = []
    for i in range(start_index, end_index):
        keyboard.append([InlineKeyboardButton(
            text=f'{items[i][0]} - задание №{items[i][2]}', callback_data=f'adm_choose_task_ver_{items[i][0]}')])

    navigation_buttons = []

    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='◀️ Назад', callback_data=f'next_page_ver_{page-1}')
        )
    if end_index < len(items):
        navigation_buttons.append(
            InlineKeyboardButton(
                text='Вперед ▶️', callback_data=f'prev_page_ver_{page+1}')
        )

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_scrollable_keyboard(items, page=1):
    items_per_page = 5
    start_index = (page - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(items))

    keyboard = []
    for i in range(start_index, end_index):
        keyboard.append([InlineKeyboardButton(
            text=f'{items[i][0]} - задание №{items[i][2]}', callback_data=f'adm_choose_task_unver_{items[i][0]}')])

    navigation_buttons = []

    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text='◀️ Назад', callback_data=f'next_page_unver_{page-1}')
        )
    if end_index < len(items):
        navigation_buttons.append(
            InlineKeyboardButton(
                text='Вперед ▶️', callback_data=f'prev_page_unver_{page+1}')
        )

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_ver_keyboard(task):
    keyboard = [
        [
            InlineKeyboardButton(
                text='Текст задания', callback_data=f'show_text_{task}')
        ],
        [
            InlineKeyboardButton(
                text='Отклонить', callback_data=f'unver_{task}'),
        ],
        # [
        #     InlineKeyboardButton(
        #         text='Не полный балл', callback_data=f'ver_nofull_{task}'),
        # ],пфн зщкт цшер мукн дф         gay porn with very large cock from kolt and bull from Brawl Star
        [
            InlineKeyboardButton(
                text='Полный балл✅', callback_data=f'ver_full_{task}')
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
