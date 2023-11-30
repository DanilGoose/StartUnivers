from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)
    telegram_username = Column(String)
    full_name = Column(String)
    post = Column(String)
    telephone = Column(String)
    email = Column(String)
    mentor_full_name = Column(String)

    points = relationship("Points", back_populates="user")


class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    input = Column(ARRAY(String))

    '''
    какие могут быть элементы инпут (справочная инфа)
    - text
    - photo
    (если несколько вводов то несколько элементов масива)
    '''

    info = Column(String)
    forone_scores = Column(Integer)
    necessarily_scores = Column(Integer)
    max_scores = Column(Integer)


class Points(Base):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), unique=True)

    task1 = Column(Integer, default=0)
    implementations1 = Column(Integer, default=0)
    state1 = Column(Integer, default=0)

    task2 = Column(Integer, default=0)
    implementations2 = Column(Integer, default=0)
    state2 = Column(Integer, default=0)

    task3 = Column(Integer, default=0)
    implementations3 = Column(Integer, default=0)
    state3 = Column(Integer, default=0)

    task4 = Column(Integer, default=0)
    implementations4 = Column(Integer, default=0)
    state4 = Column(Integer, default=0)

    task5 = Column(Integer, default=0)
    implementations5 = Column(Integer, default=0)
    state5 = Column(Integer, default=0)

    task6 = Column(Integer, default=0)
    implementations6 = Column(Integer, default=0)
    state6 = Column(Integer, default=0)

    task7 = Column(Integer, default=0)
    implementations7 = Column(Integer, default=0)
    state7 = Column(Integer, default=0)

    task8 = Column(Integer, default=0)
    implementations8 = Column(Integer, default=0)
    state8 = Column(Integer, default=0)

    task9 = Column(Integer, default=0)
    implementations9 = Column(Integer, default=0)
    state9 = Column(Integer, default=0)

    task10 = Column(Integer, default=0)
    implementations10 = Column(Integer, default=0)
    state10 = Column(Integer, default=0)

    sum = Column(Integer, default=0)
    state_sum = Column(Integer, default=0)

    user = relationship("User", back_populates="points")


def start_db():
    engine = create_engine(
        'postgresql://default:gUIu2DXdW4eb@ep-jolly-limit-71386765.eu-central-1.postgres.vercel-storage.com:5432/verceldb')
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session


def delete_user(session, telegram_id):
    try:
        user_for_delete = session.query(User).filter(
            User.telegram_id == telegram_id).one()
        session.delete(user_for_delete)
        session.commit()
    except NoResultFound:
        print("what's your name bro? My name? Yes, your name. So... Ovoveveve enetyonveve ogbymygbyn Osas (error)")


def check_id(session, telegram_id):
    try:
        user_for_found = session.query(User).filter(
            User.telegram_id == telegram_id).one()
        return True
    except:
        return False


def get_number_of_users(session):
    return session.query(User).count()


def print_all_users(session):
    users = session.query(User).all()
    for user in users:
        print(
            f"ID: {user.id}, Telegram ID: {user.telegram_id}, Telegram Username: {user.telegram_username}")
        print(f"Full Name: {user.full_name}")
        print(f"Telephone: {user.telephone}, Email: {user.email}")
        print(f"Mentor Full Name: {user.mentor_full_name}\n")


def get_users(session):
    users = session.query(User).all()
    return users


def get_user(session, id):
    user = session.query(User).filter(User.id == id).one()
    return user


def get_user_tg(session, id):
    user = session.query(User).filter(User.telegram_id == id).one()
    return user


def get_points(session, id):
    user = session.query(User).filter(User.telegram_id == id).one()
    points = session.query(Points).filter(Points.user_id == user.id).one()
    return points


def create_user(session, telegram_id, telegram_username, full_name, post, telephone, email, mentor_full_name):
    new_user = User(
        telegram_id=telegram_id,
        telegram_username=telegram_username,
        full_name=full_name,
        post=post,
        telephone=telephone,
        email=email,
        mentor_full_name=mentor_full_name
    )

    points = Points(user=new_user)

    new_user.points.append(points)

    session.add(new_user)
    session.commit()

    return new_user


def create_task(session, task_name, task_description, task_input, task_info, task_forone_scores, task_necessarily_scores, task_max_scores):
    new_task = Tasks(
        name=task_name,
        description=task_description,
        input=task_input,
        info=task_info,
        forone_scores=task_forone_scores,
        necessarily_scores=task_necessarily_scores,
        max_scores=task_max_scores
    )

    session.add(new_task)
    session.commit()

    return new_task


def get_tasks(session):
    tasks = session.query(Tasks).all()
    return tasks


def get_task(session, id):
    task = session.query(Tasks).filter(Tasks.id == id).one()
    return task


def add_try(session, telegram_id, task_number):
    points = get_points(session, telegram_id)

    # Проверим, существует ли у пользователя столбец для этого задания
    task_column_name = f'implementations{task_number}'
    if hasattr(points, task_column_name):
        # Увеличим попытку и установим состояние
        task_attempts = getattr(points, task_column_name) + 1
        setattr(points, task_column_name, task_attempts)
        setattr(points, f'state{task_number}', 1)

        # Сохранить изменения
        session.commit()
    else:
        print(
            f"Задание с номером {task_number} не существует для пользователя")
        

def add_try_dec(session, telegram_id, task_number):
    points = get_points(session, telegram_id)

    # Проверим, существует ли у пользователя столбец для этого задания
    task_column_name = f'implementations{task_number}'
    if hasattr(points, task_column_name):
        # Увеличим попытку и установим состояние
        task_attempts = getattr(points, task_column_name) - 1
        setattr(points, task_column_name, task_attempts)
        setattr(points, f'state{task_number}', 1)

        # Сохранить изменения
        session.commit()
    else:
        print(
            f"Задание с номером {task_number} не существует для пользователя")


def verify(session, telegram_id, task_number, points_set):
    if points_set == 0:
        add_try_dec(session, telegram_id, task_number) 
    try:
        points = get_points(session, telegram_id)
        task = get_task(session, task_number)
        # Check if the task_number is valid (between 1 and 10)
        if 1 <= task_number <= 10:
            task_column_name = f'task{task_number}'
            implementations_column_name = f'implementations{task_number}'
            state_column_name = f'state{task_number}'

            if hasattr(points, task_column_name):
                # Update the state and points
                implementations = getattr(points, implementations_column_name)
                if implementations == task.max_scores:
                    setattr(points, state_column_name, 2)
                elif implementations >= task.necessarily_scores:
                    setattr(points, state_column_name, 3)
                else:
                    setattr(points, state_column_name,
                            (task.necessarily_scores - implementations) * -1)

                task_points = getattr(points, task_column_name)
                setattr(points, task_column_name, task_points + points_set)

                # Update the total points
                total_points = getattr(points, 'sum')
                setattr(points, 'sum', total_points + points_set)

                # Save the changes
                session.commit()

                print(f"Task {task_number} verified successfully.")
            else:
                print(f"Task {task_number} does not exist for this user.")
        else:
            print("Invalid task number. Task number must be between 1 and 10.")
    except Exception as e:
        print(f"Error verifying task: {e}")


def ver_state_sum(session, telegram_id):
    points = get_points(session, telegram_id)

    for i in range(1, 11):
        implementations_column_name = f'implementations{i}'
        task = get_task(session, i)
        if task.necessarily_scores < getattr(points, implementations_column_name):
            break
    else:
        setattr(points, 'state_sum', 1)


# тест
if __name__ == '__main__':
    engine, session = start_db()
    Base.metadata.create_all(engine)

    # new_user = create_user(
    #     session,
    #     telegram_id=1234,
    #     telegram_username='john_doe',
    #     full_name='John Doe',
    #     post='Developer',
    #     telephone='123-456-7890',
    #     email='john.doe@example.com',
    #     mentor_full_name='Jane Smith'
    # )

    # print(
    #     f"Создан пользователь с именем '{new_user.full_name}' и email '{new_user.email}'")

    create_task(session, 'Уроки коллег',
                'Сходив на урок к опытному коллеге, вы наверняка увидите интересный прием, технологию или способ работы. Опишите, что из увиденного вы сможете применять в своей работе.',
                ['text'], 'нету', 5, 4, 4)
    create_task(session, 'Мастерская',
                'Выберите одну из мастерских на этот учебный год. С каждого занятия присылайте фото одного из заданий, которое вы там выполняли, подпишите дату и название мастерской.',
                ['photo'], 'нету', 7, 3, 6)
    create_task(session, 'Открытые уроки',
                'Вам предстоит приглашать на свои уроки наставника, методиста, коллег. После каждого такого урока и его обсуждения, запишите здесь, что удалось вам лучше всего.',
                ['text'], 'нету', 10, 1, 4)
    create_task(session, 'Пед. наблюдение',
                'Опишите ситуацию, которую вы увидели или были участником, где вы увидели особенности возраста, с которым работаете.',
                ['text'], 'нету', 7, 2, 3)
    create_task(session, 'Чтение',
                'Прочитайте книгу из предложенного списка и выделите наиболее интересные для вас цитаты. Цитаты нужно разместить на доске в учительской, сфотографировать это и прислать  сюда. (Тут будет ссылка на диск с текстами)',
                ['photo'], 'нету', 5, 1, 4)
    create_task(session, 'Посты о Гимназии',
                'Напишите пост о событии в жизни Гимназии или  своих впечатлениях о буднях в школе. Скриншот публикации прикрепите здесь.',
                ['photo'], 'нету', 5, 1, 2)
    create_task(session, 'Клубы',
                'Выберите один из клубов для учителей и посетите занятие. Сделайте там селфи с коллегами и пришлите сюда, подписав дату и название клуба. (Будет прикреплёно расписание клубов)',
                ['photo'], 'нету', 5, 0, 4)
    create_task(session, 'Организация событий',
                'Организуйте или поучаствуйте в проведении события для сотрудников гимназии.  Опишите коротко замысел мероприятия и  свою роль в команде.',
                ['text'], 'нету', 15, 0, 1)
    create_task(session, 'Выступления с учителями',
                'Отзовитесь на приглашение поучаствовать в любой – спортивной, творческой, интеллектуальной, трудовой команде учителей школы. Коротко опишите событие, в котором участвовали и наиболее яркое впечатление от коллег. Добавьте к описанию фото.',
                ['text', 'photo'], 'нету', 7, 0, 2)
    create_task(session, 'Особые встречи',
                'Получив приглашение на встречу для молодых педагогов, не пропустите его. Сделайте там общее фото и пришлите его, подписав дату и тему встречи. (Будет прикреплён список встреч на четверть)',
                ['photo'], 'нету', 10, 0, 1)

    tasks = session.query(Tasks).all()
    for task in tasks:
        print(
            f"ID: {task.id}, Name: {task.name}, Description: {task.description}, Scores: {task.max_scores}\n\n{task.input}")

    print("\nСписок всех пользователей:")
    print_all_users(session)

    number_of_users = get_number_of_users(session)
    print(f"\nВсего пользователей: {number_of_users}")
