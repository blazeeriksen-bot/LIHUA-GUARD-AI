from datetime import datetime


class LihuaLogger:

    def __init__(self):
        self.logs = []


    def record(self, event):

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log = f"[{time}] EVENT: {event}"

        self.logs.append(log)

        print(log)


    def get_logs(self):

        return self.logs