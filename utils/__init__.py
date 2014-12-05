from datetime import datetime

class DateTimeUtil:
    format = '%Y-%m-%dT%H:%M:%S'

    def __init__(self):
        pass

    def get_difference_as_seconds(self, datetime1, datetime2):
        datetime1 = datetime.strptime(datetime1, self.format)
        datetime2 = datetime.strptime(datetime2, self.format)
        return (datetime2-datetime1).seconds