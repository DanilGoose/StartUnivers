from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import re
from .keyboard import create_main_kb, create_admin_kb, contact_keyboard
from database import create_user, check_id, get_users, get_user

from . import admin_arr, session, bot
# global new_user_dict, admin_arr, session

register_router = Router()
register_form_router = Router()


class new_user(StatesGroup):
    full_name = State()
    post = State()
    telephone = State()
    e_mail = State()
    mentor_full_name = State()


async def check_valid_name(name):
    text = name.split()
    try_name = True
    if len(text) == 3:
        for i in text:
            if i[0].islower():
                try_name = False
    else:
        try_name = False

    return try_name


@register_form_router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    return await message.answer(f"Отменено. Пропишите /start", reply_markup=ReplyKeyboardRemove())


@register_router.message(F.text == '/start')
async def cmd_start(message: Message, state: FSMContext) -> None:
    username = message.from_user.first_name

    if message.from_user.id in admin_arr:
        keyboard = create_admin_kb
        return await message.answer(f'Добро пожаловать, {username}!', reply_markup=keyboard)

    if check_id(session, message.from_user.id):
        keyboard = create_main_kb

        return await message.answer(f'Добро пожаловать, {username}!\n\nСкорее приступайте к выполнению заданий!', reply_markup=keyboard)

    welcome_message = f"Привет, {username}! " \
        "Здесь проходит игра Start_Univers!\n"\
        "Для начала игры необходимо зарегистрироваться\n\n"\
        "Введите своё ФИО! (ПРИ НЕПРАВИЛЬНО ВВЕДЁННЫХ ДАННЫХ СООБЩИТЕ АДМИНАМ)"

    await message.answer(welcome_message, reply_markup=ReplyKeyboardRemove())

    await state.set_state(new_user.full_name)


@register_form_router.message(new_user.full_name)
async def process_full_name(message: Message, state: FSMContext) -> None:
    text = message.text

    try_name = await check_valid_name(text)

    if try_name:
        await state.update_data(full_name=text)
        await message.answer(f"Ваше ФИО: {text}\n\nТеперь введите вашу должность")
        await state.set_state(new_user.post)

    else:
        return await message.answer('Некоректный ввод, введите Имя, Фамилию и Отчество с большой буквы и через пробел соответственно')


@register_form_router.message(new_user.post)
async def process_telephone(message: Message, state: FSMContext) -> None:
    post = message.text

    await state.update_data(post=post)

    kb = contact_keyboard()

    await message.answer(f"Ваша должность: {post}\n\nТеперь поделитесь своим номером телефона", reply_markup=kb)

    await state.set_state(new_user.telephone)


@register_form_router.message(new_user.telephone)
async def process_telephone(message: Message, state: FSMContext) -> None:
    contact = message.contact.phone_number

    await state.update_data(telephone=contact)

    await message.answer(f"Ваш номер телефона: {contact}\n\nТеперь введите ваш e-mail", reply_markup=ReplyKeyboardRemove())

    await state.set_state(new_user.e_mail)


@register_form_router.message(new_user.e_mail)
async def process_e_mail(message: Message, state: FSMContext) -> None:
    text = message.text

    await state.update_data(email=text)

    regexp = re.compile(
        r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}$', re.IGNORECASE)
    email = regexp.findall(text)
    if not email:
        return await message.answer("Неверная почта, введите повторно")

    await message.answer(f"Ваш e-mail: {text}\n\nТеперь введите ФИО вашего наставника")

    await state.set_state(new_user.mentor_full_name)


@register_form_router.message(new_user.mentor_full_name)
async def process_mentor_full_name(message: Message, state: FSMContext) -> None:
    text = message.text

    try_name = await check_valid_name(text)
    if try_name:
        kb = create_main_kb
        if message.from_user.id in admin_arr:
            kb = create_admin_kb

        await message.answer(f"ФИО наставника: {text}\n\nРегистрация успешно завершина!\n\nВремя приступить к выполнению заданий!", reply_markup=kb)
        await state.update_data(mentor_full_name=text)
        user_data = await state.get_data()
        create_user(session, message.from_user.id, message.from_user.username,
                    user_data["full_name"], user_data["post"], user_data["telephone"], user_data["email"], user_data["mentor_full_name"])
        await state.clear()

    else:
        return await message.answer('Некоректный ввод, введите Имя, Фамилию и Отчество с большой буквы и через пробел соответственно')
