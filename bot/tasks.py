from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from .keyboard import create_pass_kb, create_tasks_kb, create_ver_keyboard
from database import get_tasks, get_task, get_points, add_try, verify, ver_state_sum
from database.task import *

from . import session, admin_arr


task_router = Router()
task_form_router = Router()


class pass_text(StatesGroup):
    text = State()
    photo = State()


class points(StatesGroup):
    points = State()


async def set_state(number):
    if number == 0:
        return 'Задание не отправленно'
    if number == 1:
        return 'Задание на проверке'
    if number == 2:
        return 'Задание сдано и проверено, сдать больше нельзя'
    if number > 2:
        return f'Задание сдано и проверено, но можно сдать ещё'
    return f'Сдано и проверено, но для зачёта необходимо сдать ещё {abs(number)} раз(а)'


@task_router.message(F.text == "Задания")
async def cmd_user_tasks(message: Message):
    tasks = get_tasks(session)
    keyboard = create_tasks_kb(tasks)
    await message.answer(f'Задания:', reply_markup=keyboard)


@task_router.callback_query(F.data.startswith('task_'))
async def cmd_task(callback: CallbackQuery):
    task_id = callback.data.replace('task_', '')
    task = get_task(session, task_id)

    text = f"Название: <b>{task.name}</b>\n" \
        f"Описание: <b>{task.description}</b>\n" \
        f"Формат сдачи задания: <b>{'текст' if task.input[0] == 'text' and len(task.input) == 1 else ('фото' if task.input[0] == 'photo' and len(task.input) == 1 else 'текст и фото')}</b>\n" \
        f"Нужно сдать для зачёта: <b>{task.necessarily_scores}</b>\n" \
        f"Максимальное количество баллов: <b>{task.max_scores * task.forone_scores}</b>\n\n"

    if callback.from_user.id in admin_arr:
        return await callback.message.answer(
            text,
            parse_mode="HTML"
        )

    if task_id == '1':
        task_i = points.task1
        implementations_i = points.implementations1
        state_i = await set_state(points.state1)
    if task_id == '2':
        task_i = points.task2
        implementations_i = points.implementations2
        state_i = await set_state(points.state2)
    if task_id == '3':
        task_i = points.task3
        implementations_i = points.implementations3
        state_i = await set_state(points.state3)
    if task_id == '4':
        task_i = points.task4
        implementations_i = points.implementations4
        state_i = await set_state(points.state4)
    if task_id == '5':
        task_i = points.task5
        implementations_i = points.implementations5
        state_i = await set_state(points.state5)
    if task_id == '6':
        task_i = points.task6
        implementations_i = points.implementations6
        state_i = await set_state(points.state6)
    if task_id == '7':
        task_i = points.task7
        implementations_i = points.implementations7
        state_i = await set_state(points.state7)
    if task_id == '8':
        task_i = points.task8
        implementations_i = points.implementations8
        state_i = await set_state(points.state8)
    if task_id == '9':
        task_i = points.task9
        implementations_i = points.implementations9
        state_i = await set_state(points.state9)
    if task_id == '10':
        task_i = points.task10
        implementations_i = points.implementations10
        state_i = await set_state(points.state10)

    points = get_points(session, callback.from_user.id)

    await callback.answer(f'Вы выбрали {task.name}')

    if not task:
        return await callback.message.answer(
            f"ошибка"
        )

    if callback.from_user.id not in admin_arr:
        text += f"Сдано раз: <b>{implementations_i}/{task.max_scores}</b>\n"
        text += f"Количество набранных баллов: <b>{task_i}</b>\n"
        text += f"Состояние задания: <b>{state_i}</b>"

    if implementations_i == task.max_scores or callback.from_user.id in admin_arr:
        return await callback.message.answer(
            text,
            parse_mode="HTML"
        )

    kb = create_pass_kb(task_id)
    await callback.message.answer(
        text,
        parse_mode="HTML",
        reply_markup=kb
    )


@task_router.callback_query(F.data.startswith('pass_'))
async def cmd_task_pass(callback: CallbackQuery, state: FSMContext) -> None:
    task_id = callback.data.replace('pass_', '')
    await state.update_data(task_id=task_id)
    task = get_task(session, task_id)
    points = get_points(session, callback.from_user.id)

    if task_id == '1':
        implementations_i = points.implementations1
    if task_id == '2':
        implementations_i = points.implementations2
    if task_id == '3':
        implementations_i = points.implementations3
    if task_id == '4':
        implementations_i = points.implementations4
    if task_id == '5':
        implementations_i = points.implementations5
    if task_id == '6':
        implementations_i = points.implementations6
    if task_id == '7':
        implementations_i = points.implementations7
    if task_id == '8':
        implementations_i = points.implementations8
    if task_id == '9':
        implementations_i = points.implementations9
    if task_id == '10':
        implementations_i = points.implementations10

    if implementations_i == task.max_scores:
        return await callback.message.answer(
            f"Вы не можете отправлять это задание"
        )
    task = get_task(session, task_id)
    await state.update_data(arr_input=task.input)
    if not task:
        await callback.message.answer(
            f"ошибка"
        )
    user_data = await state.get_data()
    if user_data['arr_input'][0] == 'text':
        await state.set_state(pass_text.text)
        await callback.message.answer(
            f"Отправьте текст - решение задания. Для отмены /cancel"
        )
    else:
        await state.set_state(pass_text.photo)
        await callback.message.answer(
            f"Отправьте фото - решение задания. Для отмены /cancel"
        )


@task_form_router.message(pass_text.text, F.text)
async def cmd_task_pass_text(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    user_data = await state.get_data()
    if len(user_data['arr_input']) == 1:
        add_try(session, message.from_user.id, user_data['task_id'])
        insert_task_with_text(message.from_user.id,
                              user_data['task_id'], 0, 0, user_data['text'])
        await message.answer(
            f"Ваш ответ принят!"
        )
        await state.clear()
    else:
        await message.answer(
            f"Отправьте фото - решение задания. Для отмены /cancel"
        )
        await state.set_state(pass_text.photo)


@task_form_router.message(pass_text.photo, F.photo)
async def cmd_task_pass_text(message: Message, state: FSMContext) -> None:
    photo = message.photo[-1].file_id
    user_data = await state.get_data()
    add_try(session, message.from_user.id, user_data['task_id'])
    if len(user_data['arr_input']) == 1:
        insert_task_with_photo(message.from_user.id,
                               user_data['task_id'], 0, 0, photo)
    else:
        insert_task_with_photo_and_text(
            message.from_user.id, user_data['task_id'], 0, 0, photo, user_data['text'])
    await message.answer(
        f"Ваш ответ принят!"
    )
    await state.clear()


@task_router.callback_query(F.data.startswith('adm_choose_task_unver_'))
async def tasks_prev_page(callback: CallbackQuery):
    task_try = callback.data.replace('adm_choose_task_unver_', '')
    task = get_task_by_id(task_try)
    await callback.answer(f'Вы выбрали {task_try}')
    text = f'Номер сдачи {task[0]}\n' \
           f'Номер задания {task[2]}\n\n'

    txt = task[6]
    photo = task[5]

    kb = create_ver_keyboard(task[0])

    if photo == None:
        text += f'Ответ: {txt}'
        await callback.message.answer(text, reply_markup=kb)
    elif txt == None:
        await callback.message.answer_photo(photo, text, reply_markup=kb)
    else:
        text += f'Ответ: {txt}'
        await callback.message.answer_photo(photo, text, reply_markup=kb)


@task_router.callback_query(F.data.startswith('adm_choose_task_ver_'))
async def tasks__page(callback: CallbackQuery):
    task_try = callback.data.replace('adm_choose_task_ver_', '')
    task = get_task_by_id(task_try)
    await callback.answer(f'Вы выбрали {task_try}')
    text = f'Номер сдачи {task[0]}\n' \
           f'Номер задания {task[2]}\n\n'

    txt = task[6]
    photo = task[5]

    if photo == None:
        text += f'Ответ: {txt}'
        await callback.message.answer(text)
    elif txt == None:
        await callback.message.answer_photo(photo, text)
    else:
        text += f'Ответ: {txt}'
        await callback.message.answer_photo(photo, text)


@task_router.callback_query(F.data.startswith('show_text_'))
async def cmd_adm(callback: CallbackQuery):
    id = callback.data.replace('show_text_', '')
    await callback.answer(f'Вы выбрали {id}')
    if not id:
        return await callback.message.answer(
            f"ошибка"
        )
    task = get_task_by_id(id)
    task = get_task(session, task[2])
    await callback.message.answer(
        f"Текст задания:\n{task.description}"
    )


@task_router.callback_query(F.data.startswith('unver_'))
async def cmd_adm(callback: CallbackQuery):
    id = callback.data.replace('unver_', '')
    await callback.answer(f'Вы выбрали {id}')
    if not id:
        return await callback.message.answer(
            f"ошибка"
        )
    task = get_task_by_id(id)
    if task[3] == 1:
        return await callback.message.answer(
            f"Это решение уже оценено"
        )
    verify(session, task[1], task[2], 0)
    verify_task(id, 0)
    ver_state_sum(session, callback.from_user.id)
    await callback.message.answer(
        "За это решение выдано 0 баллов"
    )


@task_router.callback_query(F.data.startswith('ver_full_'))
async def cmd_adm(callback: CallbackQuery):
    id = callback.data.replace('ver_full_', '')
    await callback.answer(f'Вы выбрали {id}')
    if not id:
        return await callback.message.answer(
            f"ошибка"
        )
    task = get_task_by_id(id)
    if task[3] == 1:
        return await callback.message.answer(
            f"Это решение уже оценено"
        )
    task_points = get_task(session, task[2]).forone_scores
    verify(session, task[1], task[2], task_points)
    verify_task(id, task_points)
    ver_state_sum(session, callback.from_user.id)
    await callback.message.answer(
        f"За это решение выдано {task_points} баллов"
    )


@task_router.callback_query(F.data.startswith('ver_nofull_'))
async def cmd_adm(callback: CallbackQuery, state: FSMContext) -> None:
    id = callback.data.replace('ver_nofull_', '')
    await state.update_data(id_adm_task=id)
    await callback.answer(f'Вы выбрали {id}')
    if not id:
        return await callback.message.answer(
            f"ошибка"
        )
    task = get_task_by_id(id)
    if task[3] == 1:
        return await callback.message.answer(
            f"Это решение уже оценено"
        )
    task_points = get_task(session, task[2]).forone_scores
    await callback.message.answer(
        f"Введите вашу оценку за это решение от 0 до {task_points}. Для отмены /cancel"
    )
    await state.set_state(points.points)


@task_form_router.message(points.points, F.text)
async def cmd_task_pass_text(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    id = user_data['id_adm_task']
    if not id:
        return await message.answer(
            f"ошибка"
        )
    points = message.text
    try:
        points = int(points)
    except:
        return await message.answer(
            f"Вы ввели не число"
        )
    task = get_task_by_id(id)
    task_points = get_task(session, task[2]).forone_scores
    if points >= task_points:
        return await message.answer(
            f"Вы ввели максимальный, или больше, балл"
        )
    if points <= 0:
        return await message.answer(
            f"Вы ввели 0, или меньше"
        )
    verify(session, task[1], task[2], points)
    verify_task(id, points)
    ver_state_sum(session, message.from_user.id)

    await message.answer(
        f"За это решение выдано {points} баллов"
    )
    await state.clear()
