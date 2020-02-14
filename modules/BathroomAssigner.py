import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# from app import DOCUMENT_NAME
from app import CleanupHour, db, Member, basedir, DOCUMENT_NAME

BATHROOM_SHEET = 4
FIRST_COL = 0
LAST_COL = 1
BATHROOM_COL = 2


class BathroomAssigner:

    def __init__(self):
        self.floor_plan = self.generate_floor_plan()

    @staticmethod
    def generate_floor_plan():
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(basedir, 'client_secret.json'), scope)
        client = gspread.authorize(creds)
        sheet = client.open(DOCUMENT_NAME).get_worksheet(BATHROOM_SHEET)
        all_values = sheet.get_all_values()
        col_one = sheet.col_values(1)
        max_row = len(col_one)
        members = []
        for i in range(1, max_row):
            member_row = all_values[i]
            name_first = member_row[FIRST_COL].strip()
            name_last = member_row[LAST_COL].strip()
            member = Member.query.filter_by(first=name_first, last=name_last).first()
            if member is None:
                print(name_first + " " + name_last)
                continue
            hours = member.hours
            bathroom = member_row[BATHROOM_COL].strip()
            members.append((member, bathroom, hours))
        members = sorted(members, key=lambda x: x[2])
        return members

    def assign_bathroom(self, task: CleanupHour):
        if '2e' in task.name.lower():
            location = '2E'
        elif '2w' in task.name.lower():
            location = '2W'
        elif '3w' in task.name.lower():
            location = '3W'
        elif '3E' in task.name.lower():
            location = '3E'
        else:
            return None
        for member_pair in self.floor_plan:
            if member_pair[1] == location:
                return (member_pair[0], task)


if __name__ == '__main__':
    assigner = BathroomAssigner()
    print(assigner.floor_plan)
