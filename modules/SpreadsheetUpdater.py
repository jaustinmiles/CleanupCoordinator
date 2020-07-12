from app import DOCUMENT_NAME, Member
from modules.MemberGenerator import get_google_creds

RUNNING_TOTAL_COL = 3
SKIPS_TOTAL_COL = 4


def update_hours():
    """
    update_hours is responsible for transporting data from the database to the Google sheet as specified by
    document_name, updating the 'Running total' worksheet. If the first and last name specified in the
    spreadsheet corresponds to a Member model in the db, the hours are updated in the correct column.
    """
    client = get_google_creds()
    sheet = client.open(DOCUMENT_NAME).get_worksheet(3)
    all_values = sheet.get_all_values()
    col_one = sheet.col_values(1)
    max_row = len(col_one)
    for i in range(1, max_row):
        member_row = all_values[i]
        first_name = member_row[0].strip()
        last_name = member_row[1].strip()
        member = Member.query.filter_by(first=first_name, last=last_name).first()
        if member is not None:
            if not member.assigned:
                continue
            # the sheet is indexed starting at 0, unlike the list from get_all_values. Adding 1 ensures proper indexing
            sheet.update_cell(i + 1, RUNNING_TOTAL_COL, member.hours)
            sheet.update_cell(i + 1, SKIPS_TOTAL_COL, member.skips)


if __name__ == '__main__':
    update_hours()
