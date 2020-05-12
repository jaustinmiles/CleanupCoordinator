import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# from app import DOCUMENT_NAME
from app import CleanupHour, db, Member, basedir, DOCUMENT_NAME, MAX_HOURS

BATHROOM_SHEET = 4
FIRST_COL = 0
LAST_COL = 1
BATHROOM_COL = 2


class BathroomAssigner:

    def __init__(self):
        self.floor_plan = self.generate_floor_plan()

    @staticmethod
    def generate_floor_plan():
        """
        Floor plan is a dictionary that maps a first name and last name concatenated (no space) to the floor
        the member lives on
        :return: the dictionary of mappings
        """
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(basedir, 'client_secret.json'), scope)
        client = gspread.authorize(creds)
        sheet = client.open(DOCUMENT_NAME).get_worksheet(BATHROOM_SHEET)
        all_values = sheet.get_all_values()
        col_one = sheet.col_values(1)
        max_row = len(col_one)
        members = {}
        for i in range(1, max_row):
            member_row = all_values[i]
            name_first = member_row[FIRST_COL].strip()
            name_last = member_row[LAST_COL].strip()
            member = Member.query.filter_by(first=name_first, last=name_last).first()
            if member is None:
                raise ValueError("Member " + name_first + " " + name_last + " is in the floor plan but not in the"
                                                                            + " members list. Please remove him from "
                                                                              "the floor plan or add to the list.")
            bathroom = member_row[BATHROOM_COL].strip()
            members[member.first + member.last] = bathroom
        return members

    def assign_bathroom(self, task: CleanupHour, filtered_members):
        """
        given a task and a list of all members in sorted order, this will assign the task to the first member
        that lives on the floor of the bathroom
        :param task: bathroom task to assign
        :param filtered_members: all eligible members
        :return: member, task pairing for the cleanup hour
        """
        if '2e' in task.name.lower():
            location = '2E'
        elif '2w' in task.name.lower():
            location = '2W'
        elif '3w' in task.name.lower():
            location = '3W'
        elif '3e' in task.name.lower():
            location = '3E'
        else:
            return None
        for member in filtered_members:
            key = member.first + member.last
            if key in self.floor_plan and self.floor_plan[key] == location:
                return member, task
        raise ValueError("The list provided had no members capable of doing this bathroom task: " + task.name)

    def get_members_on_floor(self, task: CleanupHour):
        if '2e' in task.name.lower():
            location = '2E'
        elif '2w' in task.name.lower():
            location = '2W'
        elif '3w' in task.name.lower():
            location = '3W'
        elif '3e' in task.name.lower():
            location = '3E'
        else:
            return None
        floor = [mem for mem, bath in self.floor_plan.items() if bath.lower() == location.lower()]
        all_mems = Member.query.all()
        mem: Member
        final_mems = [mem for mem in all_mems if mem.first + mem.last in floor]
        return final_mems

    def reassign_bathroom(self, task):
        members = self.get_members_on_floor(task)
        members = [m for m in members if not m.assigned and m.hours < MAX_HOURS]
        if len(members):
            return members[0]
        else:
            return None

if __name__ == '__main__':
    assigner = BathroomAssigner()
    # task = CleanupHour('Bathroom 3W', 0, "Monday", "17:00", 1, 2, "")
    # print(assigner.get_members_on_floor(task))
