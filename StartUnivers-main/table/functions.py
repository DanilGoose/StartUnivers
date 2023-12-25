def get_the_number_of_users(list_users):
    the_number_of_users = list_users.get_value('K1', 'FORMATTED_VALUE')
    return the_number_of_users


async def create_user(list_users, list_scores, idd, tg_id, tg_username, full_name, post, telephone, e_mail, mentor_full_name):
    list_users.update_value(f'A{idd+1}', idd)
    list_users.update_value(f'B{idd+1}', tg_id)
    list_users.update_value(f'C{idd+1}', tg_username)
    list_users.update_value(f'D{idd+1}', full_name)
    list_users.update_value(f'E{idd+1}', post)
    list_users.update_value(f'F{idd+1}', telephone)
    list_users.update_value(f'G{idd+1}', e_mail)
    list_users.update_value(f'H{idd+1}', mentor_full_name)

    list_scores.update_value(f'A{idd+1}', idd)
    for column in range(2, 17):
        column_letter = chr(ord('A') + column - 1)
        list_scores.update_value(f'{column_letter}{idd+1}', 0)
