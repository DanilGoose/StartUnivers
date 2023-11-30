import asyncio

import gspread_asyncio

from google.oauth2.service_account import Credentials


def get_creds():
    creds = Credentials.from_service_account_file("creds.json")
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    return scoped


async def start_table():
    agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)
    agc = await agcm.authorize()

    sheet = await agc.open('StartUnivers')

    list_users = await sheet.get_worksheet(0)
    list_scores = await sheet.get_worksheet(1)
    list_tasks = await sheet.get_worksheet(2)

    return list_users, list_scores, list_tasks


async def get_the_number_of_users(list_users):
    the_number_of_users = await list_users.get('K1')
    return int(the_number_of_users[0][0])


async def create_user(list_users, list_scores, idd, tg_id, tg_username, full_name, post, telephone, e_mail, mentor_full_name):
    await list_users.update(f'A{idd+1}', idd)
    await list_users.update(f'B{idd+1}', tg_id)
    await list_users.update(f'C{idd+1}', tg_username)
    await list_users.update(f'D{idd+1}', full_name)
    await list_users.update(f'E{idd+1}', post)
    await list_users.update(f'F{idd+1}', telephone)
    await list_users.update(f'G{idd+1}', e_mail)
    await list_users.update(f'H{idd+1}', mentor_full_name)

    await list_scores.update(f'A{idd+1}', idd)
    for column in range(2, 17):
        column_letter = chr(ord('A') + column - 1)
        await list_scores.update(f'{column_letter}{idd+1}', 0)

# тест


async def main():
    list_users, list_scores, list_tasks, list_сonfig = await start_table()

if __name__ == '__main__':
    asyncio.run(main(), debug=True)
