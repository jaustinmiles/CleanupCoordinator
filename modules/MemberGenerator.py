import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app import Member
from app import document_name


def generate_members() -> list:
    """
    Generates a list of Member objects from the document_NAME. Each member's
    data is extracted and stored in a Member. Running total of hours is accessed by
    calling the generate_hours method
    :rtype: list
    :return: list of Member objects
    """

    hours_dict = generate_hours()
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(document_name).get_worksheet(2)
    all_values = sheet.get_all_values()
    col_one = sheet.col_values(1)
    max_row = len(col_one)
    members = []
    for i in range(1, max_row):
        # time.sleep(0.5)
        member_row = all_values[i]
        name_first = member_row[0]
        name_last = member_row[1]
        phone = member_row[2]
        email = member_row[3]
        status = member_row[4]
        active = 'TRUE' in member_row[5]
        hours = hours_dict.get(name_first.strip() + name_last.strip(), -1)
        member = Member(name_first, name_last, phone, email, status, active, hours)
        members.append(member)
        # print(member)
    return members


def generate_hours() -> dict:
    """
    Retrieves the running total of hours for all members from the document_name
    The values are stored in a dictionary where the key is the member's first and last name combined
    :rtype: dict
    :return: dict of hours mapping value 'hours' to key 'last name'
    """
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(document_name).get_worksheet(3)
    all_values = sheet.get_all_values()
    col_one = sheet.col_values(1)
    max_row = len(col_one)
    hours_dict = {}
    for i in range(1, max_row):
        # time.sleep(0.5)
        member_row = all_values[i]
        hours_dict[member_row[0].strip() + member_row[1].strip()] = member_row[2]
    return hours_dict


if __name__ == '__main__':
    # To see output, uncomment print statements in generate_members()
    generate_members()
