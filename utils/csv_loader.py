import csv

__author__ = 'mkk'

class CSVLoader:
    def __init__(self, path):
        self.path = path


    def extract_col(self, colnum, offset=0):
        """
        To extract a column from a csv file
        :param colnum: Column index by zero-based indexing
        :param offset:
        :return:
        """
        col = []
        cnt = 0
        with open(self.path, 'r') as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                if cnt < offset:
                    cnt += 1
                else:
                    col.append(float(row[colnum]))
            f.close()
        return col
