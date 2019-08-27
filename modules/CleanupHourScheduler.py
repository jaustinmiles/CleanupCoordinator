import gspread
from app import CleanupHour
from app import DOCUMENT_NAME

from oauth2client.service_account import ServiceAccountCredentials


def schedule_hours() -> list:
    """
    Retrieves the weekly cleanup-hour schedule from the document_name
    and formats the table into a list of CleanupHour objects
    :rtype: list
    :return: list of CleanupHour objects
    """
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(DOCUMENT_NAME).get_worksheet(1)
    all_values = sheet.get_all_values()
    col_one = sheet.col_values(1)
    max_row = len(col_one)
    hours_list = []
    for i in range(1, max_row):
        row = all_values[i]
        name = row[0]
        task_id = row[1]
        day = row[2]
        due_time = row[3]
        worth = row[4]
        difficulty = row[5]
        link = row[6]
        hour = CleanupHour(name, task_id, day, due_time, worth, difficulty, link)
        # print(hour)
        hours_list.append(hour)
    return hours_list


if __name__ == '__main__':
    # To see output, uncomment statement in schedule_hours()
    schedule_hours()
