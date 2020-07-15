import time


class Logger:

    FILENAME = "event_log_master.log"
    CONFIRM_EVENT = "confirmed task", "user confirmed task"
    SKIP_EVENT = "skipped task", "user skipped task"
    ASSIGN_EVENT = "assigned task", "user was assigned task"
    SUBMIT_EVENT = "submitted task" "user submitted task to the portal"
    SUBMIT_FAIL_EVENT = "submission failed", "image submission failed"
    SUBMIT_SUCCESS_EVENT = "submission success", "image submission processed"
    APPROVE_EVENT = "approved submission", "user gets credit for hour"
    DENY_EVENT = "denied submission", "user did not receive credit for task"
    DENY_SKIP = "denied skip", "user attempted to skip but has used all skips"

    VALUE_TYPE_SKIP = "skips"
    VALUE_TYPE_HOURS = "completed hours"



if __name__ == '__main__':
    start = time.time()
    l = Logger()
    end = time.time()
    print(end - start)

