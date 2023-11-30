from aiogram import Bot, Dispatcher
import asyncio
from database import start_db

telegram_api_key = None
bot = None


def initialize_bot(api_key):
    global telegram_api_key, bot
    telegram_api_key = api_key
    bot = Bot(token=telegram_api_key)


def start(api_key):
    # global list_users, list_scores, list_tasks, list_сonfig
    # list_users, list_scores, list_tasks, list_сonfig = start_table()
    global admin_arr, engine, session
    admin_arr = [821150838, 5189847166, 1258200426, 1364765400, 1153757422]

    initialize_bot(api_key)
    dp = Dispatcher()

    engine, session = start_db()

    from .registration import register_router, register_form_router
    from .cmds_user import user_router, user_form_router
    from .tasks import task_router, task_form_router
    from .cmds_admin import admin_router, admin_form_router

    dp.include_routers(register_router, register_form_router)
    dp.include_routers(user_router, user_form_router)
    dp.include_routers(task_router, task_form_router)
    dp.include_routers(admin_router, admin_form_router)

    try:
        asyncio.run(dp.start_polling(bot))
    except KeyboardInterrupt:
        print('Exit')
