import sqlite3
from . import add_try_dec


def create_tasks_table():
    """Создание таблицы tasks."""
    conn = sqlite3.connect('tasks.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task_number INTEGER,
            verified INTEGER,
            points INTEGER,
            photo TEXT DEFAULT NULL,
            text TEXT DEFAULT NULL
        )
    ''')
    conn.commit()
    conn.close()


def connect_to_db():
    """Подключение к базе данных."""
    conn = sqlite3.connect('tasks.db')
    return conn


def close_connection(conn):
    """Закрытие соединения с базой данных."""
    conn.close()


def insert_task_with_photo(user_id, task_number, verified, points, photo):
    """Добавление задания с фотографией."""
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO tasks (user_id, task_number, verified, points, photo)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, task_number, verified, points, photo))
    conn.commit()
    close_connection(conn)


def insert_task_with_text(user_id, task_number, verified, points, text):
    """Добавление задания с текстом."""
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO tasks (user_id, task_number, verified, points, text)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, task_number, verified, points, text))
    conn.commit()
    close_connection(conn)


def insert_task_with_photo_and_text(user_id, task_number, verified, points, photo, text):
    """Добавление задания с фотографией и текстом."""
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO tasks (user_id, task_number, verified, points, photo, text)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, task_number, verified, points, photo, text))
    conn.commit()
    close_connection(conn)


def verify_task(task_id, points):
    """Проверка задания с изменением статуса и баллов."""
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('''
        UPDATE tasks
        SET verified = 1, points = ?
        WHERE id = ?
    ''', (points, task_id))
    conn.commit()
    close_connection(conn)


def get_all_tasks():
    """Получение всех задач из базы данных."""
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    tasks = cur.fetchall()
    close_connection(conn)
    return tasks


def get_unverified_tasks():
    """Получение всех непроверенных задач."""
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks WHERE verified = 0')
    unverified_tasks = cur.fetchall()
    close_connection(conn)
    return unverified_tasks


def get_verified_tasks():
    """Получение всех проверенных задач."""
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks WHERE verified = 1')
    unverified_tasks = cur.fetchall()
    close_connection(conn)
    return unverified_tasks


def get_task_by_id(task_id):
    """Получение информации о задании по его ID."""
    conn = connect_to_db()  # Подключаемся к базе данных
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task_info = cur.fetchone()  # Получаем информацию о задании
    close_connection(conn)  # Закрываем соединение с базой данных
    return task_info


if __name__ == "__main__":

    create_tasks_table()

    a = 0
    if a:
        # Примеры использования функций:
        insert_task_with_photo(123, 1, 1, 10, 'фото1.jpg')
        insert_task_with_text(123, 2, 1, 8, 'Текст задания')
        insert_task_with_photo_and_text(
            123, 3, 1, 12, 'фото2.jpg', 'Другой текст задания')
        # verify_task(1, 9)

    # Получить все задачи
    all_tasks = get_all_tasks()
    print("Все задачи:")
    for task in all_tasks:
        print(task)

    # Получить все непроверенные задачи
    unverified_tasks = get_unverified_tasks()
    print("\nНепроверенные задачи:")
    for task in unverified_tasks:
        print(task)
