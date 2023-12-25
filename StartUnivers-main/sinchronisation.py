import asyncio
from table import start_table
from database import start_db, Base, User, Points, Tasks
from datetime import datetime


async def update_table_user():
    # Await the asynchronous function
    list_users, list_scores, list_tasks = await start_table()

    # Get the list of users from the database
    users = session.query(User).all()

    for idx, user in enumerate(users):
        tg_id = user.telegram_id
        tg_username = user.telegram_username
        full_name = user.full_name
        post = user.post
        telephone = user.telephone
        e_mail = user.email
        mentor_full_name = user.mentor_full_name

        # user_update
        await list_users.update(f'A{idx + 2}', idx + 1)
        await list_users.update(f'B{idx + 2}', tg_id)
        await list_users.update(f'C{idx + 2}', tg_username)
        await list_users.update(f'D{idx + 2}', full_name)
        await list_users.update(f'E{idx + 2}', post)
        await list_users.update(f'F{idx + 2}', telephone)
        await list_users.update(f'G{idx + 2}', e_mail)
        await list_users.update(f'H{idx + 2}', mentor_full_name)


async def update_table_scores():
    # Await the asynchronous function
    list_users, list_scores, list_tasks = await start_table()

    # Get the list of scores from the database
    points = session.query(Points).all()

    for idx, point in enumerate(points):
        id = point.user_id
        task1 = point.task1
        task2 = point.task2
        task3 = point.task3
        task4 = point.task4
        task5 = point.task5
        task6 = point.task6
        task7 = point.task7
        task8 = point.task8
        task9 = point.task9
        task10 = point.task10

        # scores_update
        await list_scores.update(f'A{idx  + 2}', id)
        await list_scores.update(f'C{idx + 2}', task1)
        await list_scores.update(f'D{idx + 2}', task2)
        await list_scores.update(f'E{idx + 2}', task3)
        await list_scores.update(f'F{idx + 2}', task4)
        await list_scores.update(f'G{idx + 2}', task5)
        await list_scores.update(f'H{idx + 2}', task6)
        await list_scores.update(f'I{idx + 2}', task7)
        await list_scores.update(f'J{idx + 2}', task8)
        await list_scores.update(f'K{idx + 2}', task9)
        await list_scores.update(f'L{idx + 2}', task10)


async def update_table_tasks():
    # Await the asynchronous function
    list_users, list_scores, list_tasks = await start_table()

    # Get the list of task from the database
    tasks = session.query(Tasks).all()

    for idx, task in enumerate(tasks):

        id = task.id
        task_name = task.task_name
        task_description = task.task_description
        task_scores = task.task_scores

        # task_update
        await list_tasks.update(f'A{idx + 2}', id)
        await list_tasks.update(f'B{idx + 2}', task_name)
        await list_tasks.update(f'C{idx + 2}', task_description)
        await list_tasks.update(f'D{idx + 2}', task_scores)


if __name__ == '__main__':
    global engine, session
    engine, session = start_db()
    Base.metadata.create_all(engine)

    last_current_minutes = [59]
    while True:
        current_time = datetime.now()
        current_minute = current_time.minute

        if current_minute % 30 == 0 and last_current_minutes[-1] != current_minute:
            asyncio.run(update_table_user())
            asyncio.run(update_table_scores())
            asyncio.run(update_table_tasks())

            last_current_minutes.append(current_minute)
        
        if current_minute == 59 and last_current_minutes[-1] != current_minute:
            last_current_minutes = [59] 


