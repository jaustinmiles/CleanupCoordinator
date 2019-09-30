from modules import MemberGenerator
from modules import CleanupHourScheduler
from modules.BathroomAssigner import BathroomAssigner


class Assigner:

    def __init__(self, filtered_members: list, sorted_tasks: list):
        """
        The Assigner is responsible for assigning tasks until both input lists are
        empty. It takes in two lists - one of Members, and one of CleanupHours, each
        of the same length. Once a task has been completed, it is deleted. When both
        of the lists are empty, the 'finished' flag is set to True.
        NOTE: the filtered_members list MUST be the same length as the sorted_tasks, and
        it MUST be sorted in the following manner:
            1. The members must first be sorted by number of cleanup hours in their running total.
            2. All but the first len(sorted_tasks) amount of tasks must be deleted
            3. The remaining members should be sorted based on status
        NOTE: the sorted_tasks list is sorted by CleanupHour.difficulty
        :param filtered_members: sorted list of Members from MemberGenerator, see above for
                specifications
        :param sorted_tasks: sorted list of CleanupHours from the CleanupHourScheduler, see
                above for specifications
        """
        self.filtered_members = filtered_members
        self.sorted_tasks = sorted_tasks
        self.finished = len(self.filtered_members) == 0

    def assign_task(self) -> tuple:
        """
        Assigns a cleanup task to a member. Given the sorted lists in the Assigner,
        the first element of each is returned in a (Member, CleanupHour) tuple. These
        elements are then deleted from their respective lists
        :rtype: tuple
        :return: (Member, CleanupHour) tuple
        """
        if len(self.filtered_members) == 0 or len(self.sorted_tasks) == 0:
            return -1, -1
        else:
            task = self.sorted_tasks[0]
            member = self.filtered_members[0]
            del self.filtered_members[0]
            del self.sorted_tasks[0]
            if len(self.filtered_members) == 0 or len(self.sorted_tasks) == 0:
                self.finished = True
            return member, task

    def assign_bathrooms(self):
        bathroom_assigner = BathroomAssigner()
        bathrooms = []
        indices_to_remove = []
        for i, task in enumerate(self.sorted_tasks):
            if 'bathroom' in task.name.lower() and 'servery' not in task.name.lower():
                pair = bathroom_assigner.assign_bathroom(task)
                if pair is None:
                    print(task)
                    raise AssertionError("There was no one to assign this bathroom task, or the algorithm failed")
                bathrooms.append(pair)
                pair[0].assigned = True
                indices_to_remove.append(i)
        for i in range(len(indices_to_remove) - 1, -1, -1):
            del self.sorted_tasks[indices_to_remove[i]]
        # TODO: fix result of member not being deleted due to shallow copy of object
        for i in range(len(self.filtered_members) - 1, -1, -1):
            if self.filtered_members[i].assigned:
                del self.filtered_members[i]
        return bathrooms


def get_assigner(member_list: list, task_list: list) -> Assigner:
    """
    Initializes the assigner and returns it
    :rtype: Assigner
    :param member_list: list of members from MemberGenerator
    :param task_list: list of cleanup hours from CleanupHourScheduler
    :return: the assigner
    """
    assigner = initialize_assigner(member_list, task_list)
    return assigner


def initialize_assigner(member_list, task_list) -> Assigner:
    """
    Initializes the assigner. In this function call, the member_list and
    task_list are both sorted according to the specifications dictated in the
    Assigner __init__ documentation
    :rtype: Assigner
    :param member_list: list of members from MemberGenerator
    :param task_list: list of cleanup hours from CleanupHourScheduler
    :return: the assigner
    """
    partial_filtered_members = filter_members(member_list)
    sorted_tasks = sorted(task_list, key=lambda x: x.difficulty)
    filtered_members = []
    for i in range(len(sorted_tasks)):
        filtered_members.append(partial_filtered_members[i])
    final_members = sorted(filtered_members, key=lambda member: member.member_status())
    assigner = Assigner(final_members, sorted_tasks)
    return assigner


def filter_members(member_list) -> list:
    """
    Helper function to filter the member_list. Removes all inactive members from the
    list and sorts the remaining members by the number of cleanup hours they have. The
    list will be trimmed down to the correct size and filtered by status in initialize_assigner
    :rtype: list
    :param member_list:
    :return: partially sorted members
    """
    sorted_members = sorted(member_list, key=lambda x: x.hours)
    final_list = [member for member in sorted_members if member.active and not member.assigned]
    return final_list


if __name__ == '__main__':
    member_list1 = MemberGenerator.generate_members()
    sorted_tasks1 = CleanupHourScheduler.schedule_hours()
    assigner1 = get_assigner(member_list1, sorted_tasks1)
    bathrooms = assigner1.assign_bathrooms()
    for bathroom in bathrooms:
        print(bathroom[0].first + bathroom[0].last + str(bathroom[0].hours))
        print(bathroom[1].name)
    for task in assigner1.sorted_tasks:
        print(task.name)
    for member in assigner1.filtered_members:
        print(member.first + " " + member.last)
    # while not assigner1.finished:
    #     assignment = assigner1.assign_task()
    #     print("########### NEW TASK BELOW ##############\n")
    #     print(assignment[0])
    #     print(assignment[1])
    #     print("########### END OF TASK ##########\n\n\n")
