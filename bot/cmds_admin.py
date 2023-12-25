from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from .keyboard import create_admin_kb
from . import admin_arr, session, bot
from database import get_users, get_user
from database.task import get_unverified_tasks, get_verified_tasks
from .keyboard import create_scrollable_keyboard, create_admin_kb, create_scrollable_keyboard_ver, create_scrollable_user_keyboard, create_open_dialog_kb


global task, id_tg
task = {}
id_tg = 0

admin_router = Router()
admin_form_router = Router()


class new_task(StatesGroup):
    name = State()
    discription = State()
    input = State()
    info = State()
    scores = State()
    const_count = State()
    max_count = State()


class new_all_message(StatesGroup):
    message = State()


class new_user_message(StatesGroup):
    message = State()


def check_adm(id):
    if id in admin_arr:
        return True
    else:
        return False


def get_short_name(FIO):
    FIO = FIO.split()
    FIO[1] = FIO[1][0]+'.'
    FIO[2] = FIO[2][0]+'.'
    FIO = FIO[0]+' '+FIO[1]+' '+FIO[2]
    return FIO


@admin_router.message(F.text == "Таблица")
async def cmd_adm_table(message: Message):
    if not check_adm(message.from_user.id):
        return
    keyboard = create_admin_kb
    # await message.answer('Таблица со всеми данными (обновляется не сразу)\n\nhttps://docs.google.com/spreadsheets/d/1CaAC60WG1oydCELHNAKhplAuk7k_vx4GeEtyF8hiwXk/edit#gid=0', reply_markup=keyboard)
    await message.answer('Таблица временно оключена из-за медленной работы', reply_markup=keyboard)


# Рассылка
@admin_router.message(F.text == "Сделать рассылку")
async def cmd_adm(message: Message, state: FSMContext) -> None:
    if not check_adm(message.from_user.id):
        return
    await message.answer('Отправьте текст для рассылки. Для отмены /cancel')
    await state.set_state(new_all_message.message)


@admin_form_router.message(new_all_message.message)
async def process_name(message: Message, state: FSMContext) -> None:
    if not check_adm(message.from_user.id):
        return
    users = get_users(session)

    for user in users:
        try:
            await bot.send_message(user.telegram_id, f'От администратаров всем: {message.text}')
        except:
            print(
                f'Пользователю @{user.telegram_username} (id: {user.id}) не удалось отправить сообщение')
            # await message.answer(f'Пользователю @{user.telegram_username} не удалось отправить сообщение')

    await message.answer('Рассылка сделана!')
    await state.clear()


'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''


@admin_router.message(F.text == 'Пользователи')
async def cmd_vremreshenie(message: Message, state: FSMContext) -> None:
    if not check_adm(message.from_user.id):
        return
    users = get_users(session)
    if len(users) == 0:
        return await message.answer('Пользователей ещё нет')
    kb = create_scrollable_user_keyboard(users)
    await message.answer('Пользователи:', reply_markup=kb)


@admin_router.callback_query(F.data.startswith('choose_'))
async def cmd_adm(callback: CallbackQuery):
    if not check_adm(callback.from_user.id):
        return
    userid = callback.data.replace('choose_', '')
    await callback.answer(f'Вы выбрали {userid}')
    user = get_user(session, userid)
    kb = create_open_dialog_kb(user.telegram_id)
    if userid:
        await callback.message.answer(
            f"ФИО: {user.full_name}\n"
            f"Телефон: {user.telephone}\n"
            f"e-mail: {user.email}\n",
            reply_markup=kb
        )
    else:
        await callback.message.answer(
            f"ошибка"
        )


async def update_scrollable_tasks_user_kb(callback_query: CallbackQuery, tasks, page):
    if not check_adm(callback_query.from_user.id):
        return
    kb = create_scrollable_user_keyboard(tasks, page)
    await callback_query.message.edit_reply_markup(reply_markup=kb)
    await callback_query.answer()


@admin_router.callback_query(F.data.startswith('next_page_user_'))
async def tasks_next_page(callback: CallbackQuery):
    if not check_adm(callback.from_user.id):
        return
    page = int(callback.data.split('_')[-1])
    tasks = get_users(session)
    await update_scrollable_tasks_user_kb(callback, tasks, page)


@admin_router.callback_query(F.data.startswith('prev_page_user_'))
async def tasks_prev_page(callback: CallbackQuery):
    if not check_adm(callback.from_user.id):
        return
    page = int(callback.data.split('_')[-1])
    tasks = get_users(session)
    await update_scrollable_tasks_user_kb(callback, tasks, page)


'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''


@admin_router.message(F.text == 'Не проверенные задания')
async def cmd_vremreshenie(message: Message):
    if not check_adm(message.from_user.id):
        return
    tasks = get_unverified_tasks()
    if len(tasks) == 0:
        return await message.answer('Нет не проверенных заданий')
    kb = create_scrollable_keyboard(tasks)
    await message.answer('Не проверенные задания:', reply_markup=kb)


async def update_scrollable_tasks_kb(callback_query: CallbackQuery, tasks, page):
    if not check_adm(callback_query.from_user.id):
        return
    kb = create_scrollable_keyboard(tasks, page)
    await callback_query.message.edit_reply_markup(reply_markup=kb)
    await callback_query.answer()


@admin_router.callback_query(F.data.startswith('next_page_unver_'))
async def tasks_next_page(callback: CallbackQuery):
    if not check_adm(callback.from_user.id):
        return
    page = int(callback.data.split('_')[-1])
    tasks = get_unverified_tasks()
    await update_scrollable_tasks_kb(callback, tasks, page)


@admin_router.callback_query(F.data.startswith('prev_page_unver_'))
async def tasks_prev_page(callback: CallbackQuery):
    if not check_adm(callback.from_user.id):
        return
    page = int(callback.data.split('_')[-1])
    tasks = get_unverified_tasks()
    await update_scrollable_tasks_kb(callback, tasks, page)


'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''


@admin_router.message(F.text == 'Проверенные задания')
async def cmd_vremreshenie(message: Message):
    if not check_adm(message.from_user.id):
        return
    tasks = get_verified_tasks()
    if len(tasks) == 0:
        return await message.answer('Нет проверенных заданий')
    kb = create_scrollable_keyboard_ver(tasks)
    await message.answer('Проверенные задания:', reply_markup=kb)


async def update_scrollable_tasks_ver_kb(callback_query: CallbackQuery, tasks, page):
    if not check_adm(callback_query.from_user.id):
        return
    kb = create_scrollable_keyboard_ver(tasks, page)
    await callback_query.message.edit_reply_markup(reply_markup=kb)
    await callback_query.answer()


@admin_router.callback_query(F.data.startswith('next_page_ver_'))
async def tasks_next_page(callback: CallbackQuery):
    if not check_adm(callback.from_user.id):
        return
    page = int(callback.data.split('_')[-1])
    tasks = get_verified_tasks()
    await update_scrollable_tasks_ver_kb(callback, tasks, page)


@admin_router.callback_query(F.data.startswith('prev_page_ver_'))
async def tasks_prev_page(callback: CallbackQuery):
    if not check_adm(callback.from_user.id):
        return
    page = int(callback.data.split('_')[-1])
    tasks = get_verified_tasks()
    await update_scrollable_tasks_ver_kb(callback, tasks, page)


'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------'''


@admin_router.callback_query(F.data.startswith('dialog_'))
async def cmd_adm(callback: CallbackQuery, state: FSMContext) -> None:
    if not check_adm(callback.from_user.id):
        return
    userid = callback.data.replace('dialog_', '')
    await callback.answer(f'Вы выбрали {userid}')
    if userid:
        await state.set_state(new_user_message.message)
        global id_tg
        id_tg = userid
        return await callback.message.answer(
            f'Напишите сообщение пользователю. Для отмены /cancel'
        )
    await callback.message.answer(
        f"ошибка"
    )


@admin_form_router.message(new_user_message.message)
async def process_name(message: Message, state: FSMContext) -> None:
    if not check_adm(message.from_user.id):
        return
    try:
        await bot.send_message(id_tg, message.text)
        await message.answer('Сообщение отправлено!')
    except:
        await message.answer(f'Пользователю не удалось отправить сообщение')

    await state.clear()
