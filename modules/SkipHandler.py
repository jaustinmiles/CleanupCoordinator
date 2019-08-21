from modules import TextClient
from app import Member, CleanupHour, db, Assignment


"""
Main interface for handling a skip response. The main steps of the process are retrieving the member
object for the member that skipped his hour, retrieve the name of the cleanup hour that was skipped,
and proceed to reassign. Many of the modules used here are also used in the initial wave of cleanup
texts.
"""


def reassign(phone, phone_no_1):
    """
    Given two phone numbers (the same phone number with and without the extension), this method
    will drive the other methods that find the occurrence of the skip based on the phone number,
    generate a new member, re-generate the Task object for the cleanup hour, and use the text
    assigner to send the new Text message. Once the new Assignment is created, it is stored and
    committed to the database.
    :param phone:
    :param phone_no_1:
    """
    task = find_task(phone, phone_no_1)
    member = get_member_object()
    text_client = TextClient.initialize_text_assigner()
    phone = member.phone
    phone_fixed = '+1' + ''.join([char for char in phone if char != '-'])
    pair = Assignment(member.id, task.id, phone_fixed)
    member.assigned = True
    db.session.add(pair)
    db.session.add(member)
    db.session.commit()
    text_client.send_assignment((member, task), pair.id)


def get_member_object():
    """
    This method finds the member that needs hours the most that is active and has not been assigned one.
    :return: correctly Generated member object, or None in case of failure
    """
    members = Member.query.all()
    sorted_members = sorted(members, key=lambda x: x.hours)
    for member in sorted_members:
        if member.active and not member.assigned:
            return member
    return None


def find_task(phone, phone_no_1):
    """
    Find task will attempt to find the task based on a phone number by examining assignments from the db. If the
    phone number on the initial assignment is found, then the task object should be returned to signify the task
    :param phone: number with extension
    :param phone_no_1: number without extension
    :return: the task that needs to be reassigned
    """
    assignments = Assignment.query.all()
    for assignment in assignments:
        if assignment.phone_number == phone or assignment.phone_number == phone_no_1:
            task = CleanupHour.query.get(assignment.task_id)
            return task
    print('Cleanup hour object could not be retrieved.')
    return None


if __name__ == '__main__':
    reassign('+14702637816', '14702637816')
