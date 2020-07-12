import os
import time

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")


class Logger:

    FILENAME = "event_log_master.log"
    LOG_PATH = os.path.join(basedir, "static", "logs")
    CONFIRM_EVENT = "Confirmed task"
    SKIP_EVENT = "Skipped task"
    ASSIGN_EVENT = "Assigned task"
    SUBMIT_EVENT = "Submitted task"
    APPROVE_EVENT = "Approved submission"
    DENY_EVENT = "Denied submission"

    def __init__(self):
        if not os.path.exists(self.LOG_PATH):
            os.mkdir(self.LOG_PATH)


if __name__ == '__main__':
    start = time.time()
    l = Logger()
    end = time.time()
    print(end - start)

