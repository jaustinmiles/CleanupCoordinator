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

    def assign_bathrooms(self) -> list:
        """
        This method will only work if the assigner has been instantiated with a list of members already.
        This method must also be called before any regular task assignments or a bathroom may be assigned
        to someone not valid in the floor plan. If there are no bathrooms, there should be an empty list.
        :return: list of (member, cleanup hour) assignments
        """
        bathroom_assigner = BathroomAssigner()
        bathroom_tasks = []
        for i in range(len(self.sorted_tasks) - 1, -1, -1):
            task = self.sorted_tasks[i]
            if 'bathroom' in task.name.lower() and 'servery' not in task.name.lower():
                bathroom_tasks.append(task)
                del self.sorted_tasks[i]
        if not len(self.sorted_tasks):
            self.finished = True
        # if there were no bathrooms
        if not len(bathroom_tasks):
            return []
        results = []
        for task in bathroom_tasks:
            pair = bathroom_assigner.assign_bathroom(task, self.filtered_members)
            if pair is None:
                raise ValueError("There was an issue processing the bathroom tasks. Bathroom assigner found no bathroom"
                                 + "id.")
            results.append(pair)
        results[0][0].assigned = True
        self.filtered_members = filter_members(self.filtered_members)
        return results


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
    from app import MAX_HOURS
    partial_filtered_no_hours = filter_members(member_list)
    partial_filtered_members = [member for member in partial_filtered_no_hours if member.hours < MAX_HOURS]
    sorted_tasks = sorted(task_list, key=lambda x: x.difficulty)
    if len(partial_filtered_members) < len(sorted_tasks):
        raise ValueError(f"There are not enough members to complete the assigned tasks. There are {len(sorted_tasks)}"
                         + f" tasks and {len(partial_filtered_members)} eligible members")
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
    print(filter_members(member_list1))
    # assigner1 = get_assigner(member_list1, sorted_tasks1)
    # bathrooms = assigner1.assign_bathrooms()
    #
    # while not assigner1.finished:
    #     assignment = assigner1.assign_task()
    #     print("########### NEW TASK BELOW ##############\n")
    #     print(assignment[0])
    #     print(assignment[1])
    #     print("########### END OF TASK ##########\n\n\n")
