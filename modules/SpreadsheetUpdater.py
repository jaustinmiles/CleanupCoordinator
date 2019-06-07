import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app import document_name, Member


def update_hours():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(document_name).get_worksheet(3)
    all_values = sheet.get_all_values()
    col_one = sheet.col_values(1)
    max_row = len(col_one)
    for i in range(1, max_row):
        member_row = all_values[i]
        first_name = member_row[0].strip()
        last_name = member_row[1].strip()
        member = Member.query.filter_by(first=first_name, last=last_name).first()
        if member is not None:
            hours = member.hours
            sheet.update_cell(i + 1, 3, hours)


if __name__ == '__main__':
    update_hours()
