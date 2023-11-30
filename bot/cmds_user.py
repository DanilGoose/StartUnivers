from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from .keyboard import create_main_kb, create_admin_kb, create_tasks_kb
from database import get_user_tg, get_user, get_points

from . import session, bot, admin_arr

user_router = Router()
user_form_router = Router()


class help(StatesGroup):
    message = State()


@user_router.message(F.text == "Мой аккаунт")
async def cmd_user_rules(message: Message):
    user = get_user_tg(session, message.from_user.id)
    points = get_points(session, message.from_user.id)
    await message.answer(f'''
Вы: <b>{user.full_name}</b>
Ваш номер телефона: <b>{user.telephone}</b>
Ваша почта: <b>{user.email}</b>
Ваша должность: <b>{user.post}</b>
Имя вашего наставника: <b>{user.mentor_full_name}</b>
Количество суммарных баллов: <b>{points.sum}</b>
Выполнили все обязательные задания нужное кол во раз: <b>{'нет' if points.state_sum == 0 else 'да'}</b>

''',
                         parse_mode="HTML")


@user_router.message(F.text == "Правила")
async def cmd_user_rules(message: Message):
    with open('required files/rules.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    await message.answer(f'Правила:\n{text}')


@user_router.message(F.text == "Помощь")
async def cmd_user_tasks(message: Message, state: FSMContext) -> None:
    await message.answer('Отправьте вашу проблему. Для отмены введите /cancel')
    await state.set_state(help.message)


@user_form_router.message(help.message)
async def process_problem(message: Message, state: FSMContext) -> None:
    problem_text = message.text
    user = get_user_tg(session, message.from_user.id)
    for admin_id in admin_arr:
        await bot.send_message(admin_id, f"Проблема от {user.full_name}:\n{problem_text}")
    await message.answer("Ваша проблема отправлена администратору.")
    await state.clear()


# Тестове функции на время разработки
# ---------------------------------------------------------
# @user_router.message(F.text == "/getadmkb")
# async def cmd_user_tasks(message: Message):
#     kb = create_admin_kb
#     await message.answer('Вызов клавиатуры для админов', reply_markup=kb)


# @user_router.message(F.text == "/getuserkb")
# async def cmd_user_tasks(message: Message):
#     kb = create_main_kb
#     await message.answer('Вызов клавиатуры для юзеров', reply_markup=kb)
# ---------------------------------------------------------
